#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='lexicamaker',
  version='0.1.2',
  description='DSL to Apple Dictionary Service converter',
  url='http://github.com/lnxk/adsmaker',
  author='Svintuss; Lnxk',
  author_email='svintuss@gmail.com',
  license='MIT',
  packages=['lexicamaker'],
  zip_safe=True,
  entry_points = {
    'console_scripts': ['adsmaker=lexicamaker.__main__:main'],
  }
  )
