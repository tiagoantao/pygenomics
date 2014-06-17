# -*- coding: utf-8 -*-
'''
.. module:: genomics.mapreduce
   :synopsis: MapReduce framework
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import sys
from . import do_map

if __name__ == "__main__":
    do_map(sys.argv[1])
