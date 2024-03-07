==========
KIF Object
==========

.. currentmodule:: kif_lib

.. inheritance-diagram:: kif_lib.model.object.Object
                         KIF_Object
   :top-classes: kif_lib.model.object.Object
   :parts: -3
   :caption: KIF_Object hierarchy.

.. autosummary::
   KIF_Object
   KIF_Object.Nil
   KIF_Object.args
   KIF_Object.digest

Argument checking
-----------------
.. autosummary::
   KIF_Object.check
   KIF_Object.check_optional
   KIF_Object.test

Argument unpacking
------------------
.. autosummary::
   KIF_Object.unpack

Copying
-------
.. autosummary::
   KIF_Object.copy
   KIF_Object.deepcopy
   KIF_Object.replace

Encoding
--------
.. autosummary::
   KIF_Object.dump
   KIF_Object.dumps
   KIF_Object.to_json
   KIF_Object.to_markdown
   KIF_Object.to_sexp

Decoding
--------
.. autosummary::
   KIF_Object.from_json
   KIF_Object.from_sexp
   KIF_Object.from_sparql
   KIF_Object.load
   KIF_Object.loads
