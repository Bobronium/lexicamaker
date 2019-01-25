#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .context import lexicamaker



def setup_function(function):
    """Provides info on the failed function."""
    print("Output from %s" % function)


def test_import1():
    """Checks import of the lexicamaker package."""
    assert lexicamaker.__version__!=None


def test_argparse1():
    """Checks import of the parser function and tests the simplest argument configuration.
        1) %(prog) testsource/TestDictionary.dsl
        2) %(prog) testsource/TestDictionary.dsl somedir"""
    from lexicamaker.__main__ import arguments_parser
    

    os.chdir(os.path.dirname(__file__))
    assert arguments_parser().parse_args(['path/file.dsl']).dslfile == 'path/file.dsl'
    #assert arguments_parser().parse_args(['path/file.dsl']).outdir == 'path/file'
    #assert arguments_parser().parse_args(['path/file.dsa']).outdir == 'path/file.dsa'
    assert arguments_parser().parse_args(['path/file.dsl', 'adir']).outdir == 'adir'
    #assert arguments_parser().parse_args(['path/file.dsa', 'adir']).outdir == 'adir/file.dsa'



def test_argparse2():
    """Checks import of the parser function and tests the simplest argument configuration.
        1) --version
        2) --help"""
    from lexicamaker.__main__ import arguments_parser
    
    try:
        arguments_parser().parse_args(['--version'])
    except SystemExit as se:
        print("\"--version\": detect raised SystemExit with code %d" % se.code)
        assert se.code==0
    try:
        arguments_parser().parse_args(['--help'])
    except SystemExit as se:
        print("\"--help\": detect raised SystemExit with code %d" % se.code)
        assert se.code==0


