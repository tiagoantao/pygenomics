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
import bz2
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

    def __str__(self):
        str_ = 'Keys: ' + '/'.join(self.key_order)
        str_ += ' Values: ' + '/'.join([repr(self.__dict__[x])
                                        for x in self.key_order])
        return str_


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
        Schema.__init__(self, granularity)
        self.genome = genome
        self.type = 'Genome'

    def enumerate_node_keys(self):
        for chrom in self.genome.chrom_order:
            size, centro = self.genome.chroms[chrom]
            max_node = 1 + size // self.granularity
            for i in range(max_node):
                yield Key(['chromosome', 'position'], chrom,
                          1 + i * self.granularity)

    def get_partial_node_for_key(self, key):
        chromosome = key.chromosome
        position = key.position
        inner_node = (position - 1) // self.granularity
        fname = os.sep.join(['%s' % str(chromosome), '%010d' % inner_node])
        return fname

    def __str__(self):
        return 'Genome Schema: %s' % self.genome.name


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
            self._vals = [None] * db.schema.granularity

    def assign(self, last_index_position, value):
        if not self.to_write:
            raise DBException('Need to be in write mode to assign')
        start_pos = self.key.get_last_key()
        self._vals[last_index_position - start_pos] = value

    def commit(self):
        if not self.to_write:
            raise DBException('Need to be in write mode to commit')
        node_file = os.sep.join([self.db.base_dir,
                                self.partial_name])
        node_dir = os.sep.join(node_file.split(os.sep)[:-1])
        try:
            os.makedirs(node_dir)
        except FileExistsError:
            pass  # This is ok
        w = bz2.open(node_file + '.tmp', 'wt', encoding='utf-8')
        start_pos = self.key.get_last_key()
        if self.db.is_sparse:
            poses = []
            vals = []
            for i, val in enumerate(self._vals):
                if val is not None:
                    vals.append(val)
                    poses.append(i)
            w.write('\t'.join([str(x + start_pos) for x in poses]))
            w.write('\n')
            for v in vals:
                w.write('%s\n' % repr(v))
        else:
            for v in self._vals:
                w.write('%s\n' % repr(v))
        w.close()
        os.rename(node_file + '.tmp', node_file)

    def __str__(self):
        str_ = 'DB/Schema: ' + '/'.join([self.db.base_dir,
                                         str(self.db.schema)])
        str_ += ' (%s)' % str(self.key)
        return str_


class DB:
    '''A Database

    :param base_dir: Base directory
    :param schema: Schema
    :param is_sparse: sparse representation?

    The node can be mostly anything structured that ends in something that is
    an integer.  For example is can be a (chromosome, position)
    '''
    def __init__(self, base_dir, schema, is_sparse):
        self.base_dir = base_dir
        self.schema = schema
        self.is_sparse = is_sparse

    def get_write_node(self, key):
        return Node(self, True, key)

    def find_missing_nodes(self):
        pass
