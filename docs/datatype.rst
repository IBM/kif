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
   Datatype.from_value_class
   Datatype.to_value_class


Predefined instances
~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   Datatype.item
   Datatype.property
   Datatype.lexeme
   Datatype.iri
   Datatype.text
   Datatype.string
   Datatype.external_id
   Datatype.quantity
   Datatype.time


Concrete subclasses
~~~~~~~~~~~~~~~~~~~
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
