#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def processDSLbodyline(myString):
    """ Processing the line by substitution of every known tag by xml tag and wrapping free parts as paragraphs. """
    theString = myString
    DSLXMLdictionary = {
                        r'\[m\]'    : '<div>',
                        r'\[m(?P<indent>[0-9])\]': r'<div class="m\g<indent>">',
                        r'\[/m\]'   : '</div>',
                        r'\[br\]'    : '<br />',
                        r'\[\*\]'   : '<span d:priority="2">',
                        r'\[/\*\]'  : '</span>',
                        r'\[b\]'    : '<b>', r'\[/b\]': '</b>',
                        r'\[i\]'    : '<i>', r'\[/i\]': '</i>',
                        r'\[u\]'    : '<u>', r'\[/u\]': '</u>',
                        r'\[c\]'                   : '<font color="green">',
                        r'\[c (?P<color>[a-z]+)\]' : r'<font color="\g<color>">',
                        r'\[/c\]'                  : r'</font>',
                        r'\[sub\]'  : '<sub>', r'\[/sub\]': '</sub>',
                        r'\[sup\]'  : '<sup>', r'\[/sup\]': '</sup>',
                        r'\[\'\]'   : '', r'\[/\'\]'    : '\u0301',
                        r'\[lang\]'                          : '',
                        r'\[lang name="(?P<lname>[a-z]+)"\]' : '',
                        r'\[lang id="(?P<lid>[a-z]+)"\]'     : '',
                        r'\[/lang\]'                         : '',
                        r'\[trn\]'  : '', r'\[/trn\]'   : '',
                        r'\[ex\]'   : '', r'\[/ex\]'    : '',
                        r'\[com\]'  : '', r'\[/com\]'   : '',
                        r'\[!trs\]' : '', r'\[/!trs]'   : '',
                        r'\[p\]'    : '', r'\[/p\]'     : '',
                        r'\[t\]'    : '<span d:pr="1">',
                        r'\[/t\]'   : '</span>',
                        r'\[s\]'    : '', r'\[/s\]'     : '',
                        r'<<'       : '', r'>>'         : '',
                        r'\[ref\]'  : '', r'\[/ref\]'   : '',
                        r'\[url\]'  : '', r'\[/url\]'   : ''
                    }

    # Simply substitute every tag in the line
    for tag in DSLXMLdictionary:
        myString = re.sub(tag, DSLXMLdictionary[tag], myString)

    # Make sure that the line is treated as a paragraph. Either the whole line is in <div>,
    # or if there is any new paragraph <div>s in the line, wrap the free beginning and ending
    # of the line in <div>s
    myStringSplit = re.split(r'(<div(?: [^<>]+)*>|</div>)',myString)
    if len(myStringSplit) == 1:
        myString = '<div>' + myString + '</div>'
    else:
        for i in [0,-1]:
            if myStringSplit[i]:
                myStringSplit[i] = '<div>' + myStringSplit[i] + '</div>'
        myString = ''.join(myStringSplit)

    # return resulting line
    return myString

def processDSLentryhead(entryhead):
    head = ''
    for line in entryhead:
        head = head + '<d:index d:value="' + line + '" d:title="' + line + '"/>\n'
    id = re.sub('[^a-z0-9]', '_', entryhead[0].lower())
    return [id, head]

def processDSLentrybody(entrybody):
    body = ''
    for line in entrybody:
        body = body + processDSLbodyline(line) + '\n'
    return body

def processDSLentry(entryhead, entrybody):
    id, head = processDSLentryhead(entryhead)
    body = processDSLentrybody(entrybody)
    entry = '<d:entry id="' + id + '">\n' + head + body + '</d:entry>\n'
    return [id, entry]

def processDSLfile(dslFile):
    entryhead = []
    entrybody = []
    isSameEntry = None
    for line in dslFile:
        # remove newline sequence in the end of the string
        line = line.rstrip()
        # remove comments
        line = re.sub('{{.*?}}', '', line)
        # skip empty lines
        if re.fullmatch(r'\s*', line):
            pass
        # skip lines starting from hash # symbol
        elif re.match(r'#', line):
            pass
        # process the lines starting from any non-empty symbol and treat them as headwords
        elif re.match(r'[^\s]', line):
            if isSameEntry:
                entryhead.append(line)
            else:
                if isSameEntry == False:
                    __write_entry__(processDSLentry(entryhead, entrybody))
                entryhead = [line]
                entrybody = []
                isSameEntry = True
        # prcess the lines starting from any number of empty symbols and treat them as entry body
        elif re.match(r'\s', line):
            entrybody.append(re.sub(r'\s+', '', line, 1))
            isSameEntry = False
    __write_entry__(processDSLentry(entryhead, entrybody))

def __write_entry__(string):
    print('========================')
    print(string[1])
                             
                             
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

#dslFile = open('../tests/test_convert_data/3WordsDictionary.dsl', 'r', encoding='utf-16')
#processDSLfile(dslFile)
                             

