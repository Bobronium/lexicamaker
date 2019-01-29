#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys
import argparse
from lexicamaker import __version__

class IOBridge:
    parser = argparse.ArgumentParser(prog='adsmaker',
                                            description="Lexicamaker v%s - creates Apple Dictionary Service folder from DSL dictionary" % __version__,
                                            #usage='%(prog)s [options] DSL_FILE [OUTPUT_DIR]\n       %(prog)s [--help | --version]',
                                            epilog="The created Apple Dictionary Service folder must be then compiled with Apple Dictionary Development Kit")
    
    def __set_parser__(parser):
        """This function is called once for shared parser object and sets the processing of the command line arguments"""
        #parser.add_argument('dictionaryFile', metavar='DSL_FILE', type=argparse.FileType('r', encoding='utf-16le'), help="a DSL dictionary file")
        #parser.add_argument('dictionaryFile', metavar='DSL_FILE', help="a DSL dictionary file")
        parser.add_argument('dictionaryFile', metavar='DSL_FILE', help="a DSL dictionary file")
        subgroup_opath = parser.add_mutually_exclusive_group()
        subgroup_opath.add_argument('outputDictionaryPath', metavar='OUTPUT_DIR', nargs='?', default=os.getcwd(), help="a path for Apple Dictionary Service folder (uses current directory by default)")
        parser.add_argument('-v', '--verbose', action='count', default=0, help="increase output verbosity")
        group = parser.add_argument_group('Fine tuning')
        subgroup_ann = group.add_mutually_exclusive_group()
        subgroup_ann.add_argument('--annotation', metavar='FILE', dest='annotationFile', default=None, help="annotation file")
        subgroup_ann.add_argument('--no-annotation', dest='annotationFile', action='store_false', help="ignore annotation")
        subgroup_abrv = group.add_mutually_exclusive_group()
        subgroup_abrv.add_argument('--abbreviations', metavar='FILE', dest='abbreviationsFile', default=None, help="abbreviations file")
        subgroup_abrv.add_argument('--no-abbreviations', dest='abbreviationsFile', action='store_false', help="ignore abbreviations")
        group.add_argument('--name', metavar='NAME', dest='dictionaryName', help="set dictionary name")
        subgroup_media = group.add_mutually_exclusive_group()
        subgroup_media.add_argument('--no-media', action='store_true', help="Skip media")
        subgroup_media.add_argument('--media', metavar='TYPE', choices=['wav', 'mp3', 'm4a', 'aac'], help="Change media type to TYPE (supported wav, mp3, m4a, aac)")
        group.add_argument('--encoding', metavar='ENCODING', default='utf-16le', help="set dictionary name")
        parser.add_argument('--version', action='version', version="lexicamaker v%s" % __version__ ) #"%(prog)s v{}".format(__version__))
        subgroup_opath.add_argument('--remote', action='store_true', help="forces to build the Apple Dictionary Service folder next to main DSL_FILE dictionary")

    __set_parser__(parser)

    def parse_args(self, args=None, namespace=None):
        if not namespace:
            namespace = self
        return self.parser.parse_args(args, namespace)

    def __init__(self, args=None, namespace=None):
        self.parse_args(args, namespace)
    


    def open_files(self):
        #self.parse_args()

        dictionaryPath = os.path.dirname(self.dictionaryFile)
        dictionaryName, dictionaryExtension = os.path.splitext(os.path.basename(self.dictionaryFile))

        if dictionaryExtension.lower() != '.dsl':
            if self.verbose >= 1:
                sys.stdout.write ("Warning: input DSL dictionary file should have a .dsl extension.\n")
            dictionaryName = os.path.basename(self.dictionaryFile)
    
        if not self.dictionaryName:
            self.dictionaryName = dictionaryName

        if self.remote:
            self.outputDictionaryPath = os.path.join(dictionaryPath, self.dictionaryName)
        else:
            self.outputDictionaryPath = os.path.join(self.outputDictionaryPath, self.dictionaryName)
        
        self.dictionaryFile = open(self.dictionaryFile, 'r', encoding='utf-16le')

        if self.annotationFile :
            self.annotationFile = open(self.annotationFile, 'r', encoding='utf-16le')
        elif self.annotationFile is None:
            try:
                self.annotationFile = open(os.path.join(dictionaryPath, dictionaryName) + '.ann', 'r', encoding='utf-16le')
            except FileNotFoundError:
                if self.verbose >= 2:
                    sys.stdout.write ("Warning: annotation file is not found.\n")

        if self.abbreviationsFile :
            self.abbreviationsFile = open(self.abbreviationsFile, 'r', encoding='utf-16le')
        elif self.abbreviationsFile is None:
            try:
                self.abbreviationsFile = open(os.path.join(dictionaryPath, dictionaryName) + '_abrv.dsl', 'r', encoding='utf-16le')
            except FileNotFoundError:
                if self.verbose >= 2:
                    sys.stdout.write ("Warning: abbreviations file is not found.\n")




def main():
    ioDict = IOBridge()
    
    ioDict.open_files()


    print (ioDict.outputDictionaryPath)
    print (ioDict.dictionaryName)
    print (ioDict.dictionaryFile.name)
    print (ioDict.annotationFile.name)
    print (ioDict.abbreviationsFile.name)


#    print (dictionaryFile)





if __name__ == "__main__":
    main()
