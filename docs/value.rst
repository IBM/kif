=====
Value
=====

.. currentmodule:: kif_lib

.. inheritance-diagram:: KIF_Object
                         DataValue
                         DeepDataValue
                         Entity
                         ExternalId
                         IRI
                         Item
                         Lexeme
                         Property
                         Quantity
                         ShallowDataValue
                         String
                         Text
                         Time
                         Value
   :top-classes: kif_lib.model.kif_object.KIF_Object
   :parts: -3
   :caption: Value hierarchy.

Value
-----
.. autosummary::
   :toctree: generated/

   Value.mask
   Value.value
   Value.n3

Mask
~~~~
.. autosummary::
   :toctree: generated/

   Value.ITEM
   Value.PROPERTY
   Value.LEXEME
   Value.IRI
   Value.TEXT
   Value.STRING
   Value.EXTERNAL_ID
   Value.QUANTITY
   Value.TIME
   Value.ENTITY
   Value.SHALLOW_DATA_VALUE
   Value.DEEP_DATA_VALUE
   Value.DATA_VALUE
   Value.ALL

Entity
------
.. autosummary::
   :toctree: generated/

   Entity
   Entity.iri

Item
~~~~
.. autosummary::
   :toctree: generated/

   Item
   Items

Property
~~~~~~~~
.. autosummary::
   :toctree: generated/

   Property
   Properties

Lexeme
~~~~~~
.. autosummary::
   :toctree: generated/

   Lexeme
   Lexemes

DataValue
---------
.. autosummary::
   :toctree: generated/

   DataValue

ShallowDataValue
----------------
.. autosummary::
   :toctree: generated/

   ShallowDataValue

IRI
~~~
.. autosummary::
   :toctree: generated/

   IRI

Text
~~~~
.. autosummary::
   :toctree: generated/

   Text
   Text.language

String
~~~~~~
.. autosummary::
   :toctree: generated/

   String

ExternalId
~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   ExternalId

DeepDataValue
-------------
.. autosummary::
   :toctree: generated/

   DeepDataValue

Quantity
~~~~~~~~
.. autosummary::
   :toctree: generated/

   Quantity
   Quantity.amount
   Quantity.unit
   Quantity.lower_bound
   Quantity.upper_bound

Time
~~~~
.. autosummary::
   :toctree: generated/

   Time
   Time.time
   Time.precision
   Time.timezone
   Time.calendar_model

Precision
"""""""""
.. autosummary::
   :toctree: generated/

   Time.BILLION_YEARS
   Time.HUNDRED_MILLION_YEARS
   Time.TEN_MILLION_YEARS
   Time.MILLION_YEARS
   Time.HUNDRED_MILLION_YEARS
   Time.TEN_THOUSAND_YEARS
   Time.MILLENNIA
   Time.CENTURY
   Time.DECADE
   Time.YEAR
   Time.MONTH
   Time.DAY
   Time.HOUR
   Time.MINUTE
   Time.SECOND
