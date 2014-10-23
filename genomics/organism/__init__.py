# -*- coding: utf-8 -*-
'''
.. module:: organism
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
ag = Genome('Anopheles gambiae PEST', 'Ag', 180454, 'Ag PEST')

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
