# -*- coding: utf-8 -*-
"""
.. module:: genomics.popgen.pca.plot
   :synopsis: PCA plotting
   :copyright: Copyright 2013 by Tiago Antao
   :license: GNU Affero General Public License, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>
"""

from genomics.plot import get_defaults

def render_pca(indivs, weights, comp1=1, comp2=2, **kwargs):
    """Plots a PCA.

    If the cluster is empty, it will plot the name of the individual

    Parameters:
        - indivs     - dict individual -> coordinates
        - weights    - PCA weights (relative or absolute)
        - comp1      - First component to plot (starts at 1)
        - comp2      - Second component to plot
        - cluster    - dict individual -> cluster
        - gray       - List of clusters to "gray out" (requires cluster)
        - tag_indivs - List of individuals to tag (requires cluster)
    """
    comp_cluster = {}
    cluster = kwargs.get("cluster", None)
    tag_indivs = kwargs.get("tag_indivs", [])
    gray = kwargs.get("gray", [])
    if cluster is not None:
        groups = list(set(cluster.values()))
        groups.sort()
        for group in groups:
            comp_cluster[group] = []

    fig, ax = get_defaults(**kwargs)
    if weights is None:
        ax.set_xlabel('PC %d' % comp1)
        ax.set_ylabel('PC %d' % comp2)
    else:
        ax.set_xlabel('PC %d (%.1f)' % (comp1, 100 * weights[comp1 - 1]))
        ax.set_ylabel('PC %d (%.1f)' % (comp2, 100 * weights[comp2 - 1]))
    xmin, xmax, ymin, ymax = None, None, None, None
    for indiv, indiv_comps in indivs.items():
        x, y = indiv_comps[comp1 - 1], indiv_comps[comp2 - 1]
        if xmin is None:
            xmin = xmax = x
            ymin = ymax = y
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if cluster is None or indiv in tag_indivs:
            ax.text(x, y, indiv)
        if cluster is not None:
            group = cluster[indiv]
            comp_cluster[group].append((x, y))
    if cluster is None:
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
    else:
        for group in gray:
            if len(comp_cluster[group]) == 0:
                continue
            x, y = zip(*comp_cluster[group])
            ax.plot(x, y, ".", color="#BBBBBB", label=group)
        cnt = 0
        markers = ["o", "+", ","]
        for group in groups:
            if group in gray:
                continue
            if len(comp_cluster[group]) == 0:
                continue
            x, y = zip(*comp_cluster[group])
            ax.plot(x, y, markers[cnt // 7], label=group)
            cnt += 1
        ax.legend(loc="right")
        xmin, xmax = pylab.xlim()
        ax.set_xlim(xmin, xmax + 0.1 * (xmax - xmin))  # space for legend
    return ax
