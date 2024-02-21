==========
Plugin API
==========

.. currentmodule:: kif_lib

.. inheritance-diagram:: Store
                         kif_lib.store.empty.EmptyStore
                         kif_lib.store.mixer.MixerStore
                         kif_lib.store.rdf.RDF_Store
                         kif_lib.store.mapper.SPARQL_MapperStore
                         kif_lib.store.sparql.SPARQL_Store
   :top-classes: kif_lib.store.abc.Store
   :parts: -3
   :caption: Store plugin hierarchy.

Identification
--------------
.. autosummary::
   Store.store_name
   Store.store_description
   Store.registry

Internal API
------------

Error handling
~~~~~~~~~~~~~~
.. autosummary::
   Store._error
   Store._must_be_implemented_in_subclass
   Store._should_not_get_here

Caching
~~~~~~~
.. autosummary::
   Store._cache
   Store._cache_get_presence
   Store._cache_set_presence

Pagination
~~~~~~~~~~
.. autosummary::
   Store.maximum_page_size
   Store._batched

Timeout
~~~~~~~
.. autosummary::
   Store.maximum_timeout

Built-in stores
---------------

.. currentmodule:: kif_lib.store

EmptyStore
~~~~~~~~~~
.. autosummary::
   EmptyStore

MixerStore
~~~~~~~~~~
.. autosummary::
   MixerStore
   MixerStore.sources
   MixerStore.sync_flags

RDF_Store
~~~~~~~~~
.. autosummary::
   RDF_Store

SPARQL_MapperStore
~~~~~~~~~~~~~~~~~~
.. autosummary::
   SPARQL_MapperStore
   SPARQL_MapperStore.mapping

SPARQL_Store
~~~~~~~~~~~~
.. autosummary::
   SPARQL_Store
   SPARQL_Store.iri
