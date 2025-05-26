# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib
import re
import tempfile

from ... import rdflib
from ...compiler.sparql import SPARQL_Mapping
from ...compiler.sparql.results import SPARQL_Results, SPARQL_ResultsAsk
from ...model import TGraph
from ...typing import Any, BinaryIO, ClassVar, override, TextIO, TypeAlias
from . import rdfox_pipe
from .httpx import HttpxSPARQL_Store
from .sparql_core import _SPARQL_Store


class RDFoxSPARQL_Store(
        _SPARQL_Store,
        store_name='sparql-rdfox',
        store_description='SPARQL store with RDFox backend'
):
    """SPARQL store with RDFox backend.

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

    class RDFoxBackend(_SPARQL_Store.LocalBackend):
        """RDFox backend.

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

        #: RDFox process handle (singleton).
        _rdfox: ClassVar[rdfox_pipe.RDFox | None] = None

        #: The underlyin httpx backend.
        _httpx_backend: HttpxSPARQL_Store.HttpxBackend

        #: RDFox data store name for this backend.
        _name: str

        __slots__ = (
            '_httpx_backend',
            '_name',
        )

        @property
        def rdfox(self) -> rdfox_pipe.RDFox:
            """The RDFox process handle."""
            assert self._rdfox is not None
            return self._rdfox

        @override
        def _init(
                self,
                store: _SPARQL_Store,
                **kwargs: Any
        ) -> None:
            if self._rdfox is None:
                with self._lock:
                    try:
                        type(self)._rdfox = rdfox_pipe.RDFox()
                        self.rdfox.set(
                            'endpoint.port', kwargs.get('port', 12110))
                        self.rdfox.endpoint_start()
                    except BaseException as err:
                        raise store._error(
                            f'failed to create RDFox backend ({err})') from err
            self._name = 'ds' + str(id(self))
            with self._lock:
                self.rdfox.dstore_create(self._name)
                port = self.rdfox.set('endpoint.port')
                self._httpx_backend = HttpxSPARQL_Store.HttpxBackend(
                    self._store,
                    f'http://localhost:{port}/datastores/{self._name}/sparql',
                    **kwargs)

        @override
        def _load_location(
                self,
                location: pathlib.PurePath | str,
                format: str | None = None
        ) -> None:
            with self._lock:
                self.rdfox.active(self._name)
                self.rdfox.import_file(location)

        @override
        def _load_data(
                self,
                data: bytes | str,
                format: str | None = None
        ) -> None:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            with self._lock:
                self.rdfox.active(self._name)
                self.rdfox.import_data(data)

        @override
        def _skolemize(self) -> None:
            ###
            # TODO: Find a better way to do this.
            ###
            with tempfile.NamedTemporaryFile(
                    prefix='rdfox_', suffix='.n3',
                    mode='w', delete=True) as temp:
                with self._lock:
                    self.rdfox.export(
                        temp.name, 'application/n-triples',
                        'fact-domain', 'all')
                with tempfile.NamedTemporaryFile(
                        prefix='rdfox_skolemized_', suffix='.n3',
                        mode='w', delete=True) as temp_skolemized:
                    with open(temp.name) as fp:
                        for line in map(self._skolemize_n3_line, fp):
                            temp_skolemized.write(line)
                    temp_skolemized.flush()
                    with self._lock:
                        self.rdfox.clear()
                        self.rdfox.import_file(temp_skolemized.name)

        def _skolemize_n3_line(
                self,
                line: str,
                _re_start: re.Pattern = re.compile(r'^_:(\w+)( .*)$'),
                _re_end: re.Pattern = re.compile(r'^(.* )_:(\w+) \.$')
        ) -> str:
            m = _re_start.match(line)
            if m:
                s, po = m.groups()
                line = f'<{rdflib.BNode(s).skolemize()}>' + po + '\n'
            m = _re_end.match(line)
            if m:
                sp, o = m.groups()
                line = sp + f'<{rdflib.BNode(o).skolemize()}>' + ' .\n'
            return line

        @override
        def _close(self) -> None:
            self._httpx_backend.close()
            with self._lock:
                self.rdfox.dstore_delete(self._name)

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

    #: Type alias for RDFox SPARQL store arguments.
    Args: TypeAlias = RDFoxBackend.Args

    def __init__(
            self,
            store_name: str,
            *args: RDFoxSPARQL_Store.Args,
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
            self.RDFoxBackend, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize, **kwargs)
