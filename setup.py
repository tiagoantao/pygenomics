'''Setuptools based setup script for Python Genomics.

For the  installation just type the command:

python setup.py install

For more in-depth instructions, see the installation section of the
manual:

'''
from distutils.command.install import install
from setuptools import find_packages, setup

__version__ = None  # PEP 8
for line in open('genomics/__init__.py'):
    if (line.startswith('__version__ = ')):
        exec(line.strip())


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
    cmdclass={
        'install': install,
    },
)

#TODO dependencies
