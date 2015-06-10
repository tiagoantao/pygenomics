# -*- coding: utf-8 -*-

import six


def test_basic_chart():
    if six.PY2:
        return
    from os import path
    import tempfile
    import matplotlib.pyplot as plt
    plt.switch_backend('Agg')
    from genomics.plot import GridGenomePlot
    from genomics.organism import genome_db
    ggp = GridGenomePlot(genome_db['Ag'], 2)
    with tempfile.TemporaryDirectory() as tmp:
        fname = '%s/test.png' % tmp
        ggp.fig.savefig(fname)
        assert path.isfile(fname)
