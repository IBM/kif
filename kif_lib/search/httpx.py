# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import logging

import httpx

from .. import functools
from ..__version__ import __version__
from ..context import Context
from ..model import IRI, KIF_Object, T_IRI
from ..typing import (
    Any,
    cast,
    ClassVar,
    Final,
    Iterable,
    Location,
    Mapping,
    override,
    TypeAlias,
    TypeVar,
)
from .abc import Search, SearchOptions

_logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclasses.dataclass
class _HttpxSearchOptions(SearchOptions):
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
        self._init_iri(kwargs)

    # -- iri --

    #: Default value for the IRI option.
    DEFAULT_IRI: ClassVar[str | None] = None

    _v_iri: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_HTTPX_SEARCH_IRI'), DEFAULT_IRI)

    _iri: IRI | None

    def _init_iri(self, kwargs: dict[str, Any]) -> None:
        self.iri = kwargs.get(
            '_iri', self.getenv_optional_str(*self._v_iri))

    @property
    def iri(self) -> IRI | None:
        """The IRI of httpx search."""
        return self.get_iri()

    @iri.setter
    def iri(self, iri: T_IRI | None) -> None:
        self.set_iri(iri)

    def get_iri(self) -> IRI | None:
        """Gets the IRI of httpx search.

        Returns:
           IRI or ``None``.
        """
        return self._iri

    def set_iri(
            self,
            iri: T_IRI | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the IRI of httpx search.

        Parameters:
           iri: IRI.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._iri = self._check_optional_iri(
            iri, None, function, name, position)


@dataclasses.dataclass
class HttpxSearchOptions(_HttpxSearchOptions, name='httpx'):
    """Httpx search options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @override
    def get_iri(self) -> IRI | None:
        return self._do_get('_iri', super().get_iri)

    @override
    def set_iri(
            self,
            iri: T_IRI | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(iri, '_iri', functools.partial(
            super().set_iri,
            function=function, name=name, position=position))


# == Httpx search ==========================================================

TOptions = TypeVar(
    'TOptions', bound=HttpxSearchOptions, default=HttpxSearchOptions)


class HttpxSearch(
        Search[TOptions],
        search_name='httpx',
        search_description='Httpx search'
):
    """Search with httpx.

    Parameters:
       search_name: Name of the search plugin to instantiate.
       iri: IRI.
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
            iri: T_IRI | None = None,
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
        self._client = None
        self._aclient = None
        super().__init__(search_name, iri=iri, **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cast(TOptions, cls.get_context(context).options.search.httpx)

    @override
    def _update_options(self, **kwargs: Any) -> None:
        super()._update_options(**kwargs)
        if 'iri' in kwargs:
            self.set_iri(kwargs['iri'])

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

    def _http_get_json(
            self,
            iri: str,
            params: httpx._types.QueryParamTypes | None = None,
            timeout: httpx._types.TimeoutTypes | None = None
    ) -> HttpxSearch.TData:
        try:
            return self._http_get(iri, params, timeout).json()
        except httpx.HTTPStatusError as err:
            import json
            try:
                _logger.error('%s:\n%s', err, json.dumps(
                    err.response.json(), indent=2))
            except json.JSONDecodeError:
                _logger.error('%s\n%s', err, err.response.text)
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

    async def _http_aget_json(
            self,
            iri: str,
            params: httpx._types.QueryParamTypes | None = None,
            timeout: httpx._types.TimeoutTypes | None = None
    ) -> HttpxSearch.TData:
        try:
            return (await self._http_aget(iri, params, timeout)).json()
        except httpx.HTTPStatusError as err:
            import json
            try:
                _logger.error('%s:\n%s', err, json.dumps(
                    err.response.json(), indent=2))
            except json.JSONDecodeError:
                _logger.error('%s\n%s', err, err.response.text)
            raise err

# -- IRI -------------------------------------------------------------------

    @property
    def default_iri(self) -> IRI | None:
        """The default value for :attr:`HttpxSearch.iri`."""
        return self.get_default_iri()

    def get_default_iri(self) -> IRI | None:
        """Gets the default value for :attr:`HttpxSearch.iri`.

        Returns:
           Default IRI.
        """
        return self.get_default_options().iri

    @property
    def iri(self) -> IRI | None:
        """The IRI of httpx search."""
        return self.get_iri()

    @iri.setter
    def iri(self, iri: T_IRI | None = None) -> None:
        self.set_iri(iri)

    def get_iri(self, default: IRI | None = None) -> IRI | None:
        """Gets the iri of httpx search.

        If the iri is ``None``, returns `default`.

        Parameters:
           default: Default iri.

        Returns:
           Iri or ``None``.
        """
        iri = self.options.iri
        if iri is None:
            iri = default
        return iri

    def set_iri(self, iri: T_IRI | None = None) -> None:
        """Sets the IRI of httpx search.

        If `iri` is ``None``, resets it to the default.

        Parameters:
           iri: IRI.
        """
        self._set_option_with_hooks(
            iri,
            self.options.get_iri,
            functools.partial(
                self.options.set_iri,
                function=self.set_iri,
                name='iri',
                position=1),
            self._set_iri)

    def _set_iri(self, iri: IRI | None) -> bool:
        return True
