DSL specifocation
=============================================================================


Introduction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a converter for Lingvo .dsl dictionaries to Apple Dictionary Services format. 

General:

{{, }} - comment, for example, {{this is a comment}}

Entry headword:

{, } - unsorted part of a headword, for example, {to }have, CO{[sub]}2{[/sub]}-Laser

(, ) - optional part of a headword, for example, convert(ing)

\ - backslash to use the special symbols {}()@~^ in the headword, for example, \{, \@, \~

Entry body:

@ - subentry

~, ^~ - retyped the headword




[mN], [/m] - sets the left paragraph margin. N is the number of spaces which will be used for the left-hand margin. N must be within the range from 0 to 9. The corresponding closing tag of the paragraph is [/m]. and left card margin.

[*], [/*]  - the text between these tags is only displayed in full translation mode (see)




[b], [/b] - boldfaced font

[i], [/i] - italics

[u], [/u] - underlined font

[c], [c color], [/c] - coloured (highlighted) font, if color is missing, it is set to default colored (green).

[sub][/sub] - subscript

[sup][/sup] -  superscript

['],[/'] - a stressed vowel in a word.

[p], [/p] - labels (clicking a label displays its full text)



[trn], [/trn] - translations zone.

[ex], [/ex] - examples zone.

[com], [/com] - comments zone.

[t], [/t] - transcription

[s], [/s] - multimedia zone (used to add pictures or sound files into a dictionary entries ).

[!trs], [/!trs] - the text between these tags will not be indexed





[ref], [ref dict="Dictionary"], <<, [/ref], >> - hyperlink to a card in the same dictionary, or in dictionary Dictionary. You can also use "<<" and ">>" to enclose the headword of the card to make a link)

[lang], [lang name="language"], [/lang] - the language of the word or phrase
