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


class Key:
    def __init__(self, key_order, *args):
        self.key_order = key_order
        for i, name in enumerate(key_order):
            self.__dict__[name] = args[i]

    def get_last_key(self):
        return self.__dict__[self.key_order[-1]]


class Schema(metaclass=abc.ABCMeta):
    '''A Database schema

    :param granularity: Record granularity

    Granularity indicates how many positions a node can store. A sparse
    database will hold at most those. A non-sparse database will hold
    precisely those (save for the very last node).
    '''
    def __init__(self, granularity):
        self.granularity = granularity

    @abc.abstractmethod
    def enumerate_node_keys(self):
        '''generator of key nodes'''
        pass

    @abc.abstractmethod
    def get_partial_node_for_key(self, key):
        '''Returns the partial name of the node (wo basedir)'''
        pass


class GenomeSchema(Schema):
    def __init__(self, granularity, genome):
        Schema.__init__(granularity)
        self.genome = genome

    def enumerate_node_keys(self):
        for chrom, size in self.genome.chroms.items():
            max_node = 1 + size // self.granularity
            for i in range(max_node):
                yield Key(['chromosome', 'position'], chrom,
                          1 + i * self.granularity)

    def get_partial_node_for_key(self, key):
        chromosome = key.chromosome
        position = key.position
        inner_node = (position - 1) // self.granularity
        fname = os.sep.join('%s' % str(chromosome), '%9d' % inner_node)
        return fname


class Node:
    '''A Database node

    :param db: Database
    :param to_write: Write node?
    :param key: Key to the first position

    A node is a file that holds a (small) portion of the data. Its size is
    defined by the database granularity. It should be the size of the map
    operation on the map reduce framework. It should very easily fit in
    memory.
    '''
    def __init__(self, db, to_write, key):
        self.db = db
        self.to_write = to_write
        self.key = key
        self.partial_name = db.schema.get_partial_node_for_key(key)
        if to_write:
            self._vals = [None] * db.granularity

    def assign(self, last_index_position, value):
        if not self.to_write:
            raise DBException('Need to be in write mode to assign')
        last_start_pos = self.key.get_last_pos()
        self.vals[last_index_position - last_start_pos] = value

    def commit(self):
        if not self.to_write:
            raise DBException('Need to be in write mode to commit')
        node_file = os.sep.join([self.base_dir,
                                self.partial_name])
        node_dir = os.sep.join(node_file.split(os.sep)[:-1])
        os.makedirs(node_dir)
        w = open(node_file + '.tmp', 'wt', encoding='utf-8')
        if self.db.is_sparse:
            poses = []
            vals = []
            for i, val in enumerate(self._vals):
                if val is not None:
                    vals.append(val)
                    poses.append(i)
            w.write('\t'.join([str(x + self.start_pos) for x in poses]))
            w.write('\n')
            for v in vals:
                w.write('%s\n' % repr(v))
        else:
            for v in self._vals:
                w.write('%s\n' % repr(v))
        w.close()
        os.rename(self.node_file + '.tmp'. self.node_file)


class DB:
    '''A Database

    :param base_dir: Base directory
    :param schema: Schema

    The node can be mostly anything structured that ends in something that is
    an integer.  For example is can be a (chromosome, position)
    '''
    def __init__(self, base_dir, schema):
        self.base_dir = base_dir
        self.schema = schema

    def get_write_node(self, key):
        return Node(self, True, key)

    def find_missing_nodes(self):
        pass
