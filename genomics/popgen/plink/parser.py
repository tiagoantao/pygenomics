# -*- coding: utf-8 -*-
'''
.. module: genomics.popgen.plink.parser
   :synopsis: Parsing of plink output files
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao.
   :license: GNU Affero, see LICENSE for details.

.. moduleauthor:: Tiago Antao <tra@popgen.net>
'''
import os


def parse_sep_header(l, sep=' '):
    return [x for x in l.rstrip().split(sep) if x != '']


def parse_sep_body(l, sep=' ', field_ids=None, my_types=None):
    l = l.rstrip()
    toks = [y for y in [x for x in l.rstrip().split(sep) if x != '']
            if y != '']
    if my_types:
        for i in range(len(my_types)):
            if my_types[i] in [int, float] and toks[i] in ["NA"]:
                toks[i] = None
            else:
                toks[i] = my_types[i](toks[i])
    if field_ids:
        rec = {}
        for i in range(len(field_ids)):
            try:
                rec[field_ids[i]] = toks[i]
            except IndexError:
                rec[field_ids[i]] = None
        return rec
    else:
        return toks


def parse_sep(f, sep=' ', my_types=None):
    field_ids = parse_sep_header(f.readline(), sep)
    for l in f:
        yield parse_sep_body(l, sep, field_ids, my_types)


def parse_locus_miss(f):
    '''Parse plink.lmiss file'''
    for res in parse_sep(f, my_types=[int, str, int, int, float]):
        yield res


def parse_hwe(f):
    '''Parse plink.hwe file'''
    for res in parse_sep(f, my_types=[int, str, str, str, str,
                                      str, float, float, float]):
        geno = res['GENO']
        res['GENO'] = [int(x) for x in geno.split('/')]
        yield res


def parse_sex_check(f):
    for res in parse_sep(f, my_types=[str, str, int, int, str, float]):
        yield res


def parse_het(f):
    for res in parse_sep(f, my_types=[str, str, int, float, int, float]):
        yield res


def parse_genome(f):
    for res in parse_sep(f, my_types=[str, str, str, str, str, str, float, float, float, float, int, float, float, float]):
        yield res


def parse_freq(f):
    for res in parse_sep(f, my_types=[int, str, str, str, float, int]):
        yield res


def parse_r2(f):
    for res in parse_sep(f, my_types=[int, int, str, int, int, str, float]):
        yield res


def parse_nearest(f):
    f.readline()  # Header file
    for l in f:
        toks = filter(lambda x: x != "", l.rstrip().split(" "))
        t1 = max([12, len(toks[0]) + 1])
        t2 = max([13, len(toks[1]) + 1])
        t3 = max([13, len(toks[5]) + 1])
        t4 = max([13, len(toks[6]) + 1])
        fid = l[:t1].strip()
        iid = l[t1:t1 + t2].strip()
        nn = int(l[t1 + t2:t1 + t2 + 7])
        min_dst = float(l[t1 + t2 + 7:t1 + t2 + 20])
        z = float(l[t1 + t2 + 20:t1 + t2 + 33])
        fid2 = l[t1 + t2 + 33:t1 + t2 + 33 + t3].strip()
        iid2 = l[t1 + t2 + 33 + t3:t1 + t2 + t3 + t4 + 33].strip()
        prop_diff = float(l[t1 + t2 + t3 + t4 + 33:-1])
        yield {"fid": fid, "iid": iid, "nn": nn, "min_dst": min_dst,
               "z": z, "fid2": fid2, "iid2": iid2, "prop_diff": prop_diff}


def get_snps(bim, accept_fun):
    f = open(bim)
    for l in f:
        toks = l.rstrip().replace(" ", "\t").split("\t")
        chro = int(toks[0])
        snp = toks[1]
        pos = int(toks[3])
        if accept_fun(chro, pos):
            yield snp
    f.close()
