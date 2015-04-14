try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Also bump at eg.eg_util.VERSION
VERSION = '0.0.1'

# The version here must match the version in the code itself. Currently they
# have to be updated in both places.
config = {
    'name': 'eg',
    'description': 'Examples at the command line',
    'author': 'Sam Sudar',
    'url': 'https://github.com/srsudar/eg',
    'author_email': 'sudar.sam@gmail.com',
    'version': VERSION,
    'install_requires': ['colorama'],
    'packages': ['eg'],
    'scripts': ['eg/eg.py'],
    'data_files': ['eg/data/*']
}

setup(**config)
