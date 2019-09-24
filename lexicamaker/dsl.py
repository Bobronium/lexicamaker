#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from .tags import *

config = {}

def __process_header__(line):
    m = re.match(r'#(?P<var>\S+)\s+"(?P<value>.*?)"', line)
    #print(m)
    
    config[m.group('var').lower()] = m.group('value')
    #print(m.group('var'))
    #print(m.group('value'))



def processDSLfile(dslFile, outFile=None, processEntry = processDSLentry):
    entryhead = []
    entrybody = []
    isSameEntry = True
    
    global config
    #print(dslFile)
    #print(outFile)
    
    if outFile:
        result = []
    else:
        result = {}

    for line in dslFile:
        # remove newline sequence in the end of the string
        line = line.rstrip()

        # remove comments
        line = re.sub('{{.*?}}', '', line)
        
        # skip empty lines, \s stays for whitespace characters [ \t\n\r\f\v], and in case of Unicode also many other characters, for example the non-breaking spaces mandated by typography rules in many languages
        if re.fullmatch(r'\s*', line):
            pass
        
        # process lines starting from hash # symbol by adding the pair to the global 'config' dict
        elif re.match(r'#', line):
            m = re.match(r'#(?P<var>\S+)\s+"(?P<value>.*?)"', line)
            config[m.group('var').lower()] = m.group('value')
            if m.group('var').lower() == 'index_language':
                print('!')
                processEntry.__index_language__ = m.group('value')
        
        # process the lines starting from any non-empty symbol and treat them as headwords, \S is not a whitespace character which is the opposite of \s
        elif re.match(r'\S', line):
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

    # EOF closes the last entry, process it
    ref, data = processEntry(entryhead, entrybody)
    if outFile:
        outFile.write(data)
        result.append(ref)
    else:
        result[ref] = data
    
    # return the reuslting data
    return result



def writeBaseTags(xmlFile, opening = True):
    if opening:
        xmlFile.write('<?xml version="1.0" encoding="UTF-8"?>\n<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n')
    else:
        xmlFile.write('</d:dictionary>')


