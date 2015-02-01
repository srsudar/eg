try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Helpful examples for command-line tools',
    'author': 'Sam Sudar',
    'url': 'https://github.com/srsudar/eg',
    'download_url': 'https://github.com/srsudar/eg',
    'version': '0.1',
    'install_requires': ['mock', 'os', 'sys'],
    'name': 'eg'
}

setup(**config)
