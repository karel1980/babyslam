from distutils.core import setup
setup(name='babyslam',
  version='1.0',
  description='Entertains babies while protecting your computer',
  author='Karel Vervaeke',
  author_email='karel.vervaeke@telenet.be',
  url='http://github.com/karel1980/babyslam',
  packages=['babyslam'],
  package_dir={'babyslam': 'src/modules/babyslam'},
  package_data={'babyslam': ['media/*']},
  scripts=['src/scripts/babyslam'],
  )
