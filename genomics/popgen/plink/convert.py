# -*- coding: utf-8 -*-
'''
.. module:: genomics.popgen.plink.convert
   :synopsis: PLINK conversion to other formats
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import os


def to_genepop(plink_pref, gp_pref, pop_dict, header="plink2gp"):
    '''Converts a PED/MAP PLINK file to genepop.

    :param plink_pref: PLINK prefix
    :param gp_pref: Genepop prefix
    :param pop_dict: Dictionary population -> [fam, ind]
    :param header: Genepop header

    The Genepop file will be called gp_pref.gp.

    A gp_pref.pops file will report the order (sorted by name) of the
        populations in the Genepop file.
    '''
    ws = {}
    pops = list(pop_dict.keys())
    pops.sort()
    wGP = open(gp_pref + ".gp", "w")
    wGP.write(header + "\n")
    indivPops = {}

    wPop = open(gp_pref + ".pops", "w")
    for pop in pops:
        ws[pop] = open(str(os.getpid()) + "_" + pop, "w")
        wPop.write("%s\n" % pop)
        for fam, ind in pop_dict[pop]:
            indivPops.setdefault((fam, ind), []).append(pop)
    wPop.close()

    f = open(plink_pref + ".map")
    for l in f:
        toks = l.rstrip().replace(" ", "\t").split("\t")
        chro = toks[0]
        rs = toks[1]
        pos = toks[3]
        wGP.write("%s/%s/%s\n" % (chro, rs, pos))
    f.close()

    f = open(plink_pref + ".ped")
    for l in f:
        toks = l.rstrip().replace(" ", "\t").split("\t")
        fam = toks[0]
        id = toks[1]
        try:
            my_pops = indivPops[(fam, id)]
        except KeyError:
            continue  # Not to be processed
        for pop in my_pops:
            ws[pop].write("%s/%s," % (fam, id))
            alleles = toks[6:]
            for i in range(len(alleles) // 2):
                aStr = ""
                for a in [alleles[2 * i], alleles[2 * i + 1]]:
                    if a == "A":
                        aStr += "01"
                    elif a == "C":
                        aStr += "02"
                    elif a == "T":
                        aStr += "03"
                    elif a == "G":
                        aStr += "04"
                    else:
                        aStr += "00"
                ws[pop].write(" " + aStr)
            ws[pop].write("\n")

    for pop in pops:
        ws[pop].close()
        wGP.write("POP\n")
        f = open(str(os.getpid()) + "_" + pop)
        for l in f:
            wGP.write(l)
        f.close()
        os.remove(str(os.getpid()) + "_" + pop)
    wGP.close()


def to_ldhat(plink_pref, ld_sites, ld_locs):
    '''Converts a PED/MAP PLINK file to genepop.

    :param plink_pref: PLINK prefix
    :param ld_sites: LD sites file
    :param ld_sites: LD locs file
    '''
    f = open(plink_pref + ".map")
    poses = []
    w = open(ld_locs, 'w')
    for l in f:
        toks = l.rstrip().replace(" ", "\t").split("\t")
        pos = int(toks[3])
        poses.append(pos / 1000)
    f.close()
    w.write('%d %d L\n' % (len(poses), poses[-1] + 1))
    w.write('\n'.join([str(pos) for pos in poses]) + '\n')
    w.close()

    f = open(plink_pref + '.ped')
    ninds = 0
    for l in f:
        ninds += 1
    f.close()
    f = open(plink_pref + '.ped')
    w = open(ld_sites, 'w')
    w.write('%d %d 2\n' % (ninds * 2, len(poses)))
    for l in f:
        toks = l.rstrip().replace(" ", "\t").split("\t")
        ind = toks[1]
        a1s = toks[6::2]
        a2s = toks[7::2]
        w.write('>%s_1\n' % ind)
        w.write(''.join(a1s) + '\n')
        w.write('>%s_2\n' % ind)
        w.write(''.join(a2s) + '\n')
    w.close()
    f.close()
