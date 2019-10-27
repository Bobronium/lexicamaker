#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from .context import lexicamaker
#from lexicamaker import dsl
from lexicamaker.dsl import processDSLbodyline


def setup_function(function):
    """Provides info on the failed function."""
    print("Output from %s" % function)



def test_import_path_template():
    """Checks conversion of the simplest tags."""
    
    
    from lexicamaker.__main__ import for_test
    
    assert for_test() == os.path.realpath(os.path.join(os.path.dirname(__file__), '../template/Makefile'))
