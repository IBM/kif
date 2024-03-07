===========
Descriptors
===========

.. currentmodule:: kif_lib

.. inheritance-diagram:: KIF_Object
                         Descriptor
                         PlainDescriptor
                         ItemDescriptor
                         PropertyDescriptor
                         LexemeDescriptor
   :top-classes: kif_lib.model.kif_object.KIF_Object
   :parts: -3
   :caption: Descriptor hierarchy.

Descriptor
----------
.. autosummary::
   :toctree: generated/

   Descriptor

PlainDescriptor
---------------
.. autosummary::
   :toctree: generated/

   PlainDescriptor

.. rubric:: Attributes
.. autosummary::
   :toctree: generated/

   PlainDescriptor.label
   PlainDescriptor.aliases
   PlainDescriptor.description

.. rubric:: Methods
.. autosummary::
   :toctree: generated/

   PlainDescriptor.get_label
   PlainDescriptor.get_aliases
   PlainDescriptor.get_description

ItemDescriptor
--------------
.. autosummary::
   :toctree: generated/

   ItemDescriptor

PropertyDescriptor
------------------
.. autosummary::
   :toctree: generated/

   PropertyDescriptor

Attributes
~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   PropertyDescriptor.datatype

Methods
~~~~~~~
.. autosummary::
   :toctree: generated/

   PropertyDescriptor.get_datatype

LexemeDescriptor
----------------
.. autosummary::
   :toctree: generated/

   LexemeDescriptor

Attributes
~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   LexemeDescriptor.lemma
   LexemeDescriptor.category
   LexemeDescriptor.language

Methods
~~~~~~~
.. autosummary::
   :toctree: generated/

   LexemeDescriptor.get_lemma
   LexemeDescriptor.get_category
   LexemeDescriptor.get_language
