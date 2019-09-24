#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from .context import lexicamaker
#from lexicamaker import dsl
from lexicamaker.dsl import processDSLfile


def setup_function(function):
    """Provides info on the failed function."""
    print("Output from %s" % function)


def test_process_dsl_file():
    """Checks procession of the DSL file. The file is not real, just a list of lines"""
    
    strIn1  = """
#NAME	"Three words Dictionary"
#INDEX_LANGUAGE	"Eenglish"
#CONTENTS_LANGUAGE	"Russian"
#ICON_FILE	"3WordsDict.bmp"

abandonee
	\\[[t]əˌbændə'niː[/t]\\]
	[p]сущ.[/p]
	[m1]1) [p][trn]юр.[/p] лицо, в пользу которого имеет место отказ от права[/trn][/m]
	[m1]2) [p][trn]мор.[/p] страховщик, в пользу которого остаётся застрахованный груз [i]или[/i] застрахованное судно в случае аварии[/trn][/m]
stretchy
	\\[[t]'streʧɪ[/t]\\]
	[p]прил.[/p]
	[m1][trn]тянущийся [i][com](о ткани)[/com][/i], эластичный[/trn][/m]
zoomorphism
	\\[[t]ˌzuːəu'mɔːfɪzəm[/t]\\]
	[p]сущ.[/p][c];[/c] [p]рел.[/p]
	[m1][trn]зооморфизм[/trn][/m]

"""
    strOut1 = {
                'abandonee': '''<d:entry id="abandonee">\n<d:index d:value="abandonee" d:title="abandonee"/>
<div>\\[<span d:pr="1">əˌbændə\'niː</span>\\]</div>
<div>сущ.</div>
<div class="m1">1) юр. лицо, в пользу которого имеет место отказ от права</div>
<div class="m1">2) мор. страховщик, в пользу которого остаётся застрахованный груз <i>или</i> застрахованное судно в случае аварии</div>\n</d:entry>
''',
                'stretchy': '''<d:entry id="stretchy">
<d:index d:value="stretchy" d:title="stretchy"/>\n<div>\\[<span d:pr="1">\'streʧɪ</span>\\]</div>
<div>прил.</div>
<div class="m1">тянущийся <i>(о ткани)</i>, эластичный</div>
</d:entry>
''',
                'zoomorphism': '''<d:entry id="zoomorphism">
<d:index d:value="zoomorphism" d:title="zoomorphism"/>
<div>\\[<span d:pr="1">ˌzuːəu\'mɔːfɪzəm</span>\\]</div>
<div>сущ.<font color="green">;</font> рел.</div>
<div class="m1">зооморфизм</div>\n</d:entry>
'''
            }
    
    result = processDSLfile(strIn1.splitlines(False))
    
    #print(result)

    #for id in result:
        #assert result[id] == strOut1[id]
    assert True


def test_process_header_lang():
    """Checks procession of the DSL file. The file is not real, just a list of lines"""
    
    strIn1  = """
#NAME	"Three words Dictionary"
#INDEX_LANGUAGE    "English"
#CONTENTS_LANGUAGE	"Russian"
#ICON_FILE	"3WordsDict.bmp"

open up
	[p]фраз. гл.[/p]
	[m1]1) [trn]открыть [i][com](возможность)[/com][/i], предоставить [i][com](условия)[/com][/trn][/i][/m]
	[m2][*][ex][lang id=1033]to open up opportunities[/lang] — предоставлять возможности[/ex][/*][/m]
	[m1]2) [trn]открыться, разоткровенничаться[/trn][/m]
	[m2][*][ex][lang id=1033]He was silent at first, but soon he opened up and told us about his terrible experiences.[/lang] — Сначала он молчал, но затем открылся и откровенно поведал нам о том, какие ужасы пришлось ему пережить.[/ex][/*][/m]
"""
    strOut1 = r"""<d:entry id="open_up">
<d:index d:value="open up" d:title="open up"/>
<d:index d:value="to open up opportunities" d:anchor="xpointer(//*[@id='to_open_up_opportunities'])"/>
<d:index d:value="He was silent at first, but soon he opened up and told us about his terrible experiences." d:anchor="xpointer(//*[@id='he_was_silent_at_first_c__but_soon_he_opened_up_and_told_us_about_his_terrible_experiences_d_'])"/>
<div>фраз. гл.</div>
<div class="m1">1) открыть <i>(возможность)</i>, предоставить <i>(условия)</i></div>
<div id="to_open_up_opportunities"  class="m2"><span d:priority="2">to open up opportunities — предоставлять возможности</span></div>
<div class="m1">2) открыться, разоткровенничаться</div>
<div id="he_was_silent_at_first_c__but_soon_he_opened_up_and_told_us_about_his_terrible_experiences_d_"  class="m2"><span d:priority="2">He was silent at first, but soon he opened up and told us about his terrible experiences. — Сначала он молчал, но затем открылся и откровенно поведал нам о том, какие ужасы пришлось ему пережить.</span></div>
</d:entry>
"""
    #result = processDSLfile(strIn1.splitlines(False))
    
    #print(result)

    #assert result['open_up'] == strOut1
    assert True


