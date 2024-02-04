=====
Value
=====

.. currentmodule:: kif_lib

.. inheritance-diagram:: Value Entity Item Property Lexeme DataValue IRI Text
                         String ExternalId DeepDataValue Quantity Time
   :top-classes: kif_lib.model.value.Value
   :parts: -3
   :caption: Value hierarchy.

Value
-----

.. autosummary::
   :toctree: generated/

   Value
   Value.get_datatype
   Value.value
   Value.get_value
   Value.n3

Entity
------

.. autosummary::
   :toctree: generated/

   Entity
   Entity.iri
   Entity.get_iri

Item
~~~~

.. autosummary::
   :toctree: generated/

   Item
   Item.datatype
   Items

Property
~~~~~~~~

.. autosummary::
   :toctree: generated/

   Property
   Property.datatype
   Properties

Lexeme
~~~~~~

.. autosummary::
   :toctree: generated/

   Lexeme
   Lexeme.datatype
   Lexemes

Data Value
----------

.. autosummary::
   :toctree: generated/

   DataValue

IRI
~~~

.. autosummary::
   :toctree: generated/

   IRI
   IRI.datatype

Text
~~~~

.. autosummary::
   :toctree: generated/

   Text
   Text.datatype

String
~~~~~~

.. autosummary::
   :toctree: generated/

   String
   String.datatype

ExternalId
~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   ExternalId
   ExternalId.datatype

Deep Data Value
---------------

.. autosummary::
   :toctree: generated/

   DeepDataValue

Quantity
~~~~~~~~

.. autosummary::
   :toctree: generated/

   Quantity
   Quantity.datatype
   Quantity.amount
   Quantity.get_amount
   Quantity.unit
   Quantity.get_unit
   Quantity.lower_bound
   Quantity.get_lower_bound
   Quantity.upper_bound
   Quantity.get_upper_bound

Time
~~~~

.. autosummary::
   :toctree: generated/

   Time
   Time.datatype
   Time.time
   Time.get_time
   Time.precision
   Time.get_precision
   Time.timezone
   Time.get_timezone
   Time.calendar_model
   Time.get_calendar_model
