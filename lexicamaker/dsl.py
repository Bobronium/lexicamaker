#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from .tags import *

def __process_and_write_entry__(entryhead, entrybody):
    #print('========================')
    string = processDSLentry(entryhead, entrybody)
    print(string[1])

def processDSLfile(dslFile, outFile=None, processEntry = processDSLentry):
    entryhead = []
    entrybody = []
    isSameEntry = True
    
    #print(dslFile)
    #print(outFile)
    
    if outFile:
        result = []
    else:
        result = {}

    for line in dslFile:
        # remove newline sequence in the end of the string
        line = line.rstrip()
        #print(line)
        # remove comments
        line = re.sub('{{.*?}}', '', line)
        # skip empty lines, \s stays for whitespace characters [ \t\n\r\f\v], and in case of Unicode also many other characters, for example the non-breaking spaces mandated by typography rules in many languages
        if re.fullmatch(r'\s*', line):
            pass
        # skip lines starting from hash # symbol
        elif re.match(r'#', line):
            pass
            #print('hash')
            # process the lines starting from any non-empty symbol and treat them as headwords, \S is not a whitespace character which is the opposite of \s
        elif re.match(r'\S', line):
            #print('no space')
            if isSameEntry:
                entryhead.append(line)
            else:
                ref, data = processEntry(entryhead, entrybody)
                if outFile:
                    outFile.write(data)
                    result.append(ref)
                else:
                    result[ref] = data
                entryhead = [line]
                entrybody = []
                isSameEntry = True
        # process the lines starting from any number of empty symbols and treat them as entry body
        elif re.match(r'\s', line):
            #print('space')
            entrybody.append(re.sub(r'\s+', '', line, 1))
            isSameEntry = False


    ref, data = processEntry(entryhead, entrybody)
    if outFile:
        outFile.write(data)
        result.append(ref)
    else:
        result[ref] = data

    return result



def writeBaseTags(xmlFile, opening = True):
    if opening:
        xmlFile.write('<?xml version="1.0" encoding="UTF-8"?>\n<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n')
    else:
        xmlFile.write('</d:dictionary>')


