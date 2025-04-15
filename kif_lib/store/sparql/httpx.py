# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import httpx

from ...compiler.sparql import SPARQL_Mapping
from ...compiler.sparql.results import SPARQL_Results, SPARQL_ResultsAsk
from ...model import IRI, KIF_Object, T_IRI
from ...typing import Any, cast, Final, Mapping, override, TypeAlias
from ...version import __version__
from .sparql_core import _SPARQL_Store


class HttpxSPARQL_Store(
        _SPARQL_Store,
        store_name='sparql-httpx',
        store_description='SPARQL store with httpx backend'
):
    """SPARQL store with httpx backend.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       iri: IRI of the target SPARQL endpoint.
       headers: HTTP headers.
       mapping: SPARQL mapping.
       kwargs: Other keyword arguments.
    """

    class HttpxBackend(_SPARQL_Store.Backend):
        """Httpx backend.

        Parameters:
           store: Parent SPARQL store.
           iri: IRI of the target SPARQL endpoint.
           headers: HTTP headers.
           kwargs: Other keyword arguments.
        """

        HTTP_Headers: TypeAlias = Mapping[str, str]

        _default_headers: Final[HTTP_Headers] = {
            ###
            # See <https://meta.wikimedia.org/wiki/User-Agent_policy>.
            ###
            'User-Agent': f'KIF/{__version__} (https://github.com/IBM/kif/)',
            'Content-Type': 'application/sparql-query;charset=utf-8',
            'Accept': 'application/sparql-results+json;charset=utf-8',
        }

        __slots__ = (
            '_client',
            '_headers',
            '_iri',
        )

        #: HTTP client.
        _client: httpx.Client | None

        #: HTTP headers.
        _headers: HTTP_Headers

        #: IRI of the target SPARQL endpoint.
        _iri: IRI

        def __init__(
                self,
                store: _SPARQL_Store,
                iri: T_IRI,
                *,
                headers: HTTP_Headers | None = None,
                **kwargs: Any
        ) -> None:
            super().__init__(store)
            self._client = None
            self._iri = IRI.check(iri, type(store), 'iri')
            try:
                self._headers = cast(
                    HttpxSPARQL_Store.HttpxBackend.HTTP_Headers,
                    {**dict(self._default_headers),
                     **dict(headers or {})})
            except Exception as err:
                raise KIF_Object._arg_error(
                    str(err), type(store), 'headers', exception=store.Error)
            self._client = httpx.Client(headers=self._headers)

        def __del__(self) -> None:
            if self._client is not None:
                self._client.close()

        @override
        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return cast(SPARQL_ResultsAsk, self._select(query))

        @override
        def _select(self, query: str) -> SPARQL_Results:
            return self._http_post(query).json()

        def _http_post(self, text: str) -> httpx.Response:
            assert self._client is not None
            try:
                res = self._client.post(
                    self._iri.content, content=text.encode('utf-8'))
                res.raise_for_status()
                return res
            except httpx.RequestError as err:
                raise err

        @override
        def _set_timeout(self, timeout: float | None = None) -> None:
            if self._client is not None:
                self._client.timeout = httpx.Timeout(timeout)

    def __init__(
            self,
            store_name: str,
            iri: T_IRI,
            headers: HttpxSPARQL_Store.HttpxBackend.HTTP_Headers | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(
            store_name,
            (mapping if mapping is not None
             else self._wikidata_mapping_constructor()),
            self.HttpxBackend, iri=iri, headers=headers, **kwargs)
