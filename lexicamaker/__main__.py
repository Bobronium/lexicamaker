#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys
import argparse
from lexicamaker import __version__

class IOBridge:
    
    def __init__(self):
        
        self.parser = argparse.ArgumentParser(prog='adsmaker',
                                         description="Lexicamaker v%s - creates Apple Dictionary Service folder from DSL dictionary" % __version__,
                                         #usage='%(prog)s [options] DSL_FILE [OUTPUT_DIR]\n       %(prog)s [--help | --version]',
                                         epilog="The created Apple Dictionary Service folder must be then compiled with Apple Dictionary Development Kit")
        #self.parser.add_argument('dslfile', metavar='DSL_FILE', type=argparse.FileType('r', encoding='utf-16le'), help="a DSL dictionary file")
        self.parser.add_argument('dictionaryFile', metavar='DSL_FILE', help="a DSL dictionary file")
        subgroup0 = self.parser.add_mutually_exclusive_group()
        subgroup0.add_argument('outputDictionaryPath', metavar='OUTPUT_DIR', nargs='?', default=os.getcwd(), help="a path for Apple Dictionary Service folder (uses current directory by default)")
        self.parser.add_argument('-v', '--verbose', action='count', help="increase output verbosity")
        group = self.parser.add_argument_group('Fine tuning')
        subgroup1 = group.add_mutually_exclusive_group()
        subgroup1.add_argument('--no-annotation', dest='annotationFile', action='store_false', help="Ignore annotation")
        #subgroup1.add_argument('--annotation', metavar='FILE', type=argparse.FileType('r', encoding='utf-16le'), help="annotation file")
        subgroup1.add_argument('--annotation', metavar='FILE', dest='annotationFile', help="annotation file")
        subgroup2 = group.add_mutually_exclusive_group()
        #group.add_argument('--abbreviations', metavar='FILE', type=argparse.FileType('r', encoding='utf-16le'), help="abbreviations file")
        subgroup2.add_argument('--abbreviations', metavar='FILE', dest='abbreviationsFile', help="abbreviations file")
        subgroup2.add_argument('--no-abbreviations', dest='abbreviationsFile', action='store_false', help="Ignore abbreviations")
        group.add_argument('--name', metavar='NAME', dest='dictionaryName', help="set dictionary name")
        subgroup3 = group.add_mutually_exclusive_group()
        subgroup3.add_argument('--no-media', action='store_true', help="Skip media")
        subgroup3.add_argument('--media', metavar='TYPE', choices=['wav', 'mp3', 'm4a', 'aac'], help="Change media type to TYPE (supported wav, mp3, m4a, aac)")
        group.add_argument('--encoding', metavar='ENCODING', default='utf-16le', help="set dictionary name")
        self.parser.add_argument('--version', action='version', version="lexicamaker v%s" % __version__ ) #"%(prog)s v{}".format(__version__))
        subgroup0.add_argument('--remote', action='store_true', help="forces to build the Apple Dictionary Service folder next to main DSL_FILE dictionary")

    def parse_args(self):
        self.parser.parse_args(namespace = self)

    def open_files(self):
        self.parse_args()

        dictionaryPath = os.path.dirname(self.dictionaryFile)
        dictionaryName, dictionaryExtension = os.path.splitext(os.path.basename(self.dictionaryFile))

        if dictionaryExtension.lower() != '.dsl':
            sys.stderr.write ("Warning: dictionary file does not have a .dsl extension.\n")
            dictionaryName += dictionaryExtension
    
        if not self.dictionaryName:
            self.dictionaryName = dictionaryName

        if self.remote:
            self.outputDictionaryPath = os.path.join(dictionaryPath, dictionaryName)
        else:
            self.outputDictionaryPath = os.path.join(self.outputDictionaryPath, dictionaryName)
        
        self.dictionaryFile = open(self.dictionaryFile, 'r', encoding='utf-16le')

        if self.annotationFile :
            self.annotationFile = open(self.annotationFile, 'r', encoding='utf-16le')
        elif self.annotationFile == None:
            try:
                self.annotationFile = open(os.path.join(dictionaryPath, dictionaryName) + '.ann', 'r', encoding='utf-16le')
            except FileNotFoundError:
                self.annotationFile = None

        if self.abbreviationsFile :
            self.abbreviationsFile = open(self.abbreviationsFile, 'r', encoding='utf-16le')
        elif self.abbreviationsFile == None:
            try:
                self.abbreviationsFile = open(os.path.join(dictionaryPath, dictionaryName) + '_abrv.dsl', 'r', encoding='utf-16le')
            except FileNotFoundError:
                self.abbreviationsFile = None



        print (self.outputDictionaryPath)
        print (self.dictionaryName)
        print (self.dictionaryFile)
        print (self.annotationFile)
        print (self.abbreviationsFile)


def main():
    ioDict = IOBridge()
    
    ioDict.open_files()
    #args = arguments_parser().parse_args()

    




#    print (dictionaryFile)





if __name__ == "__main__":
    main()
