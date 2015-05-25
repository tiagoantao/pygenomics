# -*- coding: utf-8 -*-
'''
.. module:: genomics.popgen.admix.plot
   :synopsis: Admixture plot
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero General Public License, see LICENSE for details

.. moduleauthor:: Tiago Antao <tiago@popgen.net>
'''

from matplotlib import pyplot as plt

#Most function names are not verbs because the module name is already one


def _get_defaults(add_ax=True, **kwargs):
    if 'fig' in kwargs:
        fig = kwargs['fig']
    else:
        fig = plt.figure(figsize=(15, 8))
    if add_ax:
        if 'ax' in kwargs:
            ax = kwargs['ax']
        else:
            ax = fig.add_subplot(1, 1, 1)
    else:
        ax = kwargs.get('ax', None)
    return fig, ax


def single(components, cluster, nrows=1, with_names=False,
           with_pop_labels=True,
           colors=['r', 'g', '0.25', 'b', 'y', '0.75', 'm', 'c', '0.5', 'k',
                   '#ffebcd', '#0000cd', '#006400', '#daa520', '#b22222',
                   '#ff4500', '#a020f0', '#abcdef', '#987654', '#1166ff'],
           with_white_bar=False,
           **kwargs):
    '''Plots Admixture.

    Args:
        components: dict individual -> components
        cluster: list of tuple (cluster, [individuals])
        with_pop_labels: print pop labels
    '''
    fig, ax = _get_defaults(**kwargs)
    nrows = kwargs.get('nrows', 1)
    with_names = kwargs.get('with_names', False)
    all_ind_ks = []
    all_ind_names = []
    for name, inds in cluster.items():
        all_ind_ks.extend([components[ind] for ind in inds])
        all_ind_names.extend([ind for ind in inds])
    nks = len(all_ind_ks[0])

    def draw_row(sp, row_inds, start_ind, inds_row, ind_names):
        bottoms = [0.0] * len(row_inds)
        for k in range(nks):
            i = 0
            sp.bar(range(len(row_inds)), [ks[k] for ks in row_inds],
                   lw=0, width=1, bottom=bottoms, color=colors[k])
            for ind in row_inds:
                bottoms[i] += ind[k]
                i += 1
        if with_white_bar:
            sp.bar(range(len(row_inds)),
                   [j % 2 == 0 for j in range(len(row_inds))],
                   color='white', alpha=0.4, lw=0, width=1)
        pos = 0
        for name, inds in cluster.items():
            pos += len(inds)
            if pos > start_ind + inds_row:
                break
            elif pos < start_ind:
                continue
            if with_pop_labels:
                sp.text(pos - start_ind, 0.5, name, ha='right', va='center',
                        rotation='vertical',
                        fontsize=kwargs.get('popfontsize', 'small'),
                        backgroundcolor='white')
            sp.axvline(pos - start_ind, color='black', lw=0.5)
        sp.set_ylim(0, 1.0)
        sp.set_xlim(0, inds_row + 1)
        if with_names:
            pos = 0
            for name in ind_names:
                sp.text(pos, 1.0, name, ha='left', va='top',
                        rotation='vertical',
                        alpha=0.5,
                        fontsize=kwargs.get('indfontsize', 'small'),
                        backgroundcolor='white')
                pos += 1

    inds_row = len(all_ind_ks) // nrows
    for row in range(nrows):
        if nrows == 1:
            sp = ax
        else:
            sp = fig.add_subplot(nrows, 1, row + 1)
        start = row * inds_row
        if row == nrows - 1 and nrows != 1:
            end = None
        else:
            end = (row + 1) * inds_row  # NOT - 1
        row_inds = all_ind_ks[start:end]
        ind_names = all_ind_names[start:end]
        draw_row(sp, row_inds, start, inds_row, ind_names)
        sp.get_yaxis().set_visible(False)
        sp.get_xaxis().set_visible(False)

    return fig


def stacked(k_components, cluster, fig, k_colors=None, **kwargs):
    '''Plots stacked admixture plots in increasing order of K.

    Args:
        k_components: dict k -> (dict individual -> components)
        cluster: list of tuple (cluster, [individuals])
        fig: matplotlib figure
        k_colors: color per K (can be incomplete)
    '''
    k_colors = k_colors or {}
    fig.clf()
    ks = list(k_components.keys())
    ks.sort()
    for i, k in enumerate(ks):
        ax = fig.add_subplot(len(ks), 1, i + 1)
        if k in k_colors:
            single(k_components[k], cluster, fig=fig, ax=ax,
                   colors=k_colors[k],
                   with_pop_labels=False)
        else:
            single(k_components[k], cluster, fig=fig, ax=ax,
                   with_pop_labels=False)

    pos = 0
    for name, inds in cluster.items():
        pos += len(inds)
        ax.text(pos, 0.0, name, ha='right', va='bottom',
                rotation='vertical',
                fontsize=kwargs.get('popfontsize', 'small'),
                backgroundcolor='white')
    fig.tight_layout()
