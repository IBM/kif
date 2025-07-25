# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

import httpx

from ..__version__ import __version__
from ..model import KIF_Object
from ..typing import (
    Any,
    ClassVar,
    Final,
    Iterable,
    Mapping,
    override,
    TypeAlias,
)
from .abc import Search, SearchOptions, TOptions


@dataclasses.dataclass
class HttpxSearchOptions(SearchOptions, name='httpx'):
    """Httpx search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_HTTPX_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_HTTPX_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_HTTPX_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_HTTPX_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_HTTPX_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_HTTPX_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_HTTPX_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_HTTPX_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_HTTPX_SEARCH_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Httpx search ==========================================================

class HttpxSearch(
        Search[TOptions],
        search_name='httpx',
        search_description='Search with httpx'
):
    """Search with httpx.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       iri: IRI of the target HTTP endpoint.
       headers: HTTP headers.
       kwargs: Other keyword arguments.
    """

    HTTP_Headers: TypeAlias = Mapping[str, str]

    _default_headers: Final[HTTP_Headers] = {
        ###
        # See <https://meta.wikimedia.org/wiki/User-Agent_policy>.
        ###
        'User-Agent': f'KIF/{__version__} (https://github.com/IBM/kif/)',
    }

    __slots__ = (
        '_aclient',
        '_client',
        '_headers'
    )

    #: HTTP client.
    _client: httpx.Client | None

    #: Async HTTP client.
    _aclient: httpx.AsyncClient | None

    #: HTTP headers.
    _headers: HTTP_Headers

    def __init__(
            self,
            search_name: str,
            headers: HTTP_Headers | None = None,
            **kwargs: Any
    ) -> None:
        assert search_name == self.search_name
        try:
            self._headers = {
                **dict(self._default_headers),
                **dict(headers or {})}
        except Exception as err:
            raise KIF_Object._arg_error(
                str(err), type(self), 'headers', exception=self.Error)
        super().__init__(search_name, headers, **kwargs)
        self._client = None
        self._aclient = None

    @property
    def client(self) -> httpx.Client:
        return self.get_client()

    def get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(headers=self._headers)
        return self._client

    @override
    def _close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def _http_get(
            self,
            iri: str,
            params: httpx._types.QueryParamTypes | None = None,
            timeout: httpx._types.TimeoutTypes | None = None
    ) -> httpx.Response:
        try:
            res = self.client.get(
                iri, params=params, timeout=httpx.Timeout(self.timeout))
            res.raise_for_status()
            return res
        except httpx.RequestError as err:
            raise err

    @property
    def aclient(self) -> httpx.AsyncClient:
        return self.get_aclient()

    def get_aclient(self) -> httpx.AsyncClient:
        if self._aclient is None:
            self._aclient = httpx.AsyncClient(headers=self._headers)
        return self._aclient

    @override
    async def _aclose(self) -> None:
        if self._aclient is not None:
            await self._aclient.aclose()
            self._aclient = None

    async def _http_aget(
            self,
            iri: str,
            params: httpx._types.QueryParamTypes | None = None,
            timeout: httpx._types.TimeoutTypes | None = None
    ) -> httpx.Response:
        try:
            res = await self.aclient.get(
                iri, params=params, timeout=httpx.Timeout(self.timeout))
            res.raise_for_status()
            return res
        except httpx.RequestError as err:
            raise err
