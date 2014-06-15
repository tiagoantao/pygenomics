# -*- coding: utf-8 -*-
'''
.. module:: genomics.db
   :synopsis: Database for distributed write-once mapreduce ops
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import os


class DBException(Exception):
    pass  # TODO sort this out


class Node:
    '''A Database node

    :param base_dir: Base directory
    :param node_file: File that will hold the node
    :param start_pos: Start position in the current key contect
    :param size: Size of the node
    :param to_write: Write node?
    :param is_sparse: Sparse implementation

    A node is a file that holds a (small) portion of the data. Its size is
    defined by the database granularity. It should be the size of the map
    operation on the map reduce framework. It should very easily fit in
    memory.
    '''
    def __init__(self, base_dir, node_file, start_pos, size,
                 to_write, is_sparse):
        self.base_dir = base_dir
        self.node_file = node_file
        self.start_pos = start_pos
        self.size = size
        self.to_write = to_write
        self.is_sparse = is_sparse
        self._vals = [None] * size

    def assign(self, position, value):
        if not self.to_write:
            raise
        self.vals[position - self.start_pos] = value

    def commit(self):
        if not self.to_write:
            raise
        node_dir = os.sep.join([self.base_dir] +
                               self.node_file.split(os.sep)[:-1])
        os.makedirs(node_dir)
        w = open(self.node_file + '.tmp', 'wt', encoding='utf-8')
        w.close()
        os.rename(self.node_file + '.tmp'. self.node_file)


class DB:
    '''A Database

    :param base_dir: Base directory
    :param key_class: Key c;ass
    :param granularity: Record granularity
    :param is_sparse: Sparse implementation

    Granularity indicates how many positions a node can store. A sparse
    database will hold at most those. A non-sparse database will hold
    precisely those (save for the very last node).

    The key can be mostly anything that ends in something that is an integer.
    For example is can be a (chromosome, position)
    '''
    def __init__(self, base_dir, key_fun, granularity, is_sparse=False):
        self.base_dir = base_dir
        self.key_fun = key_fun
        self.granularity = granularity
        self.is_sparse = is_sparse

    def get_write_node(self, **kwargs):
        node_file = self.key_fun(self.granularity, kwargs)
        return Node(self.base_dir, node_file, True, self.is_sparse)

    def find_missing_nodes(self):
        pass


class Key:
    def __init__(self, granularity):
        self.granularity = granularity

    def enumerate_nodes(self):
        pass

    def get_node(self, **kwargs):
        pass


class GenomeKey(Key):
    def __init__(self, granularity, genome):
        Key.__init__(self, granularity)
        self.genome = genome

    def enumerate_nodes(self):
        pass

    def get_node(self, chromosome, position):
        return os.sep.join('%s' % str(chromosome),
                           '%9d' % position // self.granularity)
