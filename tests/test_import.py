#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .context import lexicamaker
#from lexicamaker import dsl
from lexicamaker.dsl import processDSLbodyline

def setup_function(function):
    """Provides info on the failed function."""
    print("Output from %s" % function)


def test_convert_simple_line():
    """Checks conversion of the simplest tags."""
    
    strIn1  = r"\[[u]'əup(ə)n[/u]\] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"
    strOut1 = "<div>\\[<u>'əup(ə)n</u>\\] <font color=\"green\">брит.</font> <b>1.</b> <i>прил.</i> открытый</div>"
    
    assert processDSLbodyline(strIn1) == (strOut1, '')
