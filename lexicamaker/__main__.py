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
        subgroup_opath.add_argument('outputDictionaryPath', metavar='OUTPUT_DIR', nargs='?', default=os.getcwd(),
                                    help="Use an OUTPUT_DIR to place Apple Dictionary Service folder (uses current directory by default)")
        parser.add_argument('-v', '--verbose', action='count', default=0,
                                    help="Increases output verbosity")
        group = parser.add_argument_group('Fine tuning')
        subgroup_ann = group.add_mutually_exclusive_group()
        subgroup_ann.add_argument('--annotation', metavar='FILE', dest='annotationFile', default=None,
                                    help="Use FILE as annotation file")
        subgroup_ann.add_argument('--no-annotation', dest='annotationFile', action='store_false',
                                    help="Ignore annotation files")
        subgroup_abrv = group.add_mutually_exclusive_group()
        subgroup_abrv.add_argument('--abbreviations', metavar='FILE', dest='abbreviationsFile', default=None,
                                    help="Use FILE as abbreviations file")
        subgroup_abrv.add_argument('--no-abbreviations', dest='abbreviationsFile', action='store_false',
                                    help="Ignore abbreviations files")
        group.add_argument('--name', metavar='NAME', dest='dictionaryName', help="set dictionary name")
        subgroup_media = group.add_mutually_exclusive_group()
        subgroup_media.add_argument('--no-media', action='store_true', dest='media',
                                    help="Skip media entries")
        subgroup_media.add_argument('--media', metavar='TYPE', choices=['wav', 'mp3', 'm4a', 'aac'],
                                    help="Change media type to TYPE. Supported formats are \'wav\', \'mp3\', \'m4a\', and \'aac\'")
        group.add_argument('--encoding', metavar='ENCODING', default='utf-16', choices=['utf-8', 'utf-16', 'utf-16le', 'utf-16be'],
                                    help="Set DSL dictionary encoding, suppored encodings are \'utf-8\' and \'utf-16\' (default). If in latter encoding the Byte Order Mark is is missing use \'utf-16le\' or \'utf-16be\'.")
        parser.add_argument('--version', action='version', version="lexicamaker v%s" % __version__ ) #"%(prog)s v{}".format(__version__))
        subgroup_opath.add_argument('--remote', action='store_true',
                                    help="Forces to place the Apple Dictionary Service folder next to main DSL_FILE dictionary")

    __set_parser__(parser)

    
    
    def parse_args(self, args=None, namespace=None):
        """Calls ArgumentParser::parse_args function with itself instead of Namespace"""
        if not namespace:
            namespace = self
        return self.parser.parse_args(args, namespace)

    def __set_path_name__(self):
        """Checks the file extension and sets dictionary name and output path"""
        self.dictionaryPath = os.path.dirname(self.dictionaryFile)
        dictionaryName, dictionaryExtension = os.path.splitext(os.path.basename(self.dictionaryFile))
        
        if dictionaryExtension.lower() != '.dsl':
            if self.verbose >= 1:
                sys.stdout.write ("Warning: input DSL dictionary file should have a .dsl extension.\n")
            dictionaryName = os.path.basename(self.dictionaryFile)
        
        if not self.dictionaryName:
            self.dictionaryName = dictionaryName
        
        if self.remote:
            self.outputDictionaryPath = os.path.join(self.dictionaryPath, self.dictionaryName)
        else:
            self.outputDictionaryPath = os.path.join(self.outputDictionaryPath, self.dictionaryName)


    def __init__(self, args=None, namespace=None):
        """1) Runs parse_args function
           2) Calls __set_path_name__,  but only if the parsed data is passed to itself"""
        self.parse_args(args, namespace)
        if not namespace:
            self.__set_path_name__()
        
    


    def open_input_files(self):
        """Searches for annotation and abbreviations, checks existence, opens the files for reading."""
        self.dictionaryFile = open(self.dictionaryFile, 'r', encoding=self.encoding)

        if self.annotationFile :
            self.annotationFile = open(self.annotationFile, 'r', encoding=self.encoding)
        elif self.annotationFile is None:
            try:
                self.annotationFile = open(os.path.join(self.dictionaryPath, self.dictionaryName + '.ann'), 'r', encoding=self.encoding)
            except FileNotFoundError:
                if self.verbose >= 2:
                    sys.stdout.write ("Warning: annotation file is not found.\n")

        if self.abbreviationsFile :
            self.abbreviationsFile = open(self.abbreviationsFile, 'r', encoding=self.encoding)
        elif self.abbreviationsFile is None:
            try:
                self.abbreviationsFile = open(os.path.join(self.dictionaryPath, self.dictionaryName + '_abrv.dsl'), 'r', encoding=self.encoding)
            except FileNotFoundError:
                if self.verbose >= 2:
                    sys.stdout.write ("Warning: abbreviations file is not found.\n")


    def open_output_files(self):
        """Checks existence of the output path and, opens the files for writing."""
        if not os.path.exists(self.outputDictionaryPath):
            os.makedirs(self.outputDictionaryPath)
        self.XMLfile = open(os.path.join(self.outputDictionaryPath, 'MyDictionary.xml'), 'w+', encoding='utf-8') # this is the output file
        self.Makefile = open(os.path.join(self.outputDictionaryPath, 'Makefile'), 'w+', encoding='utf-8')
        self.MyInfoFile = open(os.path.join(self.outputDictionaryPath, 'MyInfo.plist'), 'w+', encoding='utf-8')



def main():
    #ioDict = IOBridge()
    #ioDict.open_input_files()

    #print (ioDict.encoding)
    #print (ioDict.outputDictionaryPath)
    #print (ioDict.dictionaryName)
    #print (ioDict.dictionaryFile.name)
    #print (ioDict.annotationFile.name)
    #print (ioDict.abbreviationsFile.name)
    
    #print(ioDict.dictionaryFile.read(1).encode('raw_unicode_escape'))
    

    from . import dslconverter







if __name__ == "__main__":
    main()
