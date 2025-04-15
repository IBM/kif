# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from ... import itertools, rdflib
from ...compiler.sparql import SPARQL_Mapping
from ...model import Filter, IRI, T_IRI, TGraph
from ...typing import Any, BinaryIO, Iterator, TextIO, TypeAlias
from ..abc import Store
from ..mixer import MixerStore
from .rdf import RDF_Store
from .sparql_core import _SPARQL_Store


class SPARQL_Store(
        MixerStore,
        store_name='sparql',
        store_description='SPARQL store'
):
    """SPARQL store.

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

    #: Type alias for SPARQL Store arguments.
    Args: TypeAlias = T_IRI | RDF_Store.Args

    @classmethod
    def _is_http_or_https_iri(
            cls,
            arg: Args,
            _re: re.Pattern = re.compile(r'^http[s]?://')
    ) -> bool:
        content: str
        if isinstance(arg, IRI):
            content = arg.content
        elif isinstance(arg, rdflib.URIRef):
            content = str(arg)
        elif isinstance(arg, str):
            content = arg
        else:
            return False
        return bool(_re.match(content))

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
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
        other, iris = map(list, itertools.partition(
            self._is_http_or_https_iri, args))

        def it() -> Iterator[Store]:
            for iri in iris:
                yield Store('sparql-httpx', iri, mapping=mapping, **kwargs)
            if (other
                    or location is not None
                    or file is not None
                    or data is not None
                    or graph is not None
                    or rdflib_graph is not None):
                yield Store(
                    'rdf', *other, format=format,
                    location=location, file=file, data=data, graph=graph,
                    rdflib_graph=rdflib_graph, skolemize=skolemize,
                    mapping=mapping, **kwargs)
        super().__init__(store_name, list(it()), **kwargs)


class DBpediaSPARQL_Store(
        SPARQL_Store,
        store_name='dbpedia-sparql',
        store_description='DBpedia SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with DBpedia mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
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
        if not args:
            resolver_iri = self.context.options.vocabulary.db.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._dbpedia_mapping_constructor()
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class PubChemSPARQL_Store(
        SPARQL_Store,
        store_name='pubchem-sparql',
        store_description='PubChem SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with PubChem mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
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
        if not args:
            resolver_iri = self.context.options.vocabulary.pc.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._pubchem_mapping_constructor(
                normalize_casrn=normalize_casrn)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WikidataSPARQL_Store(
        SPARQL_Store,
        store_name='wikidata-sparql',
        store_description='Wikidata SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with Wikidata mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            blazegraph: bool | None = None,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if not args:
            resolver_iri = self.context.options.vocabulary.wd.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=blazegraph,
                strict=strict,
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WDQS_Store(
        WikidataSPARQL_Store,
        store_name='wdqs',
        store_description='Wikidata query service store'
):
    """Alias for :class:`WikidataSPARQL_Store` with stricter mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=True,  # force
                strict=True,      # force
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)
