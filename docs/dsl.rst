=================
DSL specification
=================

Introduction
============

This is a converter for Lingvo .dsl dictionaries to Apple Dictionary Services format.

Format short description
========================

Special symbols
---------------

General:
~~~~~~~~

``{{, }}``
comment, for example, ``{{this is a comment}}`` but single ``{, }`` are literals in bodies only, but are special in headwords
``#``
preprocessor directive

Entry headwords:
~~~~~~~~~~~~~~~

``{, }``
unsorted part of a headword, for example, ``{to }have``, ``CO{[sub]}2{[/sub]}-Laser``, in body are literals
``(, )``
optional part of a headword, for example, ``convert(ing)``, in body are literals
``\``
backslash to use the special symbols ``{}()@~^`` in the headword, for example, ``\{``, ``\@``, ``\~``

Entry body:
~~~~~~~~~~~

``@``
subentry
``~, ^~``
retyped the headword
``[, ]``
tags, but double ``[[`` is treated as single non-tag symbol ``[`` i.e is equivalent to ``\[``
``\``
backslash to use the special symbols ``{}()@~^`` in the body, for example, ``\{``, ``\@``, ``\~``
``<<, >>``
referencing
``[[, ]]``
treated as single non-tag symbol ``[, ]`` but should not followed by a tag without a space

Tags
----

Standard paragraphing tags:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``[mN], [/m]``
sets the left paragraph margin. N is the number of spaces which will be used for the left-hand margin. N must be within the range from 0 to 9. The corresponding closing tag of the paragraph is ``[/m]``. and left card margin.
``[*], [/*]``
the text between these tags is only displayed in full translation mode (see)

Standard markup tags:
~~~~~~~~~~~~~~~~~~~~~

``[b], [/b]``
boldfaced font
``[i], [/i]``
italics
``[u], [/u]``
underlined font
``[c], [c color], [/c]``
coloured (highlighted) font, if color is missing, it is set to default colored (green).
``[sub], [/sub]``
subscript
``[sup][/sup]``
superscript
``['], [/']``
a stressed vowel in a word.
``[p], [/p]``
labels (clicking a label displays its full text) _automatically excluded from the indexing_
``[t], [/t]``
transcription

Indexing tags:
~~~~~~~~~~~~~~

``[trn], [/trn]``
translations zone
``[ex], [/ex]``
examples zone
``[com], [/com]``
comments zone
``[!trs], [/!trs]``
the text between these tags will not be indexed
``[lang], [lang name="language"], [lang id=code], [/lang]``
the language of the word or phrase

Reference tags:
~~~~~~~~~~~~~~~

``[ref], [ref dict="Dictionary"], <<, [/ref], >>``
hyperlink to a card in the same dictionary, or in dictionary Dictionary. You can also use ``<<`` and ``>>`` to enclose the headword of the card to make a link)
``[s], [/s]``
multimedia zone (used to add pictures or sound files into a dictionary entries).
``[url], [/url]``
forms an URL link
