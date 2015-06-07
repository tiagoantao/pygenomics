# -*- coding: utf-8 -*-
'''
.. module:: genomics.phylo.newick.convert
   :synopsis: Newick conversion to other formats
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import os

def _phylo_to_networkx(node, graph=None, my_id=0):
    graph = graph or nx.Graph()

    if node.is_terminal():
        next_id = my_id + 1
        name = node.name
        graph.add_node(name)
        node = graph.node[name]
        add_counts(haplo_to_seq[haplo], node)
        resistances = set([resistance])
    else:
        resistances = set()
        name = '%d' % my_id 
        graph.add_node(name, size=0.01)
        next_id = my_id + 1
        size = 0.0
        for child in node:
            ret = phylo_to_networkx(child, graph, next_id)
            child_res = ret['resistances']
            size += ret['size']
            if len(child_res) == 1:
                res = list(child_res)[0]
                if res == 'TA':
                    color = '#00FF00'
                elif res == 'TT':
                    color = '#FF3000'
                elif res == 'CA':
                    color = '#FF0030'
                else:
                    print(res)
            else:
                color = '#000000'
            resistances |= child_res
            graph.add_weighted_edges_from([(name, ret['name'], child.total_branch_length())], color=color)
            next_id = ret['next_id'] + 1
    return {'graph': graph, 'next_id': next_id, 'name': name,
            'resistances': resistances, 'size': size,
           }


def to_networkx(tree):
    '''Converts a Newick tree to NetworkX.

    Args:
        tree: A Newick tree from Biopython's Bio.Phylo.read

    Returns:
        A NetworkX Graph

    Requires NetworkX but not Biopython, though you will need it to
        parse the tree
    '''
