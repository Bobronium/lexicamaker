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



    if processDSLstring.__indexing__ and processDSLstring.__language__ == 'English':
        processDSLstring.__theindex__.append(string)

    return string

# Here we add attributes to the processDSLstring() function.
# 1) whether the __indexing__ should be performed with values:
#    True   if indexing should be performed
#    False  if indexing should not be performed
#    None   no indexing until it changes to True
processDSLstring.__indexing__ = False
processDSLstring.__language__ = None
processDSLstring.__theindex__ = []

#def fix_attr():
#    processDSLstring.__indexing__ = None

def __parse_ex__(match):
    
    # Turn on indexing flag
    processDSLstring.__indexing__ = True
    # rerun processDSLstring() fir indexing and processing of the substring
    string = processDSLstring(match.expand(r'\g<text>'))
    # Turn off indexing flag
    processDSLstring.__indexing__ = False
    
    return string

def __parse_lang__(match):
    idtoname = {
                    #'1068' : 'AzeriLatin',
                    '1033' : 'English',
                    '1025' : 'Arabic',
                    '1067' : 'Armenian',
                    '32811': 'ArmenianWestern',
                    '1078' : 'Afrikaans',
                    '1069' : 'Basque',
                    '1133' : 'Bashkir',
                    '1059' : 'Belarusian',
                    '1026' : 'Bulgarian',
                    '1038' : 'Hungarian',
                    '1043' : 'Dutch',
                    '1032' : 'Greek',
                    '1079' : 'Georgian',
                    '1030' : 'Danish',
                    '1057' : 'Indonesian',
                    '1039' : 'Icelandic',
                    '3082' : 'SpanishModernSort',
                    '1034' : 'SpanishTraditionalSort',
                    '1040' : 'Italian',
                    '1087' : 'Kazakh',
                    #'1595' : 'Kirgiz',
                    '1028' : 'Chinese',
                    '2052' : 'ChinesePRC',
                    '1142' : 'Latin',
                    '1062' : 'Latvian',
                    '1063' : 'Lithuanian',
                    '1086' : 'Malay',
                    '1031' : 'German',
                    #'32775': 'GermanNewSpelling',
                    '1044' : 'NorwegianBokmal',
                    '2068' : 'NorwegianNynorsk',
                    '1045' : 'Polish',
                    '2070' : 'PortugueseStandard',
                    '1048' : 'Romanian',
                    '1049' : 'Russian',
                    '3098' : 'SerbianCyrillic',
                    '1051' : 'Slovak',
                    '1060' : 'Slovenian',
                    '1089' : 'Swahili',
                    '1064' : 'Tajik',
                    '1092' : 'Tatar',
                    '1055' : 'Turkish',
                    #'1090' : 'Turkmen',
                    #'1091' : 'UzbekLatin',
                    '1058' : 'Ukrainian',
                    '1035' : 'Finnish',
                    '1036' : 'French',
                    '1029' : 'Czech',
                    '1053' : 'Swedish',
                    '1061' : 'Estonian'
                }
    # Remember the previous language
    prevLang = processDSLstring.__language__
    # Set language flag
    #lang = match.expand(r'\g<name>')
    
    processDSLstring.__language__ = match.expand(r'\g<name>')
    # rerun processDSLstring() fir indexing and processing of the substring
    string = processDSLstring(match.expand(r'\g<text>'))
    # Remove language flag
    processDSLstring.__language__ = prevLang
    
    return string

def makeID(string):
    id = string

    symbolList = {
            r"_" : r"__",
            r" " : r"_",
            r"'" : r"_a_",
            r"-" : r"_d_",
            r"\(": r"_l_",
            r"\)": r"_r_",
            r"/" : r"_s_"
        }
    for symbol in symbolList:
        id = re.sub(symbol, symbolList[symbol], id)

    print (id)
    return id

def processDSLbodyline(string):
    """ Processing the line by calling processDSLstring() and wrapping free parts as paragraphs by <div>s. """

    processDSLstring.__indexing__ = False
    processDSLstring.__language__ = None
    processDSLstring.__theindex__ = []
    
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

    # attach id to the first <div> in the bodyline.
    # it should be not always precise if there are numerous paragraphs in one bodyline
    if processDSLstring.__theindex__:
        string = re.sub(r'<div', r'<div id="' + makeID(processDSLstring.__theindex__[0]) + '" ', string, 1)

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
                             

