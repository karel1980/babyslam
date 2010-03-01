import glob, sys, os

from types import StringType
from distutils.command.install_data import install_data
from distutils.core import setup
from distutils.util import change_root, convert_path

filtered_data_files=[('/etc', [ 'src/etc/babyslam.xml' ])]

"""
  Replacement for install_data.
     - data_files are copied as usual
     - filtered_data_files are copied, and subsequently their contents undergo the following replacements:
          @@@install_dir@@@ -> self.install_dir

       (the keyword can't be escaped)
"""
class FilterInstallData(install_data):
    """Specialized install_data."""
    def __init__(self, alpha):
        install_data.__init__(self, alpha)
        pass

    def initialize_options(self):
        install_data.initialize_options(self)

    def run(self):
        global filtered_data_files

        self.mkpath(self.install_dir)
        outfiles = []
        self.process_files(self.data_files, outfiles)
        self.outfiles += outfiles

        outfiles = []
        self.process_files(filtered_data_files, outfiles)
        self.outfiles += outfiles
        for x in outfiles:
            lines = [ line.replace('@@@install_dir@@@', self.install_dir) for line in open(x, 'r').readlines() ]
            open(x, 'w').writelines(lines)

    def process_files(self, data_files, outfiles):
        for f in data_files:
            if type(f) is StringType:
                # it's a simple file, so copy it
                f = convert_path(f)
                if self.warn_dir:
                    self.warn("setup script did not provide a directory for "
                              "'%s' -- installing right in '%s'" %
                              (f, self.install_dir))
                (out, _) = self.copy_file(f, self.install_dir)
                outfiles.append(out)
            else:
                # it's a tuple with path to install to and a list of files
                dir = convert_path(f[0])
                if not os.path.isabs(dir):
                    dir = os.path.join(self.install_dir, dir)
                elif self.root:
                    dir = change_root(self.root, dir)
                self.mkpath(dir)

                if f[1] == []:
                    # If there are no files listed, the user must be
                    # trying to create an empty directory, so add the
                    # directory to the list of output files.
                    outfiles.append(dir)
                else:
                    # Copy files, adding them to the list of output files.
                    for data in f[1]:
                        data = convert_path(data)
                        (out, _) = self.copy_file(data, dir)
                        outfiles.append(out)

setup(name='babyslam',
  version='1.0',
  description='Entertains babies while protecting your computer',
  author='Karel Vervaeke',
  author_email='karel.vervaeke@telenet.be',
  url='http://github.com/karel1980/babyslam',
  cmdclass={'install_data': FilterInstallData},
  packages=['babyslam'],
  package_dir={'babyslam': 'src/modules/babyslam'},
  #package_data={'babyslam': ['media/*']},
  scripts=['src/scripts/babyslam'],
  data_files=[('share/babyslam/media', glob.glob('src/media/*'))]
  )
