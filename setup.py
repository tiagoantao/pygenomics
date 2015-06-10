'''Setuptools based setup script for Python Genomics.

For the  installation just type the command:

python setup.py install

For more in-depth instructions, see the installation section of the
manual:

'''
from setuptools import Command, find_packages, setup
import os

__version__ = None  # PEP 8
for line in open('genomics/__init__.py'):
    if (line.startswith('__version__ = ')):
        exec(line.strip())


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


class Sphinx(Command):
    user_options = []
    description = 'build sphinx documentation'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # metadata contains information supplied in setup()
        metadata = self.distribution.metadata
        src_dir = os.path.join(os.getcwd(),  'genomics')
        # Run sphinx by calling the main method, '--full' also adds a conf.py
        from sphinx import apidoc
        apidoc.main(
            ['', '-f', '-H', 'Python Genomics', '-A', metadata.author,
             '-V', metadata.version, '-R', metadata.version,
             '-o', os.path.join('doc', 'api'), src_dir])
        # build the doc sources
        os.chdir('doc')
        os.system('make html')
        os.chdir('..')


setup(
    name='pygenomics',
    version=__version__,
    author='Tiago Antao',
    author_email='tra@popgen.net',
    description=('A modern genomics library'),
    keywords='genomics genetics population-genetics population-genomics',
    url='http://github.com/tiagoantao/pygenomics',
    license='AGPLv3',
    packages=find_packages(),
    py_modules=['genomics'],
    install_requires=['six', 'enum34', 'setuptools'],
    classifiers=[
        'Development Status :: 3 - Alpha',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
    ],
    cmdclass={
        'doc': Sphinx,
        'test': PyTest
    },
)

#TODO dependencies
