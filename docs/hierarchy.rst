=================================
Hierarchy of the called functions
=================================



| ``processDSLfile(file)``
|               reads till finds new entry
|  ↳ ``processDSLentry([lines])``
|               contains ``__index__`` should  return entry and data for referencing to the entry (for subentries)
|   ↳ ``processDSLentryhead([lines])``
|               should write to ``processDSLentry.__index__``
|   ↳ ``processDSLentrybody([lines])``
|               should search for subentries and call ``processDSLentry()``
|    ↳ ``processDSLbodyline(line)``
|     ↳ ``processDSLstring(string)``
|               contains ``__indexing__`` and ``__language__`` should write to ``processDSLentry.__index__``
|      ↳ ``__parse_tag__(match)``
|               always called for text between tags and should call ``processDSLstring()`` for it

