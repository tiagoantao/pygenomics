# -*- coding: utf-8 -*-
'''
.. module:: genomics.popgen.pca.smart
   :synopsis: Eigensoft smartPCA utilities
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import os


class SmartPCAController(object):
    '''Controller for EIGENSOFT smartpca.

    pref - the prefix of all input and output files
    '''
    def __init__(self, pref):
        self._pref = pref

    @property
    def pref(self):
        return self._pref

    def get_config(self):
        return ('genotypename: {0}.geno\n'
                'snpname: {0}.snp\n'
                'indivname: {0}.ind\n'
                'evecoutname: {0}.evec\n'
                'evaloutname: {0}.eval\n'
                'altnormstyle: NO\n'
                'numoutevec: 10\n'
                'numoutlieriter: 0\n'
                'numoutlierevec: 10\n'
                'outliersigmathresh: 6\n'
                'qtmode: 0\n').format(self.pref)

    def run(self, param_name=None):
        param_name = param_name or '%s.param' % self.pref
        w = open(param_name, 'wt')  # XXX python3?
        w.write(self.get_config())
        w.close()
        os.system('smartpca -p %s' % param_name)


def parse_evec(evec_name, evl_name=None):
    '''Parse SMARTPCA evec output.

    Arguments:
        evec_name - the EVEC file
        evl_name  - Optional, full list of weights

    If there is a full list of weights, then the percentage of each
    component will be computed

    Returns:
        weights
        weights_as_percentage
        dict individual -> components
    '''
    f = open(evec_name)
    header = f.readline().strip()
    weights = [float(x) for x in header.split(' ')[1:] if x != '']
    indivs = {}
    for l in f:
        toks = [x for x in l.rstrip().split(' ') if x != '']
        indivs[toks[0]] = [float(x) for x in toks[1:-1]]
    if evl_name is None:
        return weights, None, indivs
    f = open(evl_name)
    all_weights = [float(x.rstrip().strip()) for x in f.readlines()]
    sum_weights = sum(all_weights)
    return all_weights, [x / sum_weights for x in all_weights], indivs
