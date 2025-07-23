# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

import httpx

from ..__version__ import __version__
from ..context import Context
from ..error import Error as KIF_Error
from ..model import (
    Entity,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    String,
    TTextLanguage,
)
from ..typing import (
    Any,
    AsyncIterator,
    cast,
    Final,
    Iterator,
    Literal,
    Location,
    Mapping,
    TypeAlias,
)

at_property = property


class Search:
    """Abstract base class for vocabulary searches."""

    class Error(KIF_Error):
        """Base class for search errors."""

    #: Type alias for HTTP headers.
    HTTP_Headers: TypeAlias = Mapping[str, str]

    #: Default HTTP headers.
    _default_headers: Final[HTTP_Headers] = {
        'User-Agent': f'KIF/{__version__} (https://github.com/IBM/kif/)',
    }

    __slots__ = (
        '_aclient',
        '_client',
        '_headers',
        '_timeout',
    )

    #: HTTP client.
    _client: httpx.Client | None

    #: Async HTTP client.
    _aclient: httpx.AsyncClient | None

    #: HTTP headers.
    _headers: Search.HTTP_Headers

    #: Timeout in seconds.
    _timeout: float | None

    def __init__(
            self,
            *args: Any,
            headers: HTTP_Headers | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> None:
        self._client = None
        self._aclient = None
        try:
            self._headers = cast(Search.HTTP_Headers, {
                **dict(self._default_headers),
                **dict(headers or {})})
        except Exception as err:
            raise KIF_Object._arg_error(
                str(err), type(self), 'headers', exception=self.Error)
        self._timeout = KIF_Object._check_optional_arg_float(
            timeout, None, type(self), 'timeout')

    @at_property
    def client(self) -> httpx.Client:
        return self.get_client()

    def get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(headers=self._headers)
        return self._client

    def _http_get(
            self,
            iri: str,
            params: httpx._types.QueryParamTypes | None = None,
            timeout: httpx._types.TimeoutTypes | None = None
    ) -> httpx.Response:
        try:
            res = self.client.get(iri, params=params, timeout=timeout)
            res.raise_for_status()
            return res
        except httpx.RequestError as err:
            raise err

    @at_property
    def aclient(self) -> httpx.AsyncClient:
        return self.get_aclient()

    def get_aclient(self) -> httpx.AsyncClient:
        if self._aclient is None:
            self._aclient = httpx.AsyncClient(headers=self._headers)
        return self._aclient

    async def _http_aget(
            self,
            iri: str,
            params: httpx._types.QueryParamTypes | None = None,
            timeout: httpx._types.TimeoutTypes | None = None
    ) -> httpx.Response:
        try:
            res = await self.aclient.get(iri, params=params, timeout=timeout)
            res.raise_for_status()
            return res
        except httpx.RequestError as err:
            raise err

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        """Closes search."""
        self._close()

    def _close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    async def aclose(self) -> None:
        """Async version of :meth:`Search.close`."""
        await self._aclose()

    async def _aclose(self) -> None:
        if self._aclient is not None:
            await self._aclient.aclose()
            self._aclient = None

    @at_property
    def context(self) -> Context:
        """The current KIF context."""
        return self.get_context()

    def get_context(self, context: Context | None = None) -> Context:
        """Gets the current KIF context.

        If `context` is not ``None``, returns `context`.

        Parameters:
           context: Context.

        Returns:
           Context.
        """
        return Context.top(context)

    def _check_optional_language(
            self,
            language: TTextLanguage | None,
            function: Location,
    ) -> String | None:
        return String.check_optional(
            language, None, function, 'language')

    def _check_optional_limit(
            self,
            limit: int | None,
            function: Location,
    ) -> int | None:
        return KIF_Object._check_optional_arg_int(
            limit, None, function, 'limit')

    def _check_optional_page_size(
            self,
            page_size: int | None,
            function: Location,
    ) -> int | None:
        return KIF_Object._check_optional_arg_int(
            page_size, None, function, 'page_size')

    @abc.abstractmethod
    def _search(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> Iterator[tuple[Entity, dict[str, Any]]]:
        raise NotImplementedError

    def item(
            self,
            search: str,
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> Iterator[tuple[Item, dict[str, Any]]]:
        """Searches for item within vocabulary.

        Parameters:
           search: Search text.
           language: Language.
           limit: Maximum number of results.
           page_size: Maximum number of results per page.
           context: KIF Context.
        """
        return cast(
            Iterator[tuple[Item, dict[str, Any]]],
            self._search(
                search, 'item', language, limit, page_size, context))

    def lexeme(
            self,
            search: str,
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> Iterator[tuple[Lexeme, dict[str, Any]]]:
        """Searches for lexeme within vocabulary.

        Parameters:
           search: Search text.
           language: Language.
           limit: Maximum number of results.
           page_size: Maximum number of results per page.
           context: KIF Context.
        """
        return cast(
            Iterator[tuple[Lexeme, dict[str, Any]]],
            self._search(
                search, 'lexeme', language, limit, page_size, context))

    def property(
            self,
            search: str,
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> Iterator[tuple[Property, dict[str, Any]]]:
        """Searches for property within vocabulary.

        Parameters:
           search: Search text.
           language: Language.
           limit: Maximum number of results.
           page_size: Maximum number of results per page.
           context: KIF Context.
        """
        return cast(
            Iterator[tuple[Property, dict[str, Any]]],
            self._search(
                search, 'property', language, limit, page_size, context))

    @abc.abstractmethod
    def _asearch(
            self,
            search: str,
            type: Literal['item', 'lexeme', 'property'],
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> AsyncIterator[tuple[Entity, dict[str, Any]]]:
        raise NotImplementedError

    def aitem(
            self,
            search: str,
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> AsyncIterator[tuple[Item, dict[str, Any]]]:
        """Searches for item within vocabulary.

        Parameters:
           search: Search text.
           language: Language.
           limit: Maximum number of results.
           page_size: Maximum number of results per page.
           context: KIF Context.
        """
        return cast(
            AsyncIterator[tuple[Item, dict[str, Any]]],
            self._asearch(
                search, 'item', language, limit, page_size, context))

    def alexeme(
            self,
            search: str,
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> AsyncIterator[tuple[Lexeme, dict[str, Any]]]:
        """Searches for lexeme within vocabulary.

        Parameters:
           search: Search text.
           language: Language.
           limit: Maximum number of results.
           page_size: Maximum number of results per page.
           context: KIF Context.
        """
        return cast(
            AsyncIterator[tuple[Lexeme, dict[str, Any]]],
            self._asearch(
                search, 'lexeme', language, limit, page_size, context))

    def aproperty(
            self,
            search: str,
            language: TTextLanguage | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            context: Context | None = None
    ) -> AsyncIterator[tuple[Property, dict[str, Any]]]:
        """Searches for property within vocabulary.

        Parameters:
           search: Search text.
           language: Language.
           limit: Maximum number of results.
           page_size: Maximum number of results per page.
           context: KIF Context.
        """
        return cast(
            AsyncIterator[tuple[Property, dict[str, Any]]],
            self._asearch(
                search, 'property', language, limit, page_size, context))
