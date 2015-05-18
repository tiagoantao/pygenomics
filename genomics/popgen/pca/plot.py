# -*- coding: utf-8 -*-
'''
.. module:: genomics.popgen.pca.plot
   :synopsis: PCA plotting
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero General Public License, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>
'''

import matplotlib.pyplot as plt

from genomics.plot import get_defaults


def render_pca(indivs, comp1=1, comp2=2,
               markers=None, colors=None,
               weights=None, cluster=None, gray=None, tag_indivs=None,
               **kwargs):
    '''Plots two components of PCA.

    If the cluster is empty, it will plot the name of the individual

    Parameters:
        - indivs     - dict individual -> coordinates
        - comp1      - First component to plot (starts at 1)
        - comp2      - Second component to plot
        - cluster    - dict individual -> cluster
        - weights    - PCA weights (relative or absolute)
        - gray       - List of clusters to "gray out" (requires cluster)
        - tag_indivs - List of individuals to tag (requires cluster)
        - markers    - Markers dictionary (cluster key -> marker)
    '''
    gray = gray or []
    tag_indivs = tag_indivs or []
    comp_cluster = {}
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
        my_weights = [100 * w / sum(weights) for w in weights]
        ax.set_xlabel('PC %d (%.1f)' % (comp1, my_weights[comp1 - 1]))
        ax.set_ylabel('PC %d (%.1f)' % (comp2, my_weights[comp2 - 1]))
    xmin, xmax, ymin, ymax = (float('inf'), float('-inf'),
                              float('inf'), float('-inf'))
    for indiv, indiv_comps in indivs.items():
        x, y = indiv_comps[comp1 - 1], indiv_comps[comp2 - 1]
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
        for group in groups:
            if group in gray:
                continue
            if len(comp_cluster[group]) == 0:
                continue
            if markers is None:
                marker = 'o'
            else:
                marker = markers.get(group, None)
            if colors is None:
                color = None
            else:
                color = colors.get(group, None)
            x, y = zip(*comp_cluster[group])
            ax.plot(x, y, marker=marker, color=color, label=group, ls=' ')
        ax.legend(loc="right")
        xmin, xmax = ax.get_xlim()
        ax.set_xlim(xmin, xmax + 0.1 * (xmax - xmin))  # space for legend
    return fig, ax


def render_pca_eight(indivs, title=None,
                     weights=None, cluster=None, gray=None, tag_indivs=None,
                     markers=None, colors=None,
                     **kwargs):
    '''Plots eight components of PCA.

    PC1 and PC2 have a special chart.
    If the cluster is empty, it will plot the name of the individual

    Parameters:
        - indivs     - dict individual -> coordinates
        - weights    - PCA weights (relative or absolute)
        - cluster    - dict individual -> cluster
        - gray       - List of clusters to "gray out" (requires cluster)
        - tag_indivs - List of individuals to tag (requires cluster)
        - markers    - Markers dictionary (cluster key -> marker)
    '''
    gray = gray or []
    tag_indivs = tag_indivs or []
    comp_cluster = [{} for i in range(4)]
    if cluster is not None:
        groups = list(set(cluster.values()))
        groups.sort()
        for group in groups:
            for i in range(4):
                comp_cluster[i][group] = []

    if 'figsize' not in kwargs:
        kwargs['figsize'] = 16, 9
    fig, ax_ = get_defaults(add_ax=False, **kwargs)  # we ignore ax_
    lims = []
    for i in range(4):
        #  xmin, xmax, ymin, ymax
        lims.append((float('inf'), float('-inf'), float('inf'), float('-inf')))
    ax = fig.add_subplot(1, 2, 1)
    axs = [ax]
    axs.append(fig.add_subplot(2, 4, 3))
    axs.append(fig.add_subplot(2, 4, 4))
    axs.append(fig.add_subplot(2, 4, 7))
    axs.append(fig.add_subplot(2, 4, 8))
    for indiv, indiv_comps in indivs.items():
        for i in range(4):
            xmin, xmax, ymin, ymax = lims[i]
            x, y = indiv_comps[i * 2], indiv_comps[i * 2 + 1]
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            lims[i] = xmin, xmax, ymin, ymax
            if cluster is None or indiv in tag_indivs:
                ax.text(x, y, indiv)
            if cluster is not None:
                group = cluster[indiv]
                comp_cluster[i][group].append((x, y))
    if weights is not None:
        my_weights = [100 * w / sum(weights) for w in weights]
    for i in range(4):
        ax = axs[i]
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        xmin, xmax, ymin, ymax = lims[i]
        if weights is not None:
            ax.text(xmin, ymin, 'PC %d (%.1f)' % (i * 2 + 1,
                                                  my_weights[i * 2]),
                    va='bottom')
            ax.text(xmax, ymax, 'PC %d (%.1f)' % (i * 2 + 2,
                                                  my_weights[i * 2 + 1]),
                    ha='right', rotation='vertical', va='top')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        if cluster is not None:
            for group in gray:
                if len(comp_cluster[group]) == 0:
                    continue
                x, y = zip(*comp_cluster[group])
                ax.plot(x, y, ".", color="#BBBBBB", label=group)
            for group in groups:
                if group in gray:
                    continue
                if len(comp_cluster[i][group]) == 0:
                    continue
                x, y = zip(*comp_cluster[i][group])
                if markers is None:
                    marker = '.'
                else:
                    marker = markers.get(group, None)
                if colors is None:
                    color = None
                else:
                    color = colors.get(group, None)
                ax.plot(x, y, marker=marker, color=color, label=group, ls=' ')
    if cluster is not None:
        handles, labels = axs[-2].get_legend_handles_labels()
        axs[-1].legend(handles, labels, loc='center')
    axs[-1].get_xaxis().set_visible(False)
    axs[-1].get_yaxis().set_visible(False)
    if title is not None:
        fig.suptitle(title)
    plt.tight_layout(h_pad=0, w_pad=0)
    return fig, axs
