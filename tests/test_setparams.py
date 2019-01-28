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
    from lexicamaker.__main__ import IOBridge
    

    os.chdir(os.path.dirname(__file__))

    args = IOBridge()
    assert args.parser.parse_args(['path/file.dsl']).dictionaryFile == 'path/file.dsl'
    assert args.parser.parse_args(['path/file.dsl']).outputDictionaryPath == os.getcwd()
    #assert args.parser.parse_args(['path/file.dsl']).outputDictionaryPath == 'path/file.dsa'
    assert args.parser.parse_args(['path/file.dsl', 'adir']).outputDictionaryPath == 'adir'
    #assert args.parser.parse_args(['path/file.dsa', 'adir']).outputDictionaryPath == 'adir/file.dsa'



def test_argparse2():
    """Checks import of the parser function and tests the simplest argument configuration.
        1) --version
        2) --help"""
    from lexicamaker.__main__ import IOBridge
    
    args = IOBridge()
    
    try:
        args.parser.parse_args(['--version'])
    except SystemExit as se:
        print("\"--version\": detect raised SystemExit with code %d" % se.code)
        assert se.code==0
    try:
        args.parser.parse_args(['--help'])
    except SystemExit as se:
        print("\"--help\": detect raised SystemExit with code %d" % se.code)
        assert se.code==0


