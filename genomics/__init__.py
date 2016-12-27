# -*- coding: utf-8 -*-
'''
.. module:: genomics
   :synopsis: A library for modern population genomics analysis
   :noindex:
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
from . import config
from .parallel import executor

__version__ = '0.1.4'


class GenomicsException(Exception):
    '''A general exception for the library'''

# Loading the configuration
cfg = config.Config()
cfg.load_config()
# Configuring the executor
if cfg.grid == 'Local':
    lexec = executor.Local(cfg.grid_limit)
else:
    raise GenomicsException('Grid %s unknown' % cfg.grid)
