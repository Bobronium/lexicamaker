#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .context import lexicamaker
#from lexicamaker import dsl
from lexicamaker.tags import processDSLbodyline
from lexicamaker.tags import processDSLentry

def setup_function(function):
    """Provides info on the failed function."""
    print("Output from %s" % function)


def test_convert_simple_line():
    """Checks conversion of the simplest tags."""
    
    strIn1  = r"\[[u]'əup(ə)n[/u]\] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"
    strOut1 = "<div>\\[<u>'əup(ə)n</u>\\] <font color=\"green\">брит.</font> <b>1.</b> <i>прил.</i> открытый</div>"

    assert processDSLbodyline(strIn1) == (strOut1, '')


def test_convert_line_paragraps():
    """Checks conversion of the paragraph tags."""
    
    strIn1  = r"[m1]\[[u]'əup(ə)n[/u]\][/m] [m2] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"
    strOut1 = "<div class=\"m1\">\\[<u>'əup(ə)n</u>\\]</div> <div class=\"m2\"><div> <font color=\"green\">брит.</font> <b>1.</b> <i>прил.</i> открытый</div>"
    
    assert processDSLbodyline(strIn1) == (strOut1, '')

def test_convert_line_star():
    """Checks conversion of the hidden tags."""
    
    strIn1  = r"[m1]\[[u]'əup(ə)n[/u]\][/m] [m2] [*][c]брит.[/c] [b]1.[/b] [i]прил.[/i][/*] открытый"
    strOut1 = "<div class=\"m1\">\\[<u>'əup(ə)n</u>\\]</div> <div class=\"m2\"><div> <span d:priority=\"2\"><font color=\"green\">брит.</font> <b>1.</b> <i>прил.</i></span> открытый</div>"
    
    assert processDSLbodyline(strIn1) == (strOut1, '')

def test_convert_line_wswitches():
    """Checks conversion of the functional tags tags. In this particular case functions __parse_ex__ and __parse_lang__ are called. Note that they are not accessible directly."""
    
    strIn1  = "[m1]1) [i][trn][com]способ изготовления изображений[/com][/trn][/i][/m][m2][*][ex][lang name=\"English\"]photography[/lang] — фотография[/ex][/*][/m]"
    strOut1 = "<div id=\"photography\"  class=\"m1\">1) <i>способ изготовления изображений</i></div><div class=\"m2\"><span d:priority=\"2\">photography — фотография</span></div>"
    strOut2 = "<d:index d:value=\"photography\" d:anchor=\"xpointer(//*[@id=\'photography\'])\"/>"

    processDSLentry.__index_language__ = 'English'
    assert processDSLbodyline(strIn1) == (strOut1, strOut2)



def test_convert_entry_id():
    inStr1 = r"""please do not abandon me
abandonee
"""
    inStr2 = r"""\[[t]əˌbændə'niː[/t]\]
[p]сущ.[/p]
[m1]1) [p][trn]юр.[/p] лицо, в пользу которого имеет место отказ от права[/trn][/m]
[m1]2) [p][trn]мор.[/p] страховщик, в пользу которого остаётся застрахованный груз [i]или[/i] застрахованное судно в случае аварии[/trn][/m]
"""
    outStr0 = r"""<d:entry id="please_do_not_abandon_me">
<d:index d:value="please do not abandon me" d:title="please do not abandon me"/>
<d:index d:value="abandonee" d:title="abandonee"/>
<div>\[<span d:pr="1">əˌbændə'niː</span>\]</div>
<div>сущ.</div>
<div class="m1">1) юр. лицо, в пользу которого имеет место отказ от права</div>
<div class="m1">2) мор. страховщик, в пользу которого остаётся застрахованный груз <i>или</i> застрахованное судно в случае аварии</div>
</d:entry>
"""
    outStr00 = 'please_do_not_abandon_me'
    id, entry = processDSLentry(inStr1.splitlines(False), inStr2.splitlines(False))
    print (entry)
    #assert True
    assert id == outStr00
    assert entry == outStr0

    #def test_import_dict():
    #    lexicamaker.dsl.fix_attr()
    #    print(lexicamaker.dsl.processDSLstring.__indexing__)
#    assert False

def test_convert_entry_index():
    inStr1 = r"""open up
"""
    inStr2 = r"""[p]фраз. гл.[/p]
[m1]1) [trn]открыть [i][com](возможность)[/com][/i], предоставить [i][com](условия)[/com][/trn][/i][/m]
[m2][*][ex][lang id=1033]to open up opportunities[/lang] — предоставлять возможности[/ex][/*][/m]
[m1]2) [trn]открыться, разоткровенничаться[/trn][/m]
[m2][*][ex][lang id=1033]He was silent at first, but soon he opened up and told us about his terrible experiences.[/lang] — Сначала он молчал, но затем открылся и откровенно поведал нам о том, какие ужасы пришлось ему пережить.[/ex][/*][/m]
[m3] test [/m]
"""
    outStr0 = r"""<d:entry id="open_up">
<d:index d:value="open up" d:title="open up"/>
<d:index d:value="to open up opportunities" d:anchor="xpointer(//*[@id='to_open_up_opportunities'])"/>
<d:index d:value="He was silent at first, but soon he opened up and told us about his terrible experiences." d:anchor="xpointer(//*[@id='he_was_silent_at_first_c__but_soon_he_opened_up_and_told_us_about_his_terrible_experiences_d_'])"/>
<div>фраз. гл.</div>
<div class="m1">1) открыть <i>(возможность)</i>, предоставить <i>(условия)</i></div>
<div id="to_open_up_opportunities"  class="m2"><span d:priority="2">to open up opportunities — предоставлять возможности</span></div>
<div class="m1">2) открыться, разоткровенничаться</div>
<div id="he_was_silent_at_first_c__but_soon_he_opened_up_and_told_us_about_his_terrible_experiences_d_"  class="m2"><span d:priority="2">He was silent at first, but soon he opened up and told us about his terrible experiences. — Сначала он молчал, но затем открылся и откровенно поведал нам о том, какие ужасы пришлось ему пережить.</span></div>
<div class="m3"> test </div>
</d:entry>
"""
    outStr00 = 'open_up'
    processDSLentry.__index_language__ = 'English'
    id, entry = processDSLentry(inStr1.splitlines(False), inStr2.splitlines(False))
    print (entry)
    #assert False
    assert id == outStr00
    assert entry == outStr0
