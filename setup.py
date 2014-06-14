'''Setuptools based setup script for Python Genomics.

For the  installation just type the command:

python setup.py install

For more in-depth instructions, see the installation section of the
manual:

'''
from distutils.command.install import install
from setuptools import Command, find_packages, setup
import os

import sphinx


__version__ = None  # PEP 8
for line in open('genomics/__init__.py'):
    if (line.startswith('__version__ = ')):
        exec(line.strip())


class Sphinx(Command):
    user_options = []
    description = 'sphinx'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # metadata contains information supplied in setup()
        metadata = self.distribution.metadata
        src_dir = os.path.join(os.getcwd(),  'genomics')
        # Run sphinx by calling the main method, '--full' also adds a conf.py
        sphinx.apidoc.main(
            ['-H', metadata.name, '-A', metadata.author,
             '-V', metadata.version, '-R', metadata.version,
             '-o', os.path.join(['doc', 'api']), src_dir])
        # build the doc sources
        sphinx.main(['', 'doc'])


setup(
    name='pygenomics',
    version=__version__,
    author='Tiago Antao',
    author_email='tra@popgen.net',
    description=('A modern genomics library'),
    keywords = 'genomics genetics population-genetics population-genomics',
    url = 'http://github.com/tiagoantao/pygenomics',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Affero General Public License v3',
    ],
    cmdclass = {
        'install': install
    }
)

#TODO dependencies
