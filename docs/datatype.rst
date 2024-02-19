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

.. autosummary::
   Datatype

Concrete subclasses
-------------------
.. autosummary::
   ItemDatatype
   PropertyDatatype
   LexemeDatatype
   IRI_Datatype
   TextDatatype
   StringDatatype
   ExternalIdDatatype
   QuantityDatatype
   TimeDatatype

Value-class conversion
----------------------
.. autosummary::
   Datatype.from_value_class
   Datatype.to_value_class
