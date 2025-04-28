# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib

from ... import rdflib
from ...compiler.sparql import SPARQL_Mapping
from ...compiler.sparql.results import SPARQL_Results, SPARQL_ResultsAsk
from ...model import IRI, TGraph
from ...typing import Any, BinaryIO, cast, override, TextIO, TypeAlias
from . import jena_jpype
from .sparql_core import _SPARQL_Store


class JenaSPARQL_Store(
        _SPARQL_Store,
        store_name='sparql-jena',
        store_description='SPARQL store with Jena backend'
):
    """SPARQL store with Jena backend.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources.
       format: Input source format (file extension or media type).
       location: Relative or absolute URL of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       rdflib_graph: RDFLib graph to be used as input source.
       skolemize: Whether to skolemize the resulting graph.
       mapping: SPARQL mapping.
       kwargs: Other keyword arguments.
    """

    class JenaBackend(_SPARQL_Store.LocalBackend):
        """Jena backend.

        Parameters:
           store: Parent SPARQL store.
           args: Input sources, files, paths, strings, or statements.
           format: Input source format (file extension or media type).
           location: Relative or absolute URL of the input source.
           file: File-like object to be used as input source.
           data: Data to be used as input source.
           graph: KIF graph to used as input source.
           rdflib_graph: RDFLib graph to be used as input source.
           skolemize: Whether to skolemize the resulting graph.
           kwargs: Other keyword arguments.
        """

        __slots__ = (
            '_jena',
        )

        #: Jena handle.
        _jena: jena_jpype.Jena

        @override
        def _init(
                self,
                store: _SPARQL_Store,
                **kwargs: Any
        ) -> None:
            jena_home = IRI.check_optional(
                kwargs.get('jena_home'), None, type(store), 'jena_home')
            try:
                self._jena = jena_jpype.Jena(
                    jena_home.content if jena_home is not None else None)
            except BaseException as err:
                raise store._error(
                    f'failed to create Jena backend ({err})') from err

        @override
        def _load_location(
                self,
                location: pathlib.PurePath | str,
                format: str | None = None
        ) -> None:
            with self._lock:
                self._jena.load(location, format)

        @override
        def _load_data(
                self,
                data: bytes | str,
                format: str | None = None
        ) -> None:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            with self._lock:
                self._jena.loads(data, format)

        @override
        def _skolemize(self) -> None:
            with self._lock:
                self._jena.skolemize()

        @override
        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return {'boolean': cast(bool, self._select(query))}

        @override
        def _select(self, query: str) -> SPARQL_Results:
            with self._lock:
                return cast(SPARQL_Results, self._jena.query(query))

    #: Type alias for Jena SPARQL store arguments.
    Args: TypeAlias = JenaBackend.Args

    def __init__(
            self,
            store_name: str,
            *args: JenaSPARQL_Store.Args,
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
        super().__init__(
            store_name,
            (mapping if mapping is not None
             else self._wikidata_mapping_constructor()),
            self.JenaBackend, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize, **kwargs)
