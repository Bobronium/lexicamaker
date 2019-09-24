#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

DSLtags = {
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
        r'\[\'\]'   : r'<font color="red">', r'\[/\'\]'    : '</font>',
 
        r'\[s\]'    : '', r'\[/s\]'     : '',
        r'<<'       : '', r'>>'         : '',
        r'\[ref\]'                             : '',
        r'\[ref dict="(?P<dname>[\w\s]+)"\]'   : '',
        r'\[/ref\]'                            : '',
        r'\[url\]'  : '', r'\[/url\]'   : '',

        # TYPE II TAGS: call a function instead of the substitution pattern, can process text between tags.
        # Downside is that opening and closing tags should be in the same line.
        # In case they isn't one has to substitute free dangling tags by empty string afterwards
        
        r'\[ex\](?P<content>)\[/ex\]'       : r'\g<content>',
        r'\[trn\](?P<content>)\[/trn\]'     : r'\g<content>',
        r'\[com\](?P<content>)\[/com\]'     : r'\g<content>',
        r'\[!trs\](?P<content>)\[/!trs\]'     : r'\g<content>',
        
        r'\[p\]'    : r'<font color="green">',
        r'\[/p\]'   : r'</font>',
        r'\[t\]'    : r'<span d:pr="1">',
        r'\[/t\]'   : r'</span>'

}

def process_escape_char(string, encode=True):
    """ Substitutes escaped characters like '\\[' by the escape code '\\x5b' and back by single character '['. Also escapes the HTML special characters '&', '\"', '>', and '<'. """
    
    if encode:
        string = re.sub(r'([&><])', r'\\\\\1', string)
        return re.sub(r'\\(.)', lambda match: r'\x%02x' % ord(match.expand(r'\1')), string)
    else:
        return re.sub(r'\\x([0-9a-f]{2})', lambda match: chr(int(match.expand(r'\1'), 16)), string)


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
                        r'\[\'\]'   : r'<font color="red">', r'\[/\'\]'    : '</font>',
                        
                        # TYPE II TAGS: call a function instead of the substitution pattern, can process text between tags.
                        # Downside is that opening and closing tags should be in the same line.
                        # In case they isn't one has to substitute free dangling tags by empty string afterwards
                        
                        r'\[p\]'    : r'<font color="green">',
                        r'\[/p\]'   : r'</font>',
                        r'\[t\]'    : r'<span d:pr="1">',
                        r'\[/t\]'   : r'</span>',
                        r'\[s\]'    : '', r'\[/s\]'     : '',
                        r'<<'       : '', r'>>'         : '',
                        r'\[ref\]'                             : '',
                        r'\[ref dict="(?P<dname>[\w\s]+)"\]'   : '',
                        r'\[/ref\]'                            : '',
                        r'\[url\]'  : '', r'\[/url\]'   : '',
                        
                        # REST OF TAGS: substituted by empty string
                        
                        r'\[.*?\]' : ''
                    }

    # Simply substitute every tag in the line
    for tag in DSLtoXMLmapping:
        string = re.sub(tag, DSLtoXMLmapping[tag], string)

    # Make sure that a line is treated as a paragraph.
    # Either the whole line is wrapped in <div>,
    # or if there is any new paragraph <div>s in the line,
    # wrap the free beginning and ending of the line in <div>s

    print(string, '\n')
    stringSplit = re.split(r'(<div(?: [^<>]+)*?>|</div>)', string)
    if len(stringSplit) == 1:
        string = r'<div>' + string + r'</div>'
    else:
        for i in [0,-1]:
            if stringSplit[i]:
                stringSplit[i] = r'<div>' + stringSplit[i] + r'</div>'
        string = ''.join(stringSplit)
    

    #string = re.sub(r'(^.+?)(?:(<div[ >])|$)', r'<div>\1</div>', string)
    print(string)
    return string

def indexDSLstring(string):

    indexing = False
    language = processDSLentry.__contents_language__
    
    index = []
    def __indexing_on__(match):
        nonlocal indexing
        indexing = True
    
    def __indexing_off__(match):
        nonlocal indexing
        indexing = False
    
    def __default_lang__(match):
        nonlocal language
        language = processDSLentry.__index_language__
    
    def __reset_lang__(match):
        nonlocal language
        language = processDSLentry.__contents_language__
    
    def __set_lang__(match):
        nonlocal language
        language = match.expand(r'\g<text>')
    
    def __set_lang_id__(match):
        nonlocal language
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
        language = idtoname[match.expand(r'\g<id>')]

    #    def __translation_on__(match):
    #        nonlocal indexing
    #        nonlocal language
    #        indexing = True
    #        language = processDSLentry.__contents_language__
    #    def __translation_off__(match):
    #        nonlocal indexing
    #        #nonlocal language
    #        indexing = False
    #        #language = processDSLentry.__contents_language__
                
    DSLindex = {
                    r'\[ex\]'  : __indexing_on__,
                    r'\[/ex\]' : __indexing_off__,
                    r'\[lang\]'                      : __default_lang__,
                    r'\[/lang\]'                     : __reset_lang__,
                    r'\[lang name="(?P<name>\w+)"\]' : __set_lang__,
                    r'\[lang id=(?P<id>\d+)\]'       : __set_lang_id__
                    #r'\[trn\]'   : __translation_on__,
                    #r'\[/trn\]'  : __translation_off__,
                    #r'\[!trs\]'  : __indexing_off__,
                    #r'\[/!trs\]' : __indexing_on__,
                    #r'\[com\]'  : __indexing_off__,
                    #r'\[/com\]' : __indexing_on__,
                 }
    #print(string)
    splitString = iter(re.split(r'(\[.*?\])', string))
    
    
    for data in splitString:
        if indexing and language == processDSLentry.__index_language__:
            index.append(data)
        tag = next(splitString, None)
        if tag:
            for itag in DSLindex:
                match = re.fullmatch(itag, tag)
                if (match != None):
                    #print(match)
                    DSLindex[itag](match)
        #pass

    #print(index)

    return index


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

    string = process_escape_char(string, True)
    
    # We presume that indexing tags are opening and closing in the same bodyline.
    index = ''
    divTag = [r'<div>', r'</div>']
    indexSplit = indexDSLstring(string)

    
    if indexSplit:
        id = __makeID__(indexSplit[0])
        # attach id to the first <div> in the bodyline if there is something in index.

        divTag[0] = r'<div id="' + id + '">'
        for value in indexSplit:
            index += '<d:index d:value="' + value + '" d:anchor="xpointer(//*[@id=\'' + id + '\'])"/>'

    
    content = convertDSLstring(string)
    
    # Make sure that a line is treated as a paragraph.
    # Either the whole line is wrapped in <div>,
    # or if there is any new paragraph <div>s in the line,
    # wrap the free beginning and ending of the line in <div>s

    # it should be not always precise if there are numerous paragraphs in one bodyline
    #contentSplit = re.split(r'(<div(?: [^<>]+)*>|</div>)',content)
    #if len(contentSplit) == 1:
    #    content = divTag[0] + content + divTag[1]
    #else:
    #    for i in [0,-1]:
    #        if contentSplit[i]:
    #            contentSplit[i] = divTag[0] + contentSplit[i] + divTag[1]
    #    content = ''.join(contentSplit)
    #for i, subString in list(enumerate(stringSplit))[0::2]:
    #    stringSplit[i] = '<div>' + subString + '</div>'

    content = process_escape_char(content, False)
    index = process_escape_char(index, False)
    # return resulting line
    return (content, index)




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
processDSLentry.__contents_language__ = 'Russian'
processDSLentry.__index_language__ = 'English'
