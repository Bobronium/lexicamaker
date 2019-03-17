#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from .context import lexicamaker
#from lexicamaker import dsl
from lexicamaker.dsl import processDSLbodyline
from lexicamaker.dsl import indexDSLstring


def setup_function(function):
    """Provides info on the failed function."""
    print("Output from %s" % function)


def test_index():
    """Checks conversion of the simplest tags."""
    
    strIn1  = r"zero [ex] one [!trs] two [ex] three [/!trs] four [!trs] five [/ex] six [/!trs] seven [/ex] eight"
    strOut1 = r"zero [ex] one  four  seven [/ex] eight"
    print(strIn1)
    print(indexDSLstring(strIn1))
    assert strOut1 == indexDSLstring(strIn1)

