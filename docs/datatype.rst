========
Datatype
========

.. currentmodule:: kif_lib

.. inheritance-diagram:: KIF_Object
                         Datatype
                         ExternalIdDatatype
                         IRI_Datatype
                         ItemDatatype
                         LexemeDatatype
                         PropertyDatatype
                         QuantityDatatype
                         StringDatatype
                         TextDatatype
                         TimeDatatype
   :top-classes: kif_lib.model.kif_object.KIF_Object
   :parts: -3
   :caption: Datatype hierarchy.

Datatype
--------
.. autosummary::
   :toctree: generated/

   Datatype

Attributes
~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   Datatype.external_id
   Datatype.iri
   Datatype.item
   Datatype.lexeme
   Datatype.property
   Datatype.quantity
   Datatype.string
   Datatype.text
   Datatype.time

Methods
~~~~~~~
.. autosummary::
   :toctree: generated/

   Datatype.from_value_class
   Datatype.to_value_class

Concrete subclasses
-------------------
.. autosummary::
   :toctree: generated/

   ItemDatatype
   PropertyDatatype
   LexemeDatatype
   IRI_Datatype
   TextDatatype
   StringDatatype
   ExternalIdDatatype
   QuantityDatatype
   TimeDatatype
