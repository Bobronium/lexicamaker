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
    
    #strIn1  = r"[test] zero [ex] one [!trs] two [/!trs] three [/ex] four [ex x=qwe] five [!trs] six [/!trs] seven [/ex] eight"
    #strOut1 = r"zero [ex] one  four  seven [/ex] eight"
    #print(strIn1)
    strIn1  = "zero [test] one [ex] two[/ex] three [ex][lang name=\"Russian\"]транскрипция[/lang] transcription[/ex] four [qwe] five [ex] six"
    listOut1 = [" two", "transcription", " six"]


    res = indexDSLstring(strIn1)
    assert False
#assert indexDSLstring(strIn1) == listOut1

