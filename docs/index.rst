=================================
Indexing
=================================


Initial string
``
zero [ex] one [!trs] two [ex] three [!trs] four [/!trs] five [/ex] six [/!trs] seven [/ex] eight
``

We do hard skip ``one seven`` not soft one ``one three five seven``

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
``[p], [/p]``
labels (clicking a label displays its full text) _automatically excluded from the indexing_
``[lang], [lang name="language"], [lang id=code], [/lang]``
the language of the word or phrase

