try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Also bump at eg.eg_util.VERSION
VERSION = '1.0.0'

LONG_DESCRIPTION = """
eg provides examples at the command line.

Many commands can be difficult to remember. Man pages work great, but can
provide too much information to be useful at a glance. You'll likely still have
to turn to the internet for some examples.

eg tries to minimize that need by providing useful examples at the command line.
`eg find` will give you useful examples of the find command right in the
terminal.

eg is extensible. If you have a particular command you like to use (like a
specific use of awk, resetting a home server, etc) you can add these to a custom
directory and eg will show you those results first when you type the relevant
command.

eg is colorful. By default eg uses colors. This is pretty. You can customize
these colors to whatever scheme you want.

See the webpage for more information.
"""

# The version here must match the version in the code itself. Currently they
# have to be updated in both places.
config = {
    'name': 'eg',
    'description': 'Examples at the command line',
    'long_description': LONG_DESCRIPTION,
    'author': 'Sam Sudar',
    'url': 'https://github.com/srsudar/eg',
    'license': 'MIT',
    'author_email': 'sudar.sam@gmail.com',
    'version': VERSION,
    'install_requires': [],
    'test_requires': ['nose', 'mock'],
    'packages': ['eg'],
    'scripts': ['bin/eg'],
    'package_data': {
        'eg': ['examples/*']
    },
    'zip_safe': False,
    'test_suite': 'nose.collector'
}

setup(**config)
