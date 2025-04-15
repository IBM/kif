# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ... import rdflib
from ...compiler.sparql import SPARQL_Mapping
from ...model import Filter, TGraph
from ...typing import Any, BinaryIO, TextIO
from .rdflib import RDFLibSPARQL_Store
from .sparql_core import _SPARQL_Store


class RDF_Store(
        RDFLibSPARQL_Store,
        store_name='rdf',
        store_description='RDF store'
):
    """RDF store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources.
       format: Input source format (file extension or media type).
       location: Relative or absolute IRI of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       rdflib_graph: RDFLib graph to be used as input source.
       skolemize: Whether to skolemize the resulting graph.
       mapping: SPARQL mapping.
       kwargs: Extra keyword arguments.
    """


class DBpediaRDF_Store(
        RDF_Store,
        store_name='dbpedia-rdf',
        store_description='DBpedia RDF store'
):
    """Alias for :class:`RDF_Store` with DBpedia mappings."""

    def __init__(
            self,
            store_name: str,
            *args: RDF_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._dbpedia_mapping_constructor()
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class PubChemRDF_Store(
        RDF_Store,
        store_name='pubchem-rdf',
        store_description='PubChem RDF store'
):
    """Alias for :class:`RDF_Store` with PubChem mappings."""

    def __init__(
            self,
            store_name: str,
            *args: RDF_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            normalize_casrn: bool | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._pubchem_mapping_constructor(
                normalize_casrn=normalize_casrn)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WikidataRDF_Store(
        RDF_Store,
        store_name='wikidata-rdf',
        store_description='Wikidata RDF store'
):
    """Alias for :class:`RDF_Store` with Wikidata mappings."""

    def __init__(
            self,
            store_name: str,
            *args: RDF_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=False,  # force
                strict=strict,
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)
