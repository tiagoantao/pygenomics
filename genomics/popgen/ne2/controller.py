'''
.. module: controller
   :synopsis: This module allows to control NeEstimator2
   :copyright: Copyright 2014 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>
'''

__docformat__ = "javadoc en"  # This has to change


import os
import sys


class NeEstimator2Controller(object):
    def __init__(self, ne2_dir=None):
        '''Initializes the controller for NeEstimator2.

        The initializer checks for existance and executability of binaries.

        @param ne2_dir is the directory where NeEstimator2 is. If empty
                       the system will try to find the binary on the PATH.

        '''
        self.platform = sys.platform
        if self.platform == 'win32':
            self.bin_name = 'Ne2.exe'
        elif self.platform == "darwin":  # Mac missing
            self.bin_name = 'Ne2M'
        else:
            self.bin_name = 'Ne2L'
        if ne2_dir:
            self.ne2_dir = ne2_dir
        else:
            for myDir in os.environ["PATH"].split(os.pathsep):
                if self.bin_name in os.listdir(myDir) and os.access(
                    myDir + os.sep + self.bin_name, os.X_OK
                ) and os.path.isfile(myDir + os.sep + self.bin_name):
                    self.ne2_dir = myDir
                    break
        dir_contents = os.listdir(self.ne2_dir)
        if self.bin_name in dir_contents:
            if not os.access(self.ne2_dir + os.sep +
                             self.bin_name, os.X_OK):
                raise IOError("NeEstimator2 not executable")
        else:
            raise IOError("NeEstimator2 not available")

    def run(self, in_dir, gen_file, out_dir, out_file,
            crits=None, LD=True, hets=False, coanc=False, temp=None,
            monogamy=False, options=None):
        '''Executes NeEstimator2.

        Args:
            in_dir: The input directory
            gen_file The genepop file
            out_dir: The output directory
            out_file Where the output will be stored
            LD: Do LD method
            hets: Do excessive heterozygosity
            coanc: Do Molecular coancestry
            temp: List of generations for the temporal method (None = Not do)

        XXX document options

        '''
        crits = crits or []
        options = options or {}
        in_name = 'in.le' + str(os.getpid())
        inf = open(in_name, 'w')
        val = 0
        if LD:
            val += 1
        if hets:
            val += 2
        if coanc:
            val += 4
        if temp is not None:
            val += 8
        inf.write("%d 0\n" % val)
        inf.write("%s/\n" % in_dir)
        inf.write("%s\n" % gen_file)
        inf.write("2\n")  # Genepop
        inf.write("%s/\n" % out_dir)
        inf.write("%s\n" % out_file)
        inf.write("%d\n" % len(crits))
        if len(crits) == 0:
            inf.write("\n")
        else:
            inf.write("%s -1\n" % " ".join([str(x) for x in crits]))
        inf.write("%d\n" % (1 if monogamy else 0))  # Random mating
        if temp:
            # Plan II only for now (and single pop only)
            inf.write("0 %s\n" % " ".join(map(lambda x: str(x), temp[0])))
        inf.close()
        if len(options) == 0:
            opt_txt = ''
        else:
            opt_name = 'opt.le' + str(os.getpid())
            opt_txt = ' o:' + opt_name
            opf = open(opt_name, 'w')
            opf.write('0 0\n')
            opf.write('0\n')
            opf.write('0\n')
            opf.write('%s\n' % options.get('burrows', '0'))
            opf.write('1\n')
            opf.write('1\n')
            opf.write('0\n')
            opf.write('0\n')
            opf.close()
        os.system(self.ne2_dir + os.sep + self.bin_name +
                  ' i:' + in_name + opt_txt + ' >' + os.devnull + ' 2>&1')
        os.remove(in_name)
        if len(options) > 0:
            os.remove(opt_name)
