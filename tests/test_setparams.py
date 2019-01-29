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
        1) --version
        2) --help"""
    from lexicamaker.__main__ import IOBridge
    
    args = IOBridge()
    
    try:
        args.parse_args(['--version'])
    except SystemExit as se:
        print("\"--version\": detect raised SystemExit with code %d" % se.code)
        assert se.code==0
    try:
        args.parse_args(['--help'])
    except SystemExit as se:
        print("\"--help\": detect raised SystemExit with code %d" % se.code)
        assert se.code==0


def test_argparse2():
    """Checks import of the parser function and tests the simplest argument configuration.
        1) parse arguments from constructor
        2) parse arguments from IOBridge::__init__
        3) parse arguments from ArgumentParser::parse_args
        4) parse arguments from IOBridge::parse_args
        5) parse arguments direct from IOBridge after parse_args
        6) forward arguments to abstract class C using ArgumentParser::namespace
        """
    from lexicamaker.__main__ import IOBridge
    
    args = IOBridge(['path/file.dsl'])
    assert args.dictionaryFile == 'path/file.dsl'
    
    assert args.parser.parse_args(['path2/file2.dsl']).dictionaryFile == 'path2/file2.dsl'
    
    assert args.parse_args(['path3/file3.dsl']).dictionaryFile == 'path3/file3.dsl'
    
    args.parse_args(['path4/file4.dsl'])
    assert args.dictionaryFile == 'path4/file4.dsl'
    
    class C:
        pass
    c = C()
    argsc = IOBridge(args=['path5/file5.dsl'], namespace=c)
    assert c.dictionaryFile == 'path5/file5.dsl'
    assert not hasattr(argsc, 'dictionaryFile')


def test_argparse3():
    """Checks import of the parser function and tests the simplest argument configuration.
        1) %(prog) PATH/file.dsl and get outputDictionaryPath as PATH
        2) %(prog) PATH/file.dsl ADIR get outputDictionaryPath as ADIR"""
    from lexicamaker.__main__ import IOBridge
    
    #os.chdir(os.path.dirname(__file__))
    
    args = IOBridge(['path/file.dsl'])
    assert args.outputDictionaryPath == os.getcwd()
    #assert args.parser.parse_args(['path/file.dsl']).outputDictionaryPath == 'path/file.dsa'
    
    args.parse_args(['path/file.dsl', 'adir'])
    assert args.outputDictionaryPath == 'adir'
    #assert args.parser.parse_args(['path/file.dsa', 'adir']).outputDictionaryPath == 'adir/file.dsa'


def test_argparse4():
    """Checks import of the parser function and tests the simplest argument configuration.
        1) abbreviations and annotation are automatically found
        2) abbreviations and annotation are explicitly given
        3) parse arguments from ArgumentParser::parse_args
        4) parse arguments from IOBridge::parse_args
        5) parse arguments direct from IOBridge after parse_args
        6) forward arguments to abstract class C using ArgumentParser::namespace
        """
    os.chdir(os.path.dirname(__file__))
    
    from lexicamaker.__main__ import IOBridge

    args = IOBridge(['--remote', 'test_setparams_data/dict1.dsl'])
    args.open_files()
    
    assert args.outputDictionaryPath == 'test_setparams_data/dict1'
    assert args.dictionaryName == 'dict1'
    assert args.dictionaryFile.name == 'test_setparams_data/dict1.dsl'
    assert args.annotationFile.name == 'test_setparams_data/dict1.ann'
    assert args.abbreviationsFile.name == 'test_setparams_data/dict1_abrv.dsl'

    args.parse_args(['--no-annotation', '--no-abbreviations', 'test_setparams_data/dict1.dsl'])
    args.open_files()
    assert args.dictionaryFile.name == 'test_setparams_data/dict1.dsl'
    assert args.annotationFile == False
    assert args.abbreviationsFile == False
    
    args.parse_args(['--annotation', 'test_setparams_data/dict1.ann', '--abbreviations', 'test_setparams_data/dict1_abrv.dsl', 'test_setparams_data/dict2.dsl'])
    args.open_files()
    assert args.dictionaryFile.name == 'test_setparams_data/dict2.dsl'
    assert args.annotationFile.name == 'test_setparams_data/dict1.ann'
    assert args.abbreviationsFile.name == 'test_setparams_data/dict1_abrv.dsl'

    args = IOBridge(['--remote', 'test_setparams_data/dict3.dsx'])
    args.open_files()
    assert args.outputDictionaryPath == 'test_setparams_data/dict3.dsx'
    assert args.dictionaryName == 'dict3.dsx'
    assert args.dictionaryFile.name == 'test_setparams_data/dict3.dsx'
