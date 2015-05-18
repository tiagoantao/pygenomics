# -*- coding: utf-8 -*-


def test_basic_chart():
    from os import path
    import tempfile
    import matplotlib
    matplotlib.use('Agg')
    from genomics.plot import GridGenomePlot
    from genomics.organism import genome_db
    ggp = GridGenomePlot(genome_db['Ag'], 2)
    with tempfile.TemporaryDirectory() as tmp:
        fname = '%s/test.png' % tmp
        ggp.fig.savefig(fname)
        assert path.isfile(fname)
