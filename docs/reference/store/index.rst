.. currentmodule:: kif_lib

=====
Store
=====

.. inheritance-diagram::
   Store
   store.EmptyStore
   store.SPARQL_Store
   store.WikidataStore
   store.RDF_Store
   store.SPARQL_MapperStore
   store.MixerStore
   :top-classes: kif_lib.store.abc.Store
   :parts: 1
   :caption: Store classes.

.. toctree::
   :hidden:

   store

.. autosummary::
   :nosignatures:

   Store
   store.EmptyStore
   store.SPARQL_Store
   store.WikidataStore
   store.RDF_Store
   store.SPARQL_MapperStore
   store.MixerStore

Properties
==========

.. rubric:: Extra references

.. autosummary::
   :nosignatures:

   Store.extra_references
   Store.default_extra_references

.. rubric:: Flags

.. autosummary::
   :nosignatures:

   Store.flags
   Store.default_flags
   Store.has_flags
   Store.set_flags
   Store.unset_flags

.. rubric:: Limit

.. autosummary::
   :nosignatures:

   Store.limit
   Store.max_limit
   Store.default_limit

.. rubric:: Page size

.. autosummary::
   :nosignatures:

   Store.page_size
   Store.default_page_size
   Store.max_page_size

.. rubric:: Timeout

.. autosummary::
   :nosignatures:

   Store.timeout
   Store.default_timeout
   Store.max_timeout

Methods
=======

.. autosummary::
   :nosignatures:

   Store.match
   Store.filter
   Store.filter_annotated
