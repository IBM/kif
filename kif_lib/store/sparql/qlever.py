# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib
import tempfile

from ... import functools, rdflib
from ...compiler.sparql import SPARQL_Mapping
from ...compiler.sparql.results import SPARQL_Results, SPARQL_ResultsAsk
from ...model import TGraph
from ...typing import (
    Any,
    BinaryIO,
    Optional,
    override,
    TextIO,
    TypeAlias,
    TypedDict,
)
from . import qlever_process
from .httpx import HttpxSPARQL_Store
from .sparql_core import _CoreSPARQL_Store, TCoreSPARQL_Store, TLocation


class PostInitIndexBuilderArgs(TypedDict):
    """Index builder arguments to be used in post-init step."""

    rebuild_index: bool
    args: list[TLocation]
    data: Optional[str]
    format: Optional[str]
    parse_parallel: Optional[bool]


class PostInitServerArgs(TypedDict):
    """Server arguments to be used in post-init step."""

    port: Optional[int]
    memory_max_size: Optional[float]
    default_query_timeout: Optional[int]
    throw_on_onbound_variables: Optional[bool]


class PostInitArgs(TypedDict):
    """Arguments to be used in post-init step."""

    basename: Optional[str]
    index_dir: Optional[TLocation]
    index_builder_args: PostInitIndexBuilderArgs
    server_args: PostInitServerArgs
    other_args: dict[str, Any]


class QLeverSPARQL_Store(
        _CoreSPARQL_Store,
        store_name='sparql-qlever',
        store_description='SPARQL store with QLever backend'
):
    """SPARQL store with QLever backend.

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

    class QLeverBackend(_CoreSPARQL_Store.LocalBackend):
        """QLever backend.

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

        #: QLever process handle (singleton).
        _qlever: qlever_process.QLever

        #: Post-init arguments.
        _post_init_args: PostInitArgs

        #: The underlying httpx backend.
        _httpx_backend: HttpxSPARQL_Store.HttpxBackend

        #: Temporary directory used to hold transient index files.
        _temp_dir: Any | None

        #: Temporary file used to hold transient RDF data.
        _temp_skolem_graph: Any | None

        __slots__ = (
            '_httpx_backend',
            '_post_init_args',
            '_qlever',
            '_temp_dir',
            '_temp_skolem_graph',
        )

        @override
        def _pre_init(
                self,
                store: TCoreSPARQL_Store,
                basename: str | None = None,
                index_dir: TLocation | None = None,
                rebuild_index: bool | None = None,
                parse_parallel: bool | None = None,
                port: int | None = None,
                memory_max_size: float | None = None,
                default_query_timeout: int | None = None,
                throw_on_onbound_variables: bool | None = None,
                index_builder_path: TLocation | None = None,
                server_path: TLocation | None = None,
                **kwargs: Any
        ) -> None:
            with self._lock:
                try:
                    self._qlever = qlever_process.QLever(
                        index_builder_path,
                        server_path)
                except qlever_process.QLever.Error as err:
                    raise store.Error(err) from err
                if basename is None or index_dir is None:
                    rebuild_index = True
                self._post_init_args = {
                    'basename': basename,
                    'index_dir': index_dir,
                    'index_builder_args': {
                        'rebuild_index': bool(rebuild_index),
                        'args': [],
                        'data': None,
                        'format': None,
                        'parse_parallel': parse_parallel,
                    },
                    'server_args': {
                        'port': port,
                        'memory_max_size': memory_max_size,
                        'default_query_timeout': default_query_timeout,
                        'throw_on_onbound_variables': (
                            throw_on_onbound_variables),
                    },
                    'other_args': kwargs,
                }
                self._temp_dir = None
                self._temp_skolem_graph = None

        @override
        def _post_init(self, store: TCoreSPARQL_Store, **kwargs) -> None:
            basename = self._post_init_args['basename']
            index_dir = self._post_init_args['index_dir']
            index_builder_args = self._post_init_args['index_builder_args']
            server_args = self._post_init_args['server_args']
            other_args = self._post_init_args['other_args']
            if index_builder_args['rebuild_index']:
                if index_dir is None:
                    self._temp_dir = tempfile.TemporaryDirectory()
                    index_dir = pathlib.Path(self._temp_dir.name)
                if basename is None:
                    basename = pathlib.Path(index_dir).stem
                self._post_init_args['basename'] = basename
                self._post_init_args['index_dir'] = index_dir
                t = index_builder_args
                self._qlever.build_index(
                    basename, *t['args'],
                    data=t['data'],
                    format=t['format'],
                    index_dir=index_dir,
                    parse_parallel=t['parse_parallel'])
            assert index_dir is not None
            assert basename is not None
            with self._lock:
                port = self._qlever.start(
                    basename=basename, index_dir=index_dir, **server_args)
                self._httpx_backend = HttpxSPARQL_Store.HttpxBackend(
                    self._store, f'http://localhost:{port}/', **other_args)

        @override
        def _load_location(
                self,
                location: TLocation,
                format: str | None = None
        ) -> None:
            with self._lock:
                t = self._post_init_args['index_builder_args']
                if format is not None:
                    t['format'] = format
                self._post_init_args['index_builder_args']['args'].append(
                    location)

        @override
        def _load_data(
                self,
                data: bytes | str,
                format: str | None = None
        ) -> None:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            with self._lock:
                t = self._post_init_args['index_builder_args']
                if format is not None:
                    t['format'] = format
                if t['data'] is None:
                    t['data'] = data
                else:
                    t['data'] += data

        @override
        def _skolemize(self) -> None:
            from ...rdflib import Graph
            t = self._post_init_args['index_builder_args']
            g = Graph()
            parse = functools.partial(g.parse, format=t['format'])
            for arg in t['args']:
                parse(arg)
            if t['data'] is not None:
                parse(data=t['data'])
            self._temp_skolem_graph = tempfile.NamedTemporaryFile()
            g.skolemize().serialize(self._temp_skolem_graph.name, format='n3')
            t['args'] = [self._temp_skolem_graph.name]
            t['data'] = None
            t['format'] = 'nt'

        @override
        def _close(self) -> None:
            self._httpx_backend.close()
            with self._lock:
                if self._temp_dir is not None:
                    self._temp_dir.cleanup()
                if self._temp_skolem_graph is not None:
                    self._temp_skolem_graph.close()
                self._qlever.stop()

        @override
        async def _aclose(self) -> None:
            await self._httpx_backend.aclose()

        @override
        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return self._httpx_backend.ask(query)

        @override
        async def _aask(self, query: str) -> SPARQL_ResultsAsk:
            return await self._httpx_backend.aask(query)

        @override
        def _select(self, query: str) -> SPARQL_Results:
            return self._httpx_backend._select(query)

        @override
        async def _aselect(self, query: str) -> SPARQL_Results:
            return await self._httpx_backend._aselect(query)

        @override
        def _set_timeout(self, timeout: float | None = None) -> None:
            self._httpx_backend._set_timeout(timeout)

    #: Type alias for QLever SPARQL store arguments.
    Args: TypeAlias = QLeverBackend.Args

    def __init__(
            self,
            store_name: str,
            *args: QLeverSPARQL_Store.Args,
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
            self.QLeverBackend, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize, **kwargs)
