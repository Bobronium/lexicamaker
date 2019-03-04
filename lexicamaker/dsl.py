#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from .tags import *

def __process_and_write_entry__(entryhead, entrybody):
    #print('========================')
    string = processDSLentry(entryhead, entrybody)
    print(string[1])

def processDSLfile(dslFile, processor = __process_and_write_entry__):
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
                    processor(entryhead, entrybody)
                entryhead = [line]
                entrybody = []
                isSameEntry = True
        # process the lines starting from any number of empty symbols and treat them as entry body
        elif re.match(r'\s', line):
            entrybody.append(re.sub(r'\s+', '', line, 1))
            isSameEntry = False
    processor(entryhead, entrybody)



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

if __name__ == "__main__":

    #theDSLbodyline = r"[c]\[[u]'əup(ə)n[/u]\][/c] [c blue]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"

    #theDSLbodyline = r"[m1]\[[u]'əup(ə)n[/u]\][/m] [m2] [c]брит.[/c] [b]1.[/b] [i]прил.[/i] открытый"

    #theDSLbodyline = r"[c]брит.[/c]"

    theDSLbodyline = "[c blue]брит.[/c] [m1]1) [i][trn][com]способ изготовления изображений[/com][/trn][/i][/m][m2][*][ex][lang name=\"English\"]photography[/lang] — фотография[/ex][/*][/m][m2][*][lang name=\"English\"]radiography[/lang] — [ex]радиография[/ex][/*][/m]"

    myString = processDSLbodyline(theDSLbodyline)


    print(myString)

    #result = re.findall(r'\[lang id=(?P<lid>[0-9]{4})\](?P<text>.*?)\[/lang\]', theDSLbodyline)

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


