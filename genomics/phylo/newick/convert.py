# -*- coding: utf-8 -*-
'''
.. module:: genomics.phylo.newick.convert
   :synopsis: Newick conversion to other formats
   :noindex:
   :copyright: Copyright 2015 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import networkx as nx


def _phylo_to_networkx(tree, _node=None, _graph=None, _my_id=None):
    '''Converts a Bio.Phylo.BaseTree.Tree to NetworkX

    Args:
        tree: Biopython's tree
        _node: Current node
        _graph: The NetworkX graph, internal parameter
        _my_id: ongoing ID, internal parameter
    '''
    if _node is None:
        _node = tree.root
        _my_id = 0
    graph = _graph or nx.Graph()

    if _node.is_terminal():
        next_id = _my_id + 1
        name = _node.name
        graph.add_node(name)
    else:
        name = '%d' % _my_id
        graph.add_node(name)
        for child in _node:
            ret = _phylo_to_networkx(child, graph, next_id)
            next_id = _my_id + 1
            graph.add_weighted_edges_from([(name, ret['name'],
                                            child.total_branch_length())])
            next_id = ret['next_id'] + 1
    return {'graph': graph, 'next_id': next_id, 'name': name}


def to_networkx(tree):
    '''Converts a Newick tree to NetworkX.

    Args:
        tree: A tree from Biopython's Bio.Phylo.BaseTreeTree

    Returns:
        A NetworkX Graph

    Requires NetworkX but not Biopython, though you will need it to
        parse the tree
    '''
    return _phylo_to_networkx(tree)
