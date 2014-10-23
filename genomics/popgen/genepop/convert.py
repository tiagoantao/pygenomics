# -*- coding: utf-8 -*-
'''
.. module:: genomics.popgen.pca.smart
   :synopsis: Eigen soft smart PCA
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''


def to_smartpca(gp_f, ind_w, snp_w, geno_w):
    '''Converts a Genepop file to smart PCA format

    :param gp_f: read handle for Genepop file
    :param ind_w: write handle for smartpca ind file
    :param snp_w: write handle for smartpca SNP file
    :param geno_w: write handle for smartpca genotype file
    '''
    from ..genepop.parser import read
    gph = read(gp_f)
    arr = []
    arr_names = []
    ind_pop = []
    pop = 0
    alleles_loci = [set() for x in gph.loci_list]

    pop_names = {}
    for rec in next(gph):
        if rec == ():
            pop += 1
            continue
        ind_pop.append(pop)
        ind, geno = rec
        pop_names[pop - 1] = ind
        for i in range(len(geno)):
            if geno[i][0] is not None:
                alleles_loci[i].add(geno[i][0])
        arr_names.append(ind)
        arr.append([x[0] for x in geno])
    for i in range(len(alleles_loci)):
        alleles_loci[i] = list(alleles_loci[i])
        alleles_loci[i].sort()

    def get_pca_indiv(geno):
        pca_indiv = []
        for i in range(len(alleles_loci)):
            allele = geno[i]
            for alt_allele in alleles_loci[i]:
                if allele is None:
                    pca_indiv.append(9)
                elif allele == alt_allele:
                    pca_indiv.append(1)
                else:
                    pca_indiv.append(0)
        return pca_indiv

    rinds = []
    for geno in arr:
        rind = get_pca_indiv(geno)
        rinds.append(rind)

    for name in arr_names:
        ind_w.write("%s U Case\n" % name)
    ind_w.close()

    pos = 0
    for i in range(len(gph.loci_list)):
        pos += 1
        for allele in alleles_loci[i]:
            snp_w.write("%s-%d 1 0.0 %d\n" % (gph.loci_list[i], allele, pos))
    ind_w.close()

    for i in range(len(rinds[0])):  # allele pos
        geno_w.write("%s\n" % "".join([str(x[i]) for x in rinds]))
    ind_w.close()
