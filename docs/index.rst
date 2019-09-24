=================================
Indexing
=================================


Initial string:
::
zero [ex] one [!trs] two [ex] three [!trs] four [/!trs] five [/ex] six [/!trs] seven [/ex] eight

We do hard skip ``one seven`` not soft one ``one three five seven``

Indexing tags:
~~~~~~~~~~~~~~

* ``[trn], [/trn]`` translations zone
* ``[ex], [/ex]`` examples zone
* ``[com], [/com]`` comments zone
* ``[!trs], [/!trs]`` the text between these tags will not be indexed
* ``[p], [/p]`` labels (clicking a label displays its full text) *automatically excluded from the indexing*
* ``[lang], [lang name="language"], [lang id=code], [/lang]`` the language of the word or phrase


String processing:
~~~~~~~~~~~~~~~~~~

Input strings:
::
1) [ex] [lang name="Latin"]id est[/lang] - that is[/ex]
2) [ex] [lang name="Latin"]et cetera[/lang] - and the rest[/ex]
3) [ex] [lang name="Latin"][!trs]mea [\!trs]alma mater[/lang] - and the rest[/ex]

Let's run the function ``processDSLstring(string, lang="English", index=False)``. We should get

.. code-block:: html

1) <span class="ex" id="id01"> id est - that is</span>
2) <span class="ex" id="id02"> et cetera - and the rest</span>
3) <span class="ex" id="id03"> mea alma mater - and the rest</span>

.. code-block:: python
:emphasize-lines: 1

{ 'id01': 'id est', 'id02': 'et cetera', 'id03': 'alma mater']

Tag pair ``[lang name="LanguageName"]string[/lang] calls function ``processDSLstring(string, lang="LanguageName", index)`` with value of ``index`` inherited from the calling function.
If ``index`` is *not* ``False``, but ``"idxid"`` and the ``lang`` coincides with ``index_language`` then ``string`` is added to element ``"idxid"`` in the dictionary.
