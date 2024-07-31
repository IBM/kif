===
All
===

.. currentmodule:: kif_lib

Datatype
--------

.. autoclass:: Datatype
   :no-index:
   :show-inheritance:

.. autoclass:: ItemDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: PropertyDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: LexemeDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: IRI_Datatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: TextDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: StringDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: ExternalIdDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: QuantityDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

.. autoclass:: TimeDatatype
   :members: value_class, variable_class
   :no-index:
   :show-inheritance:

Value
-----

.. autoclass:: Value
   :members: value, get_value, n3
   :no-index:
   :show-inheritance:

.. autoclass:: Entity
   :members: iri, get_iri
   :no-index:
   :show-inheritance:

.. autoclass:: Item
   :members: datatype_class, datatype
   :no-index:
   :show-inheritance:

.. autoclass:: Property
   :members: datatype_class, datatype, range, get_range
   :no-index:
   :show-inheritance:

.. autoclass:: Lexeme
   :members: datatype_class, datatype
   :no-index:
   :show-inheritance:

.. autoclass:: DataValue
   :no-index:
   :show-inheritance:

.. autoclass:: ShallowDataValue
   :members: content, get_content
   :no-index:
   :show-inheritance:

Snak
----

.. autoclass:: Snak
   :members: mask, get_mask, property, get_property
   :no-index:
   :show-inheritance:

.. autoclass:: ValueSnak
   :members: value, get_value
   :no-index:
   :show-inheritance:

.. autoclass:: SomeValueSnak
   :members:
   :no-index:
   :show-inheritance:

.. autoclass:: NoValueSnak
   :members:
   :no-index:
   :show-inheritance:

Statement
---------

.. autoclass:: Statement
   :members: subject, get_subject, snak, get_snak
   :no-index:
   :show-inheritance:
