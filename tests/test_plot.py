# -*- coding: utf-8 -*-
from os import path
import tempfile
from genomics.plot import GridGenomePlot
from genomics.organism import genome_db


def test_basic_chart():
    ggp = GridGenomePlot(genome_db['Ag'], 2)
    with tempfile.TemporaryDirectory() as tmp:
        fname = '%s/test.png' % tmp
        ggp.fig.savefig(fname)
        assert path.isfile(fname)
