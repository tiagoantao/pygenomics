# -*- coding: utf-8 -*-
'''
.. module:: genomics.organism
   :synopsis: Meta-data for organisms
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
from copy import deepcopy
from enum import Enum

CentroPos = Enum('CentroPos', 'left right center unknown')


class Genome:
    '''Representation of a Genome.

    A genome has a name, a short name, a (NCBI) taxon id and description.
    It is composed of a set of chromosomes, which have an order.

    >>> hs37 = Genome('Homo sapiens build 37', 'Hs', 9606, 'Hs b37')
    '''
    def __init__(self, name, short_name, taxid, desc):
        self.name = name
        self.short_name = short_name
        self.taxid = taxid
        self.desc = desc
        self.chrom_order = []
        self.chroms = {}

    def add_chrom(self, chrom, size):
        self.chroms[chrom] = size
        self.chrom_order.append(chrom)

    @property
    def chroms(self):
        return self._chroms

    @chroms.setter
    def chroms(self, chroms):
        self._chroms = chroms
        if len(self.chrom_order) == 0:
            keys = list(chroms.keys())

            def calc_key(x):
                try:
                    # ordering of numerical chromosomes
                    return '%04d' % int(x)
                except:
                    return x
            keys.sort(key=calc_key)
            self.chrom_order = keys

    def __str__(self):
        my_str = 'Species: %s (%s, taxid: %d)\n' % (self.name,
                                                    self.short_name,
                                                    self.taxid)
        my_str += '%s\n' % self.desc
        my_str += '%s\n' % str(self.chrom_order)
        my_str += '%s\n' % str(self.chroms)
        return my_str


def remove_chromosome(genome, chrom):
    '''Creates a new Genome object with a chromosome removed'''
    genome = deepcopy(genome)
    try:
        del genome.chroms[chrom]
    except KeyError:
        pass
    try:
        del genome.chrom_order[genome.chrom_order.index(chrom)]
    except ValueError:
        pass
    return genome


def remove_sex_chromosomes(genome):
    '''Creates a new Genome object with sex chromosomes removed'''
    for chrom in ['X', 'Y']:
        genome = remove_chromosome(genome, chrom)
    return genome

genome_db = {}

# Homo sapiens build 37
hs37 = Genome('Homo sapiens build 37', 'Hs', 9606, 'Hs b37')

hs37.chroms = {
    '1': (249250621, CentroPos.center),
    '2': (243199373, CentroPos.center),
    '3': (198022430, CentroPos.center),
    '4': (191154276, CentroPos.center),
    '5': (180915260, CentroPos.center),
    '6': (171115067, CentroPos.center),
    '7': (159138663, CentroPos.center),
    '8': (146364022, CentroPos.center),
    '9': (141213431, CentroPos.center),
    '10': (135534747, CentroPos.center),
    '11': (135006516, CentroPos.center),
    '12': (133851895, CentroPos.center),
    '13': (115169878, CentroPos.right),
    '14': (107349540, CentroPos.right),
    '15': (102531392, CentroPos.right),
    '16': (90354753, CentroPos.center),
    '17': (81195210, CentroPos.center),
    '18': (78077248, CentroPos.center),
    '19': (59128983, CentroPos.center),
    '20': (63025520, CentroPos.right),
    '21': (48129895, CentroPos.left),
    '22': (51304566, CentroPos.right),
    'X': (155270560, CentroPos.center),
    'Y': (59373566, CentroPos.right)
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
