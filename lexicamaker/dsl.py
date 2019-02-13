#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def processDSLbodyline(myString):
    
    theString = myString
    DSLXMLdictionary = {
                        r'\[m\]'    : '<div>',
                        r'\[m(?P<indent>[0-9])\]': r'<div class="m\g<indent>">',
                        r'\[/m\]'   : '</div>',
                        r'\[b\]'    : '<b>', r'\[/b\]': '</b>',
                        r'\[i\]'    : '<i>', r'\[/i\]': '</i>',
                        r'\[u\]'    : '<u>', r'\[/u\]': '</u>',
                        r'\[c\]'    : '<font color="green">',
                        r'\[c (?P<color>[a-z]+)\]' : r'<font color="\g<color>">',
                        r'\[/c\]'   : '</font>',
                        r'\[sub\]'  : '<sub>', r'\[/sub\]': '</sub>',
                        r'\[sup\]'  : '<sup>', r'\[/sup\]': '</sup>',
                        r'\[\'\]'   : '', r'\[/\'\]'    : '\u0301',
                        r'\[p\]'    : '', r'\[/p\]'     : '',
                        r'\[trn\]'  : '', r'\[/trn\]'   : '',
                        r'\[ex\]'   : '', r'\[/ex\]'    : '',
                        r'\[com\]'  : '', r'\[/com\]'   : '',
                        r'\[t\]'    : '', r'\[/t\]'     : '',
                        r'\[s\]'    : '', r'\[/s\]'     : '',
                        r'\[!trs\]' : '', r'\[/!trs]'   : ''
                    }
    for tag in DSLXMLdictionary:
        myString = re.sub(tag, DSLXMLdictionary[tag], myString)

    myStringSplit = re.split(r'(<div(?: [^<>]+)*>|</div>)',myString)
    if len(myStringSplit) == 1:
        myString = '<div>' + myString + '</div>'
    else:
        for i in [0,-1]:
            if myStringSplit[i]:
                myStringSplit[i] = '<div>' + myStringSplit[i] + '</div>'
        myString = ''.join(myStringSplit)
    return myString

#def __parse_c__(myString):
#    if myString == None:
#        return "<font color=\"green\">"
#    else:
#        return "<font color=\"\\g<" + myString + ">\">"

#theDSLbodyline = r"[c]\[[u]'əup(ə)n[/u]\][/c] [c blue]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"

#theDSLbodyline = r"[m1]\[[u]'əup(ə)n[/u]\][/m] [m2] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"

#theDSLbodyline = r"[c]брит.[/c]"

#myString = processDSLbodyline(theDSLbodyline)

#print(myString)
