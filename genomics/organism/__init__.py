# -*- coding: utf-8 -*-
'''
.. module:: genomics.organism
   :synopsis: Meta-data for organisms
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
from enum import Enum

CentroPos = Enum('CentroPos', 'left right center unknown')


class Genome:
    def __init__(self, name, short_name, taxid, desc):
        self.name = name
        self.short_name = short_name
        self.taxid = taxid
        self.desc = desc
        self.chroms = {}
        self.chrom_order = []

    def add_chrom(self, chrom, size):
        self.chroms[chrom] = size
        self.chrom_order.append(chrom)

    def __str__(self):
        my_str = 'Species: %s (%s, taxid: %d)\n' % (self.name,
                                                    self.short_name,
                                                    self.taxid)
        my_str += '%s\n' % self.desc
        my_str += '%s\n' % str(self.chrom_order)
        my_str += '%s\n' % str(self.chroms)
        return my_str


# Down: to remove, specific

genome_db = {}

# Homo sapiens build 37
hs37 = Genome('Homo sapiens build 37', 'Hs', 9606, 'Hs b37')

hs37.chroms = {
    1: 249250621,
    2: 243199373,
    3: 198022430,
    4: 191154276,
    5: 180915260,
    6: 171115067,
    7: 159138663,
    8: 146364022,
    9: 141213431,
    10: 135534747,
    11: 135006516,
    12: 133851895,
    13: 115169878,
    14: 107349540,
    15: 102531392,
    16: 90354753,
    17: 81195210,
    18: 78077248,
    19: 59128983,
    20: 63025520,
    21: 48129895,
    22: 51304566,
    'X': 155270560,
    'Y': 59373566
}

genome_db['Hs37'] = hs37

# Anopheles gambiae PEST reference 3.7
ag = Genome('Anopheles gambiae PEST 3.7', 'Ag', 180454, 'Ag PEST')

ag.chroms = {
    '2L': (49364325, CentroPos.left),
    '2R': (61545105, CentroPos.right),
    '3L': (41963435, CentroPos.left),
    '3R': (53200684, CentroPos.right),
    'X': (24393108, CentroPos.right),
    'UNKN': (42389979, None),
}
ag.chrom_order = ['2R', '2L', '3R', '3L', 'X', 'UNKN']

genome_db['Ag'] = ag
