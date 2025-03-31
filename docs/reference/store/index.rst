.. currentmodule:: kif_lib

=====
Store
=====

.. inheritance-diagram::
   Store
   store.EmptyStore
   store.MixerStore
   store.HttpxSPARQL_Store
   store.RDFLibSPARQL_Store
   store.RDF_Store
   store.DBpediaRDF_Store
   store.PubChemRDF_Store
   store.WikidataRDF_Store
   store.SPARQL_Store
   store.DBpediaSPARQL_Store
   store.PubChemSPARQL_Store
   store.WikidataSPARQL_Store
   store.WDQS_Store
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
   store.MixerStore
   store.HttpxSPARQL_Store
   store.RDFLibSPARQL_Store
   store.RDF_Store
   store.DBpediaRDF_Store
   store.PubChemRDF_Store
   store.WikidataRDF_Store
   store.SPARQL_Store
   store.DBpediaSPARQL_Store
   store.PubChemSPARQL_Store
   store.WikidataSPARQL_Store
   store.WDQS_Store

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

   Store.ask
   Store.contains
   Store.count
   Store.filter
   Store.filter_annotated
