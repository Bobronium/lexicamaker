#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

# fix the automatic versioning with __version__ from __init__.py

setup(name='lexicamaker',
  version='0.1.2',
  description='DSL to Apple Dictionary Service converter',
  long_description='The program takes DICT.dsl file, looks for abbreviations DICT_abrv.dsl and annotation DICT.ann and produces the a folder for Apple Dictionary Services, which has to be compiled with Dictinary Developer Kit to get the DICT.dictionary package, which one can install in ~/Library/Dictionaries/',
  classifiers=[
                   'Development Status :: 2 - Pre-Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Text Processing :: Linguistic',
                   ],
  keywords='dsl apple dictionary',
  url='http://github.com/lnxk/adsmaker',
  author='Svintuss',
  author_email='svintuss@gmail.com',
  license='MIT',
  packages=['lexicamaker'],
  zip_safe=True,
  include_package_data=True,
  entry_points = {
    'console_scripts': ['adsmaker=lexicamaker.__main__:main'],
  }
  )
