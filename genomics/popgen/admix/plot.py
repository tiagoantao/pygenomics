# -*- coding: utf-8 -*-
"""
.. module:: genomics.popgen.admix.plot
   :synopsis: Admixture plot
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero General Public License, see LICENSE for details

.. moduleauthor:: Tiago Antao <tiago@popgen.net>
"""

import math

from matplotlib import pyplot as plt

#Most function names are not verbs because the module name is already one


def _get_defaults(add_ax=True, **kwargs):
    fig = kwargs.get("fig", plt.figure(figsize=(15, 8)))
    if add_ax:
        ax = kwargs.get("ax", fig.add_subplot(1, 1, 1))
    else:
        ax = None
    return fig, ax


def single(components, cluster, **kwargs):
    """Plots Admixture.

    Parameters:
        - components  - dict individual -> components
        - cluster     - list of tuple (cluster, [individuals])
    """
    fig, ax = _get_defaults(add_ax=False, **kwargs)
    nrows = kwargs.get("nrows", 1)
    with_names = kwargs.get("with_names", False)
    colors = ["r", "g", "0.25", "b", "y", "0.75", "m", "c", "0.5", "k",
              "#ffebcd", "#0000cd", "#006400", "#daa520", "#b22222",
              "#ff4500", "#a020f0", "#abcdef", "#987654", "#1166ff"]
    all_ind_ks = []
    all_ind_names = []
    for name, inds in cluster:
        all_ind_ks.extend([components[ind] for ind in inds])
        all_ind_names.extend([ind[1] for ind in inds])
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
        sp.bar(range(len(row_inds)),
               [i % 2 == 0 for i in range(len(row_inds))],
               color="white", alpha=0.4, lw=0, width=1)
        pos = 0
        for name, inds in cluster:
            pos += len(inds)
            if pos > start_ind + inds_row:
                break
            elif pos < start_ind:
                continue
            sp.text(pos - start_ind, 0.5, name, ha="right", va="center",
                    rotation="vertical",
                    fontsize=kwargs.get("popfontsize", "small"),
                    backgroundcolor="white")
            sp.axvline(pos - start_ind, color="black", lw=0.5)
        sp.set_ylim(0, 1.05)
        sp.set_xlim(0, inds_row + 1)
        if with_names:
            pos = 0
            for name in ind_names:
                sp.text(pos, 1.0, name, ha="left", va="top",
                        rotation="vertical",
                        alpha=0.5,
                        fontsize=kwargs.get("indfontsize", "small"),
                        backgroundcolor="white")
                pos += 1

    inds_row = math.ceil(len(all_ind_ks) / nrows)
    for row in range(nrows):
        sp = fig.add_subplot(nrows, 1, row + 1)
        start = row * inds_row
        if row == nrows - 1:
            end = None
        else:
            end = (row + 1) * inds_row  # NOT - 1
        row_inds = all_ind_ks[start:end]
        ind_names = all_ind_names[start:end]
        draw_row(sp, row_inds, start, inds_row, ind_names)

    return fig


def stacked(k_components, cluster, **kwargs):
    """Plots stacked admixture plots in increasing order of K.

    Parameters:
        - k_components  - dict k -> (dict individual -> components)
        - cluster       - list of tuple (cluster, [individuals])
    """
    fig, axs = plt.subplots(len(k_components), **kwargs)
    for i, k in enumerate(k_components):
        single(k_components[k], cluster, fig=fig, ax=axs[i])

    fig.tight_layout()
