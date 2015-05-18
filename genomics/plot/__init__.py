# -*- coding: utf-8 -*-
'''
.. module:: genomics.plot
   :synopsis: Genome plotting
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero General Public License, see LICENSE for details

    .. moduleauthor:: Tiago Antao <tiagoantao@gmail.com>
'''

from functools import partial
import math
import random

import numpy
from matplotlib import patches
import matplotlib.pyplot as plt

from genomics import organism


def get_defaults(add_ax=True, **kwargs):
    '''Gets defaults for figure and ax if they are not on kwargs.'''
    fig = kwargs.get("fig", plt.figure(figsize=(15, 8)))
    if add_ax:
        ax = kwargs.get("ax", fig.add_subplot(1, 1, 1))
    else:
        ax = None
    return fig, ax


class GenomePlot(object):
    # TODO: use abc
    """A Genome plot.

    For now only thought for complete genomes (i.e. not it scaffold state)
    """

    def __init__(self, **kwargs):
        if 'fig' in kwargs:
            self.fig = kwargs['fig']
        else:
            self.fig = plt.figure()
        self.features = {}
        self.fig.subplots_adjust(top=0.99, left=0.01, bottom=0.01,
                                 right=0.99, wspace=0.008, hspace=0)

    def get_feature(self, fname):
        raise NotImplementedError("Abstract method")

    def plot_annotations(self, annots):
        raise NotImplementedError("Abstract method")


class GridGenomePlot(GenomePlot):
    """A Genome plotted as a Grid.

    Args:
        genome: A :class:`genomics.organism.Genome` object
        ncols: Number of columns
    """

    def __init__(self, genome, ncols, **kwargs):
        '''
        '''
        GenomePlot.__init__(self, **kwargs)
        chroms = genome.chrom_order
        nrows = math.ceil(len(chroms) / ncols)
        i = 1
        self.max_size = 0
        for chrom in chroms:
            size, centro = genome.chroms[chrom]
            if size > self.max_size:
                self.max_size = size
        for chrom in chroms:
            size, centro = genome.chroms[chrom]
            if chrom == chroms[0]:  # start
                self.features[chrom] = self.fig.add_subplot(nrows, ncols, i,
                                                            frame_on=True)
                self.features[chrom].get_yaxis().tick_left()
            else:
                self.features[chrom] = self.fig.add_subplot(
                    nrows, ncols, i, frame_on=True,
                    sharey=self.features[chroms[0]])
                self.features[chrom].get_yaxis().set_visible(False)
            self.features[chrom].get_xaxis().set_visible(False)
            if centro == organism.CentroPos.center:
                diff = self.max_size - size
                self.features[chrom].set_xlim(-diff // 2,
                                              self.max_size - diff // 2)
                self.features[chrom].text(- diff // 2, 1, chrom, va='top',
                                          ha='left', size='xx-large',
                                          backgroundcolor='pink')
            elif centro == organism.CentroPos.left:
                self.features[chrom].set_xlim(1, self.max_size)
                self.features[chrom].text(self.max_size, 1, chrom, va='top',
                                          ha='right', size='xx-large',
                                          backgroundcolor='pink')
            else:  # right AND default
                self.features[chrom].text(size - self.max_size, 1, chrom,
                                          va='top', ha='left',
                                          size='xx-large',
                                          backgroundcolor='pink')
                self.features[chrom].set_xlim(size - self.max_size, size)
            # self.features[chrom].axvline(0)
            i += 1

    def plot_annotations(self, annots, random_height=True, max_height=1):
        '''Plots annotations
        '''
        colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'black']
        i = 0
        for name, (type_, chrom, start, end) in annots.items():
            ax = self.features[chrom]
            if end is None:
                ax.axvline(start, 0, max_height, color='magenta')
            else:
                if random_height:
                    height = random.uniform(max_height / 2, max_height)
                else:
                    height = max_height
                rect = patches.Rectangle(
                    (start, 0), width=end - start,
                    height=height,
                    color=colors[i % len(colors)], alpha=0.1)
                i += 1
                ax.add_patch(rect)


def plot_percentile(ax, data, wsize, wstep,
                    geofuncs=(partial(numpy.percentile, q=5),
                              partial(numpy.percentile, q=20),
                              numpy.median,
                              partial(numpy.percentile, q=80),
                              partial(numpy.percentile, q=95)),
                    funcs=((max, '.'), (numpy.mean, '#0099FF'), (min, '.'))):
    """Plot percentiles.

    Data should be presented sorted by x as a list of pairs of x, y.
    """
    pts = [[] for i in range(len(geofuncs))]
    fpts = [[] for i in range(len(funcs))]
    xs = []
    bin_indexes = []
    min_pos = 0
    minx = data[0][0]
    maxx = data[-1][0]
    half = wsize / 2
    for bindex in range(math.floor(minx / wstep), math.ceil(maxx / wstep)):
        bin_indexes.append([0, 0])
        middle = wstep * bindex + half
        start = middle - half
        end = middle + half
        for pos in range(min_pos, len(data)):
            x = data[pos][0]
            if x < start:
                min_pos = pos + 1
                continue
            if x > end:
                break
            bin_indexes[-1][1] = pos
        bin_indexes[-1][0] = min_pos
    for start, end in bin_indexes:
        xstart = data[start][0]
        xs.append(xstart + half)
        my_data = [y[1] for y in data[start:end + 1]]
        for i in range(len(geofuncs)):
            if len(my_data) == 0:
                pts[i].append(None)
            else:
                pts[i].append(geofuncs[i](my_data))
        for i in range(len(funcs)):
            if len(my_data) == 0:
                fpts[i].append(None)
            else:
                fpts[i].append(funcs[i][0](my_data))
    colors = ["b", "c"]
    cut = (len(pts) - 1) / 2 - 0.5
    for i in range(len(pts) - 1):
        y1 = pts[i]
        y2 = pts[i + 1]
        cleanx, cleany1, cleany2 = [], [], []
        for j in range(len(xs)):
            if y2[j] is not None and y1[j] is not None:
                cleanx.append(xs[j])
                cleany1.append(y1[j])
                cleany2.append(y2[j])
        color = colors[int(math.floor(abs(i - cut)))]
        ax.fill_between(cleanx, cleany1, cleany2, color=color)
    if len(pts) > 0:
        ax.plot(xs, pts[len(pts) // 2], 'w')
    for i in range(len(fpts)):
        ax.plot(xs, fpts[i], funcs[i][1])
