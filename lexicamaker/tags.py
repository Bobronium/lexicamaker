#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def convertDSLstring(string):
    """ Processing the string by substitution of every known DSL tag by XML tag or calling the corresponding __parse_tag__ function """

    DSLtoXMLmapping = {
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
                        r'\[lang id=(?P<id>\d+)\](?P<text>.*?)\[/lang\]'       : __parse_lang_id__,
                        
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
    for tag in DSLtoXMLmapping:
        string = re.sub(tag, DSLtoXMLmapping[tag], string)

    # if indexing is on and the language match index language then add the string to the index
    if processDSLbodyline.__indexing__ and processDSLbodyline.__language__ == processDSLentry.__index_language__ :
        processDSLbodyline.__theindex__.append(string)

    return string

def indexDSLstring(string):

    indexing = False
    
    index = []
    def __indexing_on__():
        nonlocal indexing
        indexing = True
    def __indexing_off__():
        nonlocal indexing
        indexing = False
    
    DSLindex = {
                    r'\[ex\]'  : __indexing_on__,
                    r'\[/ex\]' : __indexing_off__,
    #                r'\[trn\](?P<text>.*?)\[/trn\]' : __parse_index__,
    #                r'\[com\](?P<text>.*?)\[/com\]' : __parse_index__,
    #                r'\[!trs\](.*?)\[/!trs]'   : '',
    #                r'\[p\](.*?)\[/p]'         : ''
                 }
    print(string)
    splitString = iter(re.split(r'(\[.*?\])', string))
    
    
    for data in splitString:
        #print(data)
        #print(indexing, data)
        if indexing:
            index.append(data)
        tag = next(splitString, None)
        #print(tag)
        if tag:
            for itag in DSLindex:
                #print(tag, itag)
                if (re.fullmatch(itag, tag)!=None):
                    #print('HEY!')
                    DSLindex[itag]()
        #pass



    #print(index)

    
    #for tag in DSLtoIndex:
    #    print(re.findall(tag, string))
    #    string = re.sub(tag, DSLtoIndex[tag], string)
    #return string
    #print(re.findall(r'(?<!\\)\[.*?\]', string))
    #print(re.split(r'(?<!\\)\[.*?\]', string))
    
    
    
    #print(re.split(r'(\[.*?\])', string))
    #print(re.finditer(r'(\[.*?\])', string))
    #for tag, str in zip(re.findall(r'\[.*?\]', r'[]'+string), re.split(r'\[.*?\]', string)):
        #print(tag+':'+str)

    return index




def __parse_index__(match):
    #print('>')
    #print(match.expand(r'\g<text>'))
    return match.expand(r'\g<text>')

def __parse_ex__(match):
    
    # Turn on indexing flag
    processDSLbodyline.__indexing__ = True
    # rerun convertDSLstring() for indexing and processing of the substring
    string = convertDSLstring(match.expand(r'\g<text>'))
    # Turn off indexing flag
    processDSLbodyline.__indexing__ = False
    
    return string

def __parse_lang_id__(match):
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
    prevLang = processDSLbodyline.__language__
    # Set language flag
    processDSLbodyline.__language__ = idtoname[match.expand(r'\g<id>')]
    # rerun convertDSLstring() for indexing and processing of the substring
    string = convertDSLstring(match.expand(r'\g<text>'))
    # Remove language flag
    processDSLbodyline.__language__ = prevLang
    return string

def __parse_lang__(match):
    # Repeats the code of __parse_lang_id__ function
    # Remember the previous language
    prevLang = processDSLbodyline.__language__
    # Set language flag
    processDSLbodyline.__language__ = match.expand(r'\g<name>')
    # rerun convertDSLstring() for indexing and processing of the substring
    string = convertDSLstring(match.expand(r'\g<text>'))
    # Remove language flag
    processDSLbodyline.__language__ = prevLang
    return string

def __makeID__(string):
    id = string

    symbolList = {
            r"_" : r"__",
            r" " : r"_",
            r"'" : r"_a_",
            r"\." : r"_d_",
            r"," : r"_c_",
            r"-" : r"_dash_",
            r"\(": r"_l_",
            r"\)": r"_r_",
            r"/" : r"_s_"
        }
    for symbol in symbolList:
        id = re.sub(symbol, symbolList[symbol], id)

    id = id.lower()
    return id


def processDSLbodyline(string):
    """ Processing the line by calling convertDSLstring() and wrapping free parts as paragraphs by <div>s. """

    # We presume that indexing tags are opening and closing in the same bodyline.
    # Therefore we set off all tags etc.
    processDSLbodyline.__indexing__ = False
    processDSLbodyline.__language__ = None
    processDSLbodyline.__theindex__ = []
    
    string = convertDSLstring(string)
    
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
        string = ''.join(stringSplit)
    #for i, subString in list(enumerate(stringSplit))[0::2]:
    #    stringSplit[i] = '<div>' + subString + '</div>'



    index = ''

    # attach id to the first <div> in the bodyline if there is something in index.
    # it should be not always precise if there are numerous paragraphs in one bodyline

    if processDSLbodyline.__theindex__:
        id = __makeID__(processDSLbodyline.__theindex__[0])
        string = re.sub(r'<div', r'<div id="' + id + '" ', string, 1)
        for value in processDSLbodyline.__theindex__:
            index += '<d:index d:value="' + value + '" d:anchor="xpointer(//*[@id=\'' + id + '\'])"/>'

    # return resulting line
    return (string, index)

# Here we add attributes to the processDSLbodyline() function.
# 1) whether the __indexing__ should be performed with values:
#    True   if indexing should be performed
#    False  if indexing should not be performed
#    None   no indexing until it changes to True
processDSLbodyline.__indexing__ = False
processDSLbodyline.__language__ = None
processDSLbodyline.__theindex__ = []



def processDSLentryhead(entryhead):
    """ This function generates the directives <d:index d:value="" d:title=""/> for further indexing. It also returns the id of the whole entry generated from the first headword."""
    head = ''
    id = __makeID__(entryhead[0])
    for line in entryhead:
        head += '<d:index d:value="' + line + '" d:title="' + line + '"/>\n'
    return (id, head)

def processDSLentrybody(entrybody):
    body = ''
    head = ''
    for line in entrybody:
        string, index = processDSLbodyline(line)
        if string:
            body += string + '\n'
        if index:
            head += index  + '\n'
    return (head, body)

def processDSLentry(entryhead, entrybody):
    """ Should return entry XML object containing the  """
    id, headOrig   = processDSLentryhead(entryhead)
    headBody, body = processDSLentrybody(entrybody)
    entry = '<d:entry id="' + id + '">\n' + headOrig + headBody + body + '</d:entry>\n'
    return (id, entry)

# Here we add attributes to the processDSLentry() function.
#processDSLentry.__index_language__ = 'Russian'
processDSLentry.__index_language__ = 'English'
