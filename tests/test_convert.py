#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .context import lexicamaker
#from lexicamaker.dsl import *
from lexicamaker.dsl import processDSLbodyline
from lexicamaker.dsl import processDSLentry

def setup_function(function):
    """Provides info on the failed function."""
    print("Output from %s" % function)


def test_convert_simple_line():
    """Checks conversion of the simplest tags."""
    
    strIn1  = r"\[[u]'əup(ə)n[/u]\] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"
    strOut1 = "\\[<u>'əup(ə)n</u>\\] <font color=\"green\">брит.</font> <b>1.</b> <i>прил.</i> открытый"
    
    assert processDSLbodyline(strIn1) == strOut1


def test_convert_line_paragraps():
    """Checks conversion of the paragraph tags."""
    
    strIn1  = r"[m1]\[[u]'əup(ə)n[/u]\][/m] [m2] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"
    strOut1 = "<div class=\"m1\">\\[<u>'əup(ə)n</u>\\]</div> <div class=\"m2\"><div> <font color=\"green\">брит.</font> <b>1.</b> <i>прил.</i> открытый</div>"
    
    assert processDSLbodyline(strIn1) == strOut1

def test_convert_line_star():
    """Checks conversion of the hidden tags."""
    
    strIn1  = r"[m1]\[[u]'əup(ə)n[/u]\][/m] [m2] [*][c]брит.[/c] [b]1.[/b] [i]прил.[/i][/*] открытый"
    strOut1 = "<div class=\"m1\">\\[<u>'əup(ə)n</u>\\]</div> <div class=\"m2\"><div> <span d:priority=\"2\"><font color=\"green\">брит.</font> <b>1.</b> <i>прил.</i></span> открытый</div>"
    
    assert processDSLbodyline(strIn1) == strOut1

def test_convert_line_wswitches():
    """Checks conversion of the functional tags tags. In this particular case functions __parse_ex__ and __parse_lang__ are called. Note that they are not accessible directly."""
    
    strIn1  = "[m1]1) [i][trn][com]способ изготовления изображений[/com][/trn][/i][/m][m2][*][ex][lang name=\"English\"]photography[/lang] — фотография[/ex][/*][/m]"
    strOut1 = "<div id=\"photography\"  class=\"m1\">1) <i>способ изготовления изображений</i></div><div class=\"m2\"><span d:priority=\"2\">photography — фотография</span></div>"
    
    assert processDSLbodyline(strIn1) == strOut1



def test_convert_entry():
    inStr1 = r"""please, do not abandon me!
abandonee
"""
    inStr2 = r"""\[[t]əˌbændə'niː[/t]\]
[p]сущ.[/p]
[m1]1) [p][trn]юр.[/p] лицо, в пользу которого имеет место отказ от права[/trn][/m]
[m1]2) [p][trn]мор.[/p] страховщик, в пользу которого остаётся застрахованный груз [i]или[/i] застрахованное судно в случае аварии[/trn][/m]
"""
    outStr0 = r"""<d:entry id="please__do_not_abandon_me_">
<d:index d:value="please, do not abandon me!" d:title="please, do not abandon me!"/>
<d:index d:value="abandonee" d:title="abandonee"/>
\[<span d:pr="1">əˌbændə'niː</span>\]
сущ.
<div class="m1">1) юр. лицо, в пользу которого имеет место отказ от права</div>
<div class="m1">2) мор. страховщик, в пользу которого остаётся застрахованный груз <i>или</i> застрахованное судно в случае аварии</div>
</d:entry>
"""
    outStr00 = 'please__do_not_abandon_me_'
    id, entry = processDSLentry(inStr1.splitlines(False), inStr2.splitlines(False))
    
    assert id == outStr00
    assert entry == outStr0

    #def test_import_dict():
    #    lexicamaker.dsl.fix_attr()
    #    print(lexicamaker.dsl.processDSLstring.__indexing__)
#    assert False
