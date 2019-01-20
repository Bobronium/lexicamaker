#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .context import lexicamaker

#import lexicamaker.adsmaker
#lexicamaker.__main__.main()


#__main__.main()




def setup_function(function):
    print("setting up %s" % function)

def test_something():
    print("TEST!!!!")
    assert 1

def test_something_else():
    print("TEST 2!!!!")
    assert 1

def test_import():
    print("TEST import!!!!")
    from lexicamaker import __main__
    assert __main__.cmd_enc()=="no"

