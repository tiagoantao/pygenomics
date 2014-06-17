# -*- coding: utf-8 -*-
'''
.. module:: genomics.mapreduce
   :synopsis: MapReduce framework
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import pickle
import tempfile

import genomics

mr_dir = genomics.cfg.mr_dir


def pickle_in(datum):
    w, fname = tempfile.mkstemp(dir=mr_dir)
    pickle.dump(datum, w)
    w.close()
    return fname
