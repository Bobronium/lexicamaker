#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys
import argparse
from lexicamaker import __version__

def arguments_parser():
    parser = argparse.ArgumentParser(prog='adsmaker',
                                     description="Lexicamaker v%s - creates Apple Dictionary Service folder from DSL dictionary" % __version__,
                                     #usage='%(prog)s [options] DSL_FILE [OUTPUT_DIR]\n       %(prog)s [--help | --version]',
                                     epilog="The created Apple Dictionary Service folder must be then compiled with Apple Dictionary Development Kit")
    #parser.add_argument('dslfile', metavar='DSL_FILE', type=argparse.FileType('r', encoding='utf-16le'), help="a DSL dictionary file")
    parser.add_argument('dslfile', metavar='DSL_FILE', help="a DSL dictionary file")
    parser.add_argument('outdir', metavar='OUTPUT_DIR', nargs='?', help="a path for Apple Dictionary Service folder")
    parser.add_argument('-v', '--verbose', action='count', help="increase output verbosity")
    group = parser.add_argument_group('Fine tuning')
    subgroup1 = group.add_mutually_exclusive_group()
    subgroup1.add_argument('--no-annotation', action='store_false', help="Ignore annotation")
    #subgroup1.add_argument('--annotation', metavar='FILE', type=argparse.FileType('r', encoding='utf-16le'), help="annotation file")
    subgroup1.add_argument('--annotation', metavar='FILE', help="annotation file")
    #group.add_argument('--abbreviations', metavar='FILE', type=argparse.FileType('r', encoding='utf-16le'), help="abbreviations file")
    group.add_argument('--abbreviations', metavar='FILE', help="abbreviations file")
    subgroup2 = group.add_mutually_exclusive_group()
    subgroup2.add_argument('--no-media', action='store_true', help="Skip media")
    subgroup2.add_argument('--media', metavar='TYPE', type=str, help="Change media type to TYPE (supported wav, mp3, m4a)")
    parser.add_argument('--version', action='version', version="lexicamaker v%s" % __version__ ) #"%(prog)s v{}".format(__version__))
    return parser

def main():

    args = arguments_parser().parse_args()
    #   print (args)

    outputDictionaryPath, dictionaryExtension = os.path.splitext(args.dslfile)

    if dictionaryExtension.lower() != '.dsl':
        sys.stderr.write ("Warning: dictionary file does not have a .dsl extension.\n")
        outputDictionaryPath = args.dslfile
    
    dictionaryName = os.path.basename(outputDictionaryPath)
    
    if args.outdir != None:
        outputDictionaryPath = os.path.join(args.outdir, dictionaryName)

    dictionaryFile = open(args.dslfile, 'r', encoding='utf-16le')

    print (dictionaryFile)
    print (outputDictionaryPath)
    print (dictionaryName)





if __name__ == "__main__":
    main()
