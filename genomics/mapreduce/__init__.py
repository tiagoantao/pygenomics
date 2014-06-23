# -*- coding: utf-8 -*-
'''
.. module:: genomics.mapreduce
   :synopsis: MapReduce framework
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import importlib
import pickle
import os
import tempfile

import genomics

mr_dir = genomics.cfg.mr_dir


def pickle_in(datum):
    w = tempfile.NamedTemporaryFile(dir=mr_dir, delete=False)
    pickle.dump(datum, w)
    w.close()
    return w.name


def do_map(pname):
    f = open(pname, 'rb')
    paras = pickle.load(f, encoding='bytes')
    f.close()
    fqdn_name = paras[0]
    fqdn_toks = fqdn_name.split('.')
    module = importlib.import_module('.'.join(fqdn_toks[:-1]))
    fun = getattr(module, fqdn_toks[-1])
    node = paras[1]
    args = paras[2:]
    fun(node, *args)
    node.commit()
    os.remove(pname)
