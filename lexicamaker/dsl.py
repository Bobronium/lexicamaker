#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re




def processDSLstring(string):
    """ Processing the string by substitution of every known DSL tag by XML tag or calling the corresponding __parse_tag__ function """

    DSLtoXMLmaping = {
                        # TYPE I TAGS: text-independent, one can map open and closing tags separately.
                        # It is useful if opening and closing tags are not in the same string.
                        # For example: here it's better to match [m] tags separately, while closing tag [/m] can be in the different line
                        r'\[m\]'                  : r'<div>',
                        # here \d stays for decimal digit, it's [0-9] and in case of Unicode other digit characters
                        r'\[m(?P<indent>\d)\]' : r'<div class="m\g<indent>">',
                        r'\[/m\]'                 : r'</div>',
                        r'\[br\]'   : r'<br />',
                        r'\[\*\]'   : r'<span d:priority="2">',
                        r'\[/\*\]'  : r'</span>',
                        r'\[b\]'    : r'<b>', r'\[/b\]'  : r'</b>',
                        r'\[i\]'    : r'<i>', r'\[/i\]'  : r'</i>',
                        r'\[u\]'    : r'<u>', r'\[/u\]'  : r'</u>',
                        # here \w stays for word characters, it's [a-zA-Z0-9_] and in case of Unicode most characters that can be part of a word in any language
                        r'\[c\]'                : r'<font color="green">',
                        r'\[c (?P<color>\w+)\]' : r'<font color="\g<color>">',
                        r'\[/c\]'               : r'</font>',
                        r'\[sub\]'  : r'<sub>', r'\[/sub\]'  : '</sub>',
                        r'\[sup\]'  : r'<sup>', r'\[/sup\]'  : '</sup>',
                        r'\[\'\]'   : '', r'\[/\'\]'    : '\u0301',
                        
                        # TYPE II TAGS: call a function instead of the substitution pattern, can process text between tags.
                        # Downside is that opening and closing tags should be in the same line.
                        # In case they isn't one has to substitute free dangling tags by empty string afterwards
                        
                        
                        r'\[ex\](?P<text>.*?)\[/ex\]'   : __parse_ex__,
                        r'\[lang\](?P<text>.*?)\[/lang\]'                      : __parse_lang__,
                        r'\[lang name="(?P<name>\w+)"\](?P<text>.*?)\[/lang\]' : __parse_lang__,
                        r'\[lang id=(?P<id>\d+)\](?P<text>.*?)\[/lang\]'       : __parse_lang__,
                        
                        r'\[trn\]'  : '', r'\[/trn\]'   : '',
                        r'\[com\]'  : '', r'\[/com\]'   : '',
                        r'\[!trs\]' : '', r'\[/!trs]'   : '',
                        
                        r'\[lang\]'            : '',
                        r'\[lang name="\w+"\]' : '',
                        r'\[lang id=\d+\]'     : '',
                        r'\[/lang\]'           : '',
                        
                        r'\[p\]'    : '', r'\[/p\]'     : '',
                        r'\[t\]'    : r'<span d:pr="1">',
                        r'\[/t\]'   : r'</span>',
                        r'\[s\]'    : '', r'\[/s\]'     : '',
                        r'<<'       : '', r'>>'         : '',
                        r'\[ref\]'                             : '',
                        r'\[ref dict="(?P<dname>[\w\s]+)"\]' : '',
                        r'\[/ref\]'                            : '',
                        r'\[url\]'  : '', r'\[/url\]'   : ''
                    }

    # Simply substitute every tag in the line
    for tag in DSLtoXMLmaping:
        string = re.sub(tag, DSLtoXMLmaping[tag], string)

    return string

def __parse_ex__(match):
    print(match)
    print(match.group())
    print(match.expand('\g<text>'))
    
    processDSLstring.__indexing__ = True
    
    # run indexing and processing

    del(processDSLstring.__indexing__)
    
    return match.expand('\g<text>')

def __parse_lang__(match):
    print(match)
    print(match.group())
    print(match.expand('\g<text>'))
    
    processDSLstring.__language__ = match.expand('\g<name>')
    
    # run indexing and processing
    
    del(processDSLstring.__language__)
    
    return match.expand('\g<text>')

def processDSLbodyline(string):
    """ Processing the line by calling processDSLstring() and wrapping free parts as paragraphs by <div>s. """

    string = processDSLstring(string)
    
    # Make sure that a line is treated as a paragraph.
    # Either the whole line is wrapped in <div>,
    # or if there is any new paragraph <div>s in the line,
    # wrap the free beginning and ending of the line in <div>s

    stringSplit = re.split(r'(<div(?: [^<>]+)*>|</div>)',string)
    if len(stringSplit) == 1:
        string = '<div>' + string + '</div>'
    else:
        for i in [0,-1]:
            if stringSplit[i]:
                stringSplit[i] = '<div>' + stringSplit[i] + '</div>'
    #for i, subString in list(enumerate(stringSplit))[0::2]:
    #    stringSplit[i] = '<div>' + subString + '</div>'

    string = ''.join(stringSplit)

    # return resulting line
    return string




def processDSLentryhead(entryhead):
    """ This function generates the directives <d:index d:value="" d:title=""/> for further indexing. It also returns the id of the whole entry generated form the first headword """
    head = ''
    for line in entryhead:
        head = head + '<d:index d:value="' + line + '" d:title="' + line + '"/>\n'
    id = re.sub('[^a-z0-9]', '_', entryhead[0].lower())
    return (id, head)

def processDSLentrybody(entrybody):
    body = ''
    for line in entrybody:
        body = body + processDSLbodyline(line) + '\n'
    return body

def processDSLentry(entryhead, entrybody):
    """ Should return entry XML object containing the  """
    id, head = processDSLentryhead(entryhead)
    body = processDSLentrybody(entrybody)
    entry = '<d:entry id="' + id + '">\n' + head + body + '</d:entry>\n'
    return (id, entry)

def processDSLfile(dslFile, xmlFile):
    entryhead = []
    entrybody = []
    isSameEntry = None
    for line in dslFile:
        # remove newline sequence in the end of the string
        line = line.rstrip()
        # remove comments
        line = re.sub('{{.*?}}', '', line)
        # skip empty lines, \s stays for whitespace characters [ \t\n\r\f\v], and in case of Unicode also many other characters, for example the non-breaking spaces mandated by typography rules in many languages
        if re.fullmatch(r'\s*', line):
            pass
        # skip lines starting from hash # symbol
        elif re.match(r'#', line):
            pass
        # process the lines starting from any non-empty symbol and treat them as headwords, \S is not a whitespace character which is the opposite of \s
        elif re.match(r'\S', line):
            if isSameEntry:
                entryhead.append(line)
            else:
                if isSameEntry == False:
                    #xmlFile.write(processDSLentry(entryhead, entrybody)[1])
                    __write_entry__(processDSLentry(entryhead, entrybody))
                entryhead = [line]
                entrybody = []
                isSameEntry = True
        # process the lines starting from any number of empty symbols and treat them as entry body
        elif re.match(r'\s', line):
            entrybody.append(re.sub(r'\s+', '', line, 1))
            isSameEntry = False
    #xmlFile.write(processDSLentry(entryhead, entrybody))
    __write_entry__(processDSLentry(entryhead, entrybody))

def __write_entry__(string):
    #print('========================')
    print(string[1])
                             
def writeBaseTags(xmlFile, opening = True):
    if opening:
        xmlFile.write('<?xml version="1.0" encoding="UTF-8"?>\n<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n')
    else:
        xmlFile.write('</d:entry>\n</d:dictionary>')

#def __parse_c__(myString):
#    if myString == None:
#        return "<font color=\"green\">"
#    else:
#        return "<font color=\"\\g<" + myString + ">\">"

#theDSLbodyline = r"[c]\[[u]'əup(ə)n[/u]\][/c] [c blue]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"

#theDSLbodyline = r"[m1]\[[u]'əup(ə)n[/u]\][/m] [m2] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"

#theDSLbodyline = r"[c]брит.[/c]"

theDSLbodyline = "[c blue]брит.[/c] [m1]1) [i][trn][com]способ изготовления изображений[/com][/trn][/i][/m][m2][*][ex][lang name=\"English\"]photography[/lang] — фотография[/ex][/*][/m][m2][*][lang name=\"English\"]radiography[/lang] — [ex]радиография[/ex][/*][/m]"

myString = processDSLbodyline(theDSLbodyline)

#result = re.findall(r'\[lang id=(?P<lid>[0-9]{4})\](?P<text>.*?)\[/lang\]', theDSLbodyline)

print(myString)



#def __f__(m):
#    number_mapping = {'1': 'one', '2': 'two', '3': 'three'}
#    print(m)
#    print(m.group())
#    print(m.expand())
#    return number_mapping[m.group()]

#print(re.sub(r'\d', __f__, "1 testing 2 3"))

#import xml.etree.ElementTree as ET

    #xmlString = """<d:entry xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">
    #    <div>\[<span d:pr="1">əˌbændə'niː</span>\]</div>
    #    <div>сущ.</div>
    #    <div class="m1">1) юр. лицо, в пользу которого имеет место отказ от права</div>
#    <div class="m1">2) мор. страховщик, в пользу которого остаётся застрахованный груз <i>или</i> застрахованное судно в случае аварии</div>
#</d:entry>"""

#root = ET.fromstring(xmlString)

#print(root.tag, root.attrib)
#for child in root:
#    print(child.tag, child.attrib, child.text)

#dslFile = open('../tests/test_convert_data/3WordsDictionary.dsl', 'r', encoding='utf-16')
#xmlFile = open('../tests/test_convert_data/3WordsDictionary.xml', 'w+', encoding='utf-8')

#processDSLfile(dslFile, xmlFile)
#xmlFile.close()
#dslFile.close()
                             

