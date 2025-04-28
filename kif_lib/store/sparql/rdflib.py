# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import pathlib

from ... import rdflib
from ...compiler.sparql import SPARQL_Mapping
from ...compiler.sparql.results import SPARQL_Results
from ...model import TGraph
from ...typing import Any, BinaryIO, cast, override, TextIO, TypeAlias
from .sparql_core import _SPARQL_Store


class RDFLibSPARQL_Store(
        _SPARQL_Store,
        store_name='sparql-rdflib',
        store_description='SPARQL store with RDFLib backend'
):
    """SPARQL store with RDFLib backend.

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

    class RDFLibBackend(_SPARQL_Store.LocalBackend):
        """RDFLib backend.

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
            '_rdflib_graph',
        )

        #: RDFLib graph.
        _rdflib_graph: rdflib.Graph

        def _init(
                self,
                store: _SPARQL_Store,
                **kwargs: Any
        ) -> None:
            self._rdflib_graph = rdflib.Graph()

        @override
        def _load_arg_unknown(
                self,
                arg: Any,
                format: str | None = None
        ) -> None:
            with self._lock:
                self._rdflib_graph.parse(arg, format=format)  # type: ignore

        @override
        def _load_location(
                self,
                location: pathlib.PurePath | str,
                format: str | None = None
        ) -> None:
            with self._lock:
                self._rdflib_graph.parse(
                    location=str(location), format=format)

        @override
        def _load_file(
                self,
                file: BinaryIO | TextIO,
                format: str | None = None
        ) -> None:
            with self._lock:
                self._rdflib_graph.parse(file=file, format=format)

        @override
        def _load_data(
                self,
                data: bytes | str,
                format: str | None = None
        ) -> None:
            with self._lock:
                self._rdflib_graph.parse(data=data, format=format)

        @override
        def _skolemize(self) -> None:
            with self._lock:
                self._rdflib_graph = self._rdflib_graph.skolemize()

        @override
        def _select(self, query: str) -> SPARQL_Results:
            with self._lock:
                res = self._rdflib_graph.query(query)
            return json.loads(cast(bytes, res.serialize(format='json')))

    #: Type alias for RDFLib SPARQL store arguments.
    Args: TypeAlias = RDFLibBackend.Args

    def __init__(
            self,
            store_name: str,
            *args: Args,
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
            self.RDFLibBackend, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize, **kwargs)
