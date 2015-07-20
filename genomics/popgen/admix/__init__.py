# -*- coding: utf-8 -*-
'''
.. module:: genomics.popgen.admix
   :synopsis: Admixture
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''

from collections import OrderedDict

from scipy.spatial import distance
from scipy.cluster import hierarchy


def _get_cluster(components, my_inds=None):
    if my_inds is None:
        my_inds = list(components.keys())
    dist = distance.pdist([components[ind] for ind in my_inds])
    hcomp = hierarchy.complete(dist)
    ll = hierarchy.leaves_list(hcomp)
    return ll


def get_main_component(components):
    '''Gets the main component per individual (value and index)'''
    main_comps = {}
    for ind, comps in components.items():
        idx = comps.index(max(comps))
        main_comps[ind] = comps[idx], idx
    return main_comps


def cluster(components, pop_ind=None):
    '''Clusters individuals according to admixture results.

    Args:
        components: ordered dict individual -> components
        pop_ind: ordered dict pop -> [individuals]

        if pop_ind is None then all individuals are clustered
          irrespective of population
        if pop_ind is used then all individuals will be clustered
          inside their populations and the populations will be clustered,
          the new population order will be returned
    '''
    if pop_ind is None:
        return _get_cluster(components)
    lls = {}
    recluster = OrderedDict()
    pop_small = {}
    for i, pop in enumerate(pop_ind):
        inds = pop_ind[pop]
        lls[pop] = _get_cluster(components, inds)
        recluster[pop + '1'] = components[inds[lls[pop][0]]]
        recluster[pop + '2'] = components[inds[lls[pop][-1]]]
        pop_small[2 * i] = pop
        pop_small[2 * i + 1] = pop
    order = _get_cluster(recluster)
    pop_order = []
    for ind in order:
        pop = pop_small[ind]
        if pop not in pop_order:
            pop_order.append(pop)
        if len(pop_order) == len(pop_ind):
            break
    pop_ind_reorder = OrderedDict()
    for pop in pop_order:
        for pop2, inds in pop_ind.items():
            if pop2 == pop:
                break
        ll = lls[pop]
        pop_ind_reorder[pop] = [inds[i] for i in ll]
    return pop_ind_reorder
