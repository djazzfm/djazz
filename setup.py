#!/usr/bin/env python

try:
    from setuptools import setup
    setuptools = True
except ImportError:
    from distutils.core import setup
    setuptools = True

params = {'name': 'djazz',
          'version': '0.1',
          'description': 'Django extension tools',
          'author': 'Guillaume Dugas',
          'author_email': 'dugas.guillaume@gmail.com',
          'url': 'https://github.com/djazzproject/djazz',
          'packages': ['djazz', 'djazz.formatters']
          }

if setuptools:
    params['install_requires'] = ['django>=1.7']

setup(**params)
