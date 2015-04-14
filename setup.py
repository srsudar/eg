try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Examples at the command line',
    'author': 'Sam Sudar',
    'url': 'https://github.com/srsudar/eg',
    'author_email': 'sudar.sam@gmail.com',
    'version': '0.0.1',
    'install_requires': [
        'colorama'
    ],
    'packages': [
        'eg'
    ],
    'scripts': [],
    'name': 'eg'
}

setup(**config)
