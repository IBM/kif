=======
Plugins
=======

.. currentmodule:: kif_lib.store

.. inheritance-diagram:: Store
                         EmptyStore
                         MixerStore
                         RDF_Store
                         SPARQL_MapperStore
                         SPARQL_Store
   :top-classes: kif_lib.store.abc.Store
   :parts: -3
   :caption: Store plugin hierarchy.

Internal API
------------
.. autosummary::
   :toctree: generated/

   Store.store_name
   Store.store_description
   Store.registry

Error
~~~~~
.. autosummary::
   :toctree: generated/

   Store._error
   Store._must_be_implemented_in_subclass
   Store._should_not_get_here

Built-in stores
---------------

EmptyStore
~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   EmptyStore

MixerStore
~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   MixerStore

RDF_Store
~~~~~~~~~
.. autosummary::
   :toctree: generated/

   RDF_Store

SPARQL_MapperStore
~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   SPARQL_MapperStore

SPARQL_Store
~~~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   SPARQL_Store
