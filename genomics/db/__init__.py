# -*- coding: utf-8 -*-
'''
.. module:: genomics.db
   :synopsis: Database for distributed write-once mapreduce ops
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import abc
import os


class DBException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Node(metaclass=abc.ABCMeta):
    '''A Database node

    :param db: Database
    :param to_write: Write node?
    :param desired_pos: Any position inside the node

    A node is a file that holds a (small) portion of the data. Its size is
    defined by the database granularity. It should be the size of the map
    operation on the map reduce framework. It should very easily fit in
    memory.
    '''
    def __init__(self, db, to_write, desired_pos=None):
        self.db = db
        self.to_write = to_write
        if to_write:
            self._vals = [None] * db.granularity

    def assign(self, position, value):
        if not self.to_write:
            raise DBException('Need to be in write mode to assign')
        self.vals[position - self.start_pos] = value

    def commit(self):
        if not self.to_write:
            raise DBException('Need to be in write mode to commit')
        node_dir = os.sep.join([self.base_dir] +
                               self.node_file.split(os.sep)[:-1])
        os.makedirs(node_dir)
        w = open(self.node_file + '.tmp', 'wt', encoding='utf-8')
        w.close()
        os.rename(self.node_file + '.tmp'. self.node_file)


class DB:
    '''A Database

    :param base_dir: Base directory
    :param node_class: Node class
    :param granularity: Record granularity
    :param is_sparse: Sparse implementation

    Granularity indicates how many positions a node can store. A sparse
    database will hold at most those. A non-sparse database will hold
    precisely those (save for the very last node).

    The node can be mostly anything structured that ends in something that is
    an integer.  For example is can be a (chromosome, position)
    '''
    def __init__(self, base_dir, key_class, granularity, is_sparse=False):
        self.base_dir = base_dir
        self.key_class = key_class
        self.granularity = granularity
        self.is_sparse = is_sparse

    def get_write_node(self, **kwargs):
        node = self.key_class(self.granularity, kwargs)
        return node.get_node(kwargs)

    def find_missing_nodes(self):
        pass


class Key:
    def __init__(self, db, granularity):
        self.db = db
        self.granularity = granularity

    def enumerate_nodes(self):
        pass

    def get_node(self, to_write, **kwargs):
        pass


class GenomeKey(Key):
    def __init__(self, db, granularity, genome):
        Key.__init__(self, db, granularity)
        self.genome = genome

    def enumerate_nodes(self):
        pass

    def get_node(self, to_write, chromosome, position):
        fname = os.sep.join('%s' % str(chromosome),
                            '%9d' % position // self.granularity)
        return Node(self.db.base_dir, fname, self.granularity, to_write,
                    self.db.is_sparse)
