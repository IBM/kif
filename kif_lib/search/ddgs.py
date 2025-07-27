# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import collections
import dataclasses
import functools
import logging
import re

from ..context import Context
from ..model import Item, Lexeme, Property, Text
from ..typing import (
    Any,
    AsyncIterator,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Literal,
    Location,
    override,
    TypeAlias,
    TypeVar,
)
from .abc import Search, SearchOptions

_DDGS_URL: Final[str] = 'https://github.com/deedy5/ddgs'
_logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclasses.dataclass
class _DDGS_SearchOptions(SearchOptions):
    """DDGS search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_DDGS_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DDGS_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DDGS_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DDGS_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DDGS_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_DDGS_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DDGS_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_DDGS_SEARCH_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._init_backend(kwargs)
        self._init_in_url(kwargs)
        self._init_item_match(kwargs)
        self._init_item_sub(kwargs)
        self._init_lexeme_match(kwargs)
        self._init_lexeme_sub(kwargs)
        self._init_property_match(kwargs)
        self._init_property_sub(kwargs)
        self._init_site(kwargs)

    # -- backend --

    #: Default value for the backend option.
    DEFAULT_BACKEND: ClassVar[str | None] = None

    _v_backend: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_BACKEND'), DEFAULT_BACKEND)

    _backend: str | None

    def _init_backend(self, kwargs: dict[str, Any]) -> None:
        self.backend = kwargs.get(
            '_backend', self.getenv_optional_str(*self._v_backend))

    @property
    def backend(self) -> str | None:
        """The backend of DDGS search."""
        return self.get_backend()

    @backend.setter
    def backend(self, backend: str | None) -> None:
        self.set_backend(backend)

    def get_backend(self) -> str | None:
        """Gets the backend of DDGS search.

        Returns:
           Backend or ``None``.
        """
        return self._backend

    def set_backend(
            self,
            backend: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the backend of DDGS search.

        Parameters:
           backend: Backend.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._backend = self._check_optional_str(
            backend, None, function, name, position)

    # -- in-URL --

    #: Default value for the in-URL option.
    DEFAULT_IN_URL: ClassVar[str | None] = None

    _v_in_url: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_IN_URL'), DEFAULT_IN_URL)

    _in_url: str | None

    def _init_in_url(self, kwargs: dict[str, Any]) -> None:
        self.in_url = kwargs.get(
            '_in_url', self.getenv_optional_str(*self._v_in_url))

    @property
    def in_url(self) -> str | None:
        """The in-URL DDGS search."""
        return self.get_in_url()

    @in_url.setter
    def in_url(self, in_url: str | None) -> None:
        self.set_in_url(in_url)

    def get_in_url(self) -> str | None:
        """Gets the in-URL of DDGS search.

        Returns:
           in-URL or ``None``.
        """
        return self._in_url

    def set_in_url(
            self,
            in_url: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the in-URL of DDGS search.

        Parameters:
           in_url: In-URL.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._in_url = self._check_optional_str(
            in_url, None, function, name, position)

    # -- item match regex --

    #: Default value for the item match regex.
    DEFAULT_ITEM_MATCH: ClassVar[str | None] = None

    _v_item_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_ITEM_MATCH'), DEFAULT_ITEM_MATCH)

    _item_match: str | None

    def _init_item_match(self, kwargs: dict[str, Any]) -> None:
        self.item_match = kwargs.get(
            '_item_match', self.getenv_optional_str(*self._v_item_match))

    @property
    def item_match(self) -> str | None:
        """The item match regex of DDGS search."""
        return self.get_item_match()

    @item_match.setter
    def item_match(self, item_match: str | None) -> None:
        self.set_item_match(item_match)

    def get_item_match(self) -> str | None:
        """Gets the item match regex of DDGS search.

        Returns:
           Item match regex or ``None``.
        """
        return self._item_match

    def set_item_match(
            self,
            item_match: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the item match regex of DDGS search.

        Parameters:
           item_match: Item match regex.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._item_match = self._check_optional_str(
            item_match, None, function, name, position)

    # -- item sub --

    #: Default value for the item sub.
    DEFAULT_ITEM_SUB: ClassVar[str | None] = None

    _v_item_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_ITEM_SUB'), DEFAULT_ITEM_SUB)

    _item_sub: str | None

    def _init_item_sub(self, kwargs: dict[str, Any]) -> None:
        self.item_sub = kwargs.get(
            '_item_sub', self.getenv_optional_str(*self._v_item_sub))

    @property
    def item_sub(self) -> str | None:
        """The item sub of DDGS search."""
        return self.get_item_sub()

    @item_sub.setter
    def item_sub(self, item_sub: str | None) -> None:
        self.set_item_sub(item_sub)

    def get_item_sub(self) -> str | None:
        """Gets the item sub of DDGS search.

        Returns:
           Item sub or ``None``.
        """
        return self._item_sub

    def set_item_sub(
            self,
            item_sub: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the item sub of DDGS search.

        Parameters:
           item_sub: Item sub.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._item_sub = self._check_optional_str(
            item_sub, None, function, name, position)

    # -- lexeme match regex --

    #: Default value for the lexeme match regex.
    DEFAULT_LEXEME_MATCH: ClassVar[str | None] = None

    _v_lexeme_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_LEXEME_MATCH'), DEFAULT_LEXEME_MATCH)

    _lexeme_match: str | None

    def _init_lexeme_match(self, kwargs: dict[str, Any]) -> None:
        self.lexeme_match = kwargs.get(
            '_lexeme_match', self.getenv_optional_str(*self._v_lexeme_match))

    @property
    def lexeme_match(self) -> str | None:
        """The lexeme match regex of DDGS search."""
        return self.get_lexeme_match()

    @lexeme_match.setter
    def lexeme_match(self, lexeme_match: str | None) -> None:
        self.set_lexeme_match(lexeme_match)

    def get_lexeme_match(self) -> str | None:
        """Gets the lexeme match regex of DDGS search.

        Returns:
           Lexeme match regex or ``None``.
        """
        return self._lexeme_match

    def set_lexeme_match(
            self,
            lexeme_match: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the lexeme match regex of DDGS search.

        Parameters:
           lexeme_match: Lexeme match regex.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._lexeme_match = self._check_optional_str(
            lexeme_match, None, function, name, position)

    # -- lexeme sub --

    #: Default value for the lexeme sub.
    DEFAULT_LEXEME_SUB: ClassVar[str | None] = None

    _v_lexeme_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_LEXEME_SUB'), DEFAULT_LEXEME_SUB)

    _lexeme_sub: str | None

    def _init_lexeme_sub(self, kwargs: dict[str, Any]) -> None:
        self.lexeme_sub = kwargs.get(
            '_lexeme_sub', self.getenv_optional_str(*self._v_lexeme_sub))

    @property
    def lexeme_sub(self) -> str | None:
        """The lexeme sub of DDGS search."""
        return self.get_lexeme_sub()

    @lexeme_sub.setter
    def lexeme_sub(self, lexeme_sub: str | None) -> None:
        self.set_lexeme_sub(lexeme_sub)

    def get_lexeme_sub(self) -> str | None:
        """Gets the lexeme sub of DDGS search.

        Returns:
           Lexeme sub or ``None``.
        """
        return self._lexeme_sub

    def set_lexeme_sub(
            self,
            lexeme_sub: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the lexeme sub of DDGS search.

        Parameters:
           lexeme_sub: Lexeme sub.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._lexeme_sub = self._check_optional_str(
            lexeme_sub, None, function, name, position)

    # -- property match regex --

    #: Default value for the property match regex.
    DEFAULT_PROPERTY_MATCH: ClassVar[str | None] = None

    _v_property_match: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_PROPERTY_MATCH'), DEFAULT_PROPERTY_MATCH)

    _property_match: str | None

    def _init_property_match(self, kwargs: dict[str, Any]) -> None:
        self.property_match = kwargs.get(
            '_property_match', self.getenv_optional_str(
                *self._v_property_match))

    @property
    def property_match(self) -> str | None:
        """The property match regex of DDGS search."""
        return self.get_property_match()

    @property_match.setter
    def property_match(self, property_match: str | None) -> None:
        self.set_property_match(property_match)

    def get_property_match(self) -> str | None:
        """Gets the property match regex of DDGS search.

        Returns:
           Property match regex or ``None``.
        """
        return self._property_match

    def set_property_match(
            self,
            property_match: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the property match regex of DDGS search.

        Parameters:
           property_match: Property match regex.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._property_match = self._check_optional_str(
            property_match, None, function, name, position)

    # -- property sub --

    #: Default value for the property sub.
    DEFAULT_PROPERTY_SUB: ClassVar[str | None] = None

    _v_property_sub: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_PROPERTY_SUB'), DEFAULT_PROPERTY_SUB)

    _property_sub: str | None

    def _init_property_sub(self, kwargs: dict[str, Any]) -> None:
        self.property_sub = kwargs.get(
            '_property_sub', self.getenv_optional_str(*self._v_property_sub))

    @property
    def property_sub(self) -> str | None:
        """The property sub of DDGS search."""
        return self.get_property_sub()

    @property_sub.setter
    def property_sub(self, property_sub: str | None) -> None:
        self.set_property_sub(property_sub)

    def get_property_sub(self) -> str | None:
        """Gets the property sub of DDGS search.

        Returns:
           Property sub or ``None``.
        """
        return self._property_sub

    def set_property_sub(
            self,
            property_sub: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the property sub of DDGS search.

        Parameters:
           property_sub: Property sub.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._property_sub = self._check_optional_str(
            property_sub, None, function, name, position)

    # -- site --

    #: Default value for the site option.
    DEFAULT_SITE: ClassVar[str | None] = None

    _v_site: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_DDGS_SEARCH_SITE'), DEFAULT_SITE)

    _site: str | None

    def _init_site(self, kwargs: dict[str, Any]) -> None:
        self.site = kwargs.get(
            '_site', self.getenv_optional_str(*self._v_site))

    @property
    def site(self) -> str | None:
        """The site of DDGS search."""
        return self.get_site()

    @site.setter
    def site(self, site: str | None) -> None:
        self.set_site(site)

    def get_site(self) -> str | None:
        """Gets the site of DDGS search.

        Returns:
           Site or ``None``.
        """
        return self._site

    def set_site(
            self,
            site: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the site of DDGS search.

        Parameters:
           site: Site.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._site = self._check_optional_str(
            site, None, function, name, position)


@dataclasses.dataclass
class DDGS_SearchOptions(_DDGS_SearchOptions, name='ddgs'):
    """DDGS search options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @override
    def get_backend(self) -> str | None:
        return self._do_get('_backend', super().get_backend)

    @override
    def set_backend(
            self,
            backend: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(backend, '_backend', functools.partial(
            super().set_backend,
            function=function, name=name, position=position))

    @override
    def get_in_url(self) -> str | None:
        return self._do_get('_in_url', super().get_in_url)

    @override
    def set_in_url(
            self,
            in_url: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(in_url, '_in_url', functools.partial(
            super().set_in_url,
            function=function, name=name, position=position))

    @override
    def get_item_match(self) -> str | None:
        return self._do_get('_item_match', super().get_item_match)

    @override
    def set_item_match(
            self,
            item_match: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(item_match, '_item_match', functools.partial(
            super().set_item_match,
            function=function, name=name, position=position))

    @override
    def get_item_sub(self) -> str | None:
        return self._do_get('_item_sub', super().get_item_sub)

    @override
    def set_item_sub(
            self,
            item_sub: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(item_sub, '_item_sub', functools.partial(
            super().set_item_sub,
            function=function, name=name, position=position))

    @override
    def get_lexeme_match(self) -> str | None:
        return self._do_get('_lexeme_match', super().get_lexeme_match)

    @override
    def set_lexeme_match(
            self,
            lexeme_match: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(lexeme_match, '_lexeme_match', functools.partial(
            super().set_lexeme_match,
            function=function, name=name, position=position))

    @override
    def get_lexeme_sub(self) -> str | None:
        return self._do_get('_lexeme_sub', super().get_lexeme_sub)

    @override
    def set_lexeme_sub(
            self,
            lexeme_sub: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(lexeme_sub, '_lexeme_sub', functools.partial(
            super().set_lexeme_sub,
            function=function, name=name, position=position))

    @override
    def get_property_match(self) -> str | None:
        return self._do_get('_property_match', super().get_property_match)

    @override
    def set_property_match(
            self,
            property_match: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(property_match, '_property_match', functools.partial(
            super().set_property_match,
            function=function, name=name, position=position))

    @override
    def get_property_sub(self) -> str | None:
        return self._do_get('_property_sub', super().get_property_sub)

    @override
    def set_property_sub(
            self,
            property_sub: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(property_sub, '_property_sub', functools.partial(
            super().set_property_sub,
            function=function, name=name, position=position))

    @override
    def get_site(self) -> str | None:
        return self._do_get('_site', super().get_site)

    @override
    def set_site(
            self,
            site: str | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(site, '_site', functools.partial(
            super().set_site,
            function=function, name=name, position=position))


# == DDGS search ===========================================================

_DDGS_Proxy: TypeAlias = Any
TOptions = TypeVar(
    'TOptions', bound=DDGS_SearchOptions, default=DDGS_SearchOptions)


class DDGS_Search(
        Search[TOptions],
        search_name='ddgs',
        search_description='DDGS search'
):
    """Search with DDGS

    Parameters:
       search_name: Name of the search plugin to instantiate.
       backend: DDGS backend.
       in_url: DDGS in-URL.
       item_match: Item match regex.
       item_sub: Item sub.
       lexeme_match: Lexeme match regex.
       lexeme_sub: Lexeme sub.
       property_match: Property match regex.
       property_sub: Property sub.
       site: DGGS site.
       kwargs: Other keyword arguments.
    """

    __slots__ = (
        '_ddgs',
        '_re_item',
        '_re_lexeme',
        '_re_property',
    )

    #: DDGS client.
    _ddgs: _DDGS_Proxy | None

    #: The compiled item match regex and sub (if any).
    _re_item: tuple[re.Pattern[str] | None, str | None] | None

    #: The compiled lexeme match regex and sub (if any).
    _re_lexeme: tuple[re.Pattern[str] | None, str | None] | None

    #: The compiled property match regex and sub (if any).
    _re_property: tuple[re.Pattern[str] | None, str | None] | None

    def __init__(
            self,
            search_name: str,
            backend: str | None = None,
            in_url: str | None = None,
            item_match: str | None = None,
            item_sub: str | None = None,
            lexeme_match: str | None = None,
            lexeme_sub: str | None = None,
            property_match: str | None = None,
            property_sub: str | None = None,
            site: str | None = None,
            **kwargs: Any
    ) -> None:
        assert search_name == self.search_name
        self._ddgs = None
        self._re_item = None
        self._re_lexeme = None
        self._re_property = None
        super().__init__(
            search_name,
            backend=backend,
            in_url=in_url,
            item_match=item_match,
            item_sub=item_sub,
            lexeme_match=lexeme_match,
            lexeme_sub=lexeme_sub,
            property_match=property_match,
            property_sub=property_sub,
            site=site,
            **kwargs)

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cast(TOptions, cls.get_context(context).options.search.ddgs)

    @override
    def _update_options(self, **kwargs: Any) -> None:
        super()._update_options(**kwargs)
        if 'backend' in kwargs:
            self.set_backend(kwargs['backend'])
        if 'in_url' in kwargs:
            self.set_in_url(kwargs['in_url'])
        if 'item_match' in kwargs:
            self.set_item_match(kwargs['item_match'])
        if 'item_sub' in kwargs:
            self.set_item_sub(kwargs['item_sub'])
        if 'lexeme_match' in kwargs:
            self.set_lexeme_match(kwargs['lexeme_match'])
        if 'lexeme_sub' in kwargs:
            self.set_lexeme_sub(kwargs['lexeme_sub'])
        if 'property_match' in kwargs:
            self.set_property_match(kwargs['property_match'])
        if 'property_sub' in kwargs:
            self.set_property_sub(kwargs['property_sub'])
        if 'site' in kwargs:
            self.set_site(kwargs['site'])

    @property
    def ddgs(self) -> _DDGS_Proxy:
        return self.get_ddgs()

    def get_ddgs(self) -> _DDGS_Proxy:
        if self._ddgs is None:
            try:
                import ddgs  # type: ignore
                self._ddgs = ddgs.DDGS(
                    timeout=(
                        int(self.timeout)
                        if self.timeout is not None else None),
                    verify=False)
            except ImportError as err:
                raise ImportError(
                    f'{self.__class__.__qualname__} '
                    f'requires {_DDGS_URL}') from err
        return self._ddgs

    @property
    def re_item(self) -> tuple[re.Pattern[str] | None, str | None]:
        return self.get_re_item()

    def get_re_item(self) -> tuple[re.Pattern[str] | None, str | None]:
        if self._re_item is None:
            self._re_item = self._get_re_x(
                self.get_item_match, self.get_item_sub)
        return self._re_item

    @property
    def re_lexeme(self) -> tuple[re.Pattern[str] | None, str | None]:
        return self.get_re_lexeme()

    def get_re_lexeme(self) -> tuple[re.Pattern[str] | None, str | None]:
        if self._re_lexeme is None:
            self._re_lexeme = self._get_re_x(
                self.get_lexeme_match, self.get_lexeme_sub)
        return self._re_lexeme

    @property
    def re_property(self) -> tuple[re.Pattern[str] | None, str | None]:
        return self.get_re_property()

    def get_re_property(self) -> tuple[re.Pattern[str] | None, str | None]:
        if self._re_property is None:
            self._re_property = self._get_re_x(
                self.get_property_match, self.get_property_sub)
        return self._re_property

    def _get_re_x(
            self,
            get_x_regex: Callable[[], str | None],
            get_x_sub: Callable[[], str | None]
    ) -> tuple[re.Pattern[str] | None, str | None]:
        regex_str = get_x_regex()
        if regex_str is not None:
            regex = re.compile(regex_str)
        else:
            regex = None
        return (regex, get_x_sub())

# -- Backend ---------------------------------------------------------------

    @property
    def default_backend(self) -> str | None:
        """The default value for :attr:`DDGS_Search.backend`."""
        return self.get_default_backend()

    def get_default_backend(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.backend`.

        Returns:
           Default backend.
        """
        return self.get_default_options().backend

    @property
    def backend(self) -> str | None:
        """The backend of DDGS search."""
        return self.get_backend()

    @backend.setter
    def backend(self, backend: str | None = None) -> None:
        self.set_backend(backend)

    def get_backend(self, default: str | None = None) -> str | None:
        """Gets the backend of DDGS search.

        If the backend is ``None``, returns `default`.

        Parameters:
           default: Default backend.

        Returns:
           Backend or ``None``.
        """
        backend = self.options.backend
        if backend is None:
            backend = default
        return backend

    def set_backend(self, backend: str | None = None) -> None:
        """Sets the backend of DDGS search.

        If `backend` is ``None``, resets it to the default.

        Parameters:
           backend: Backend.
        """
        self._set_option_with_hooks(
            backend,
            self.options.get_backend,
            functools.partial(
                self.options.set_backend,
                function=self.set_backend,
                name='backend',
                position=1),
            self._set_backend)

    def _set_backend(self, backend: str | None) -> bool:
        return True

# -- Backend ---------------------------------------------------------------

    @property
    def default_in_url(self) -> str | None:
        """The default value for :attr:`DDGS_Search.in_url`."""
        return self.get_default_in_url()

    def get_default_in_url(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.in_url`.

        Returns:
           Default in-URL.
        """
        return self.get_default_options().in_url

    @property
    def in_url(self) -> str | None:
        """The in-URL of DDGS search."""
        return self.get_in_url()

    @in_url.setter
    def in_url(self, in_url: str | None = None) -> None:
        self.set_in_url(in_url)

    def get_in_url(self, default: str | None = None) -> str | None:
        """Gets the in-URL of DDGS search.

        If the in-URL is ``None``, returns `default`.

        Parameters:
           default: Default in-URL.

        Returns:
           In-URL or ``None``.
        """
        in_url = self.options.in_url
        if in_url is None:
            in_url = default
        return in_url

    def set_in_url(self, in_url: str | None = None) -> None:
        """Sets the in-URL of DDGS search.

        If `in_url` is ``None``, resets it to the default.

        Parameters:
           in_url: In-URL.
        """
        self._set_option_with_hooks(
            in_url,
            self.options.get_in_url,
            functools.partial(
                self.options.set_in_url,
                function=self.set_in_url,
                name='in_url',
                position=1),
            self._set_in_url)

    def _set_in_url(self, in_url: str | None) -> bool:
        return True

# -- Item match regex ------------------------------------------------------

    @property
    def default_item_match(self) -> str | None:
        """The default value for :attr:`DDGS_Search.item_match`."""
        return self.get_default_item_match()

    def get_default_item_match(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.item_match`.

        Returns:
           Default item match regex.
        """
        return self.get_default_options().item_match

    @property
    def item_match(self) -> str | None:
        """The item match regex of DDGS search."""
        return self.get_item_match()

    @item_match.setter
    def item_match(self, item_match: str | None = None) -> None:
        self.set_item_match(item_match)

    def get_item_match(self, default: str | None = None) -> str | None:
        """Gets the item match regex of DDGS search.

        If the item match regex is ``None``, returns `default`.

        Parameters:
           default: Default item_match.

        Returns:
           Item match regex or ``None``.
        """
        item_match = self.options.item_match
        if item_match is None:
            item_match = default
        return item_match

    def set_item_match(self, item_match: str | None = None) -> None:
        """Sets the item match regex of DDGS search.

        If `item_match` is ``None``, resets it to the default.

        Parameters:
           item_match: Item match regex.
        """
        self._set_option_with_hooks(
            item_match,
            self.options.get_item_match,
            functools.partial(
                self.options.set_item_match,
                function=self.set_item_match,
                name='item_match',
                position=1),
            self._set_item_match)

    def _set_item_match(self, item_match: str | None) -> bool:
        self._re_item = None
        return True

# -- Item sub --------------------------------------------------------------

    @property
    def default_item_sub(self) -> str | None:
        """The default value for :attr:`DDGS_Search.item_sub`."""
        return self.get_default_item_sub()

    def get_default_item_sub(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.item_sub`.

        Returns:
           Default item sub.
        """
        return self.get_default_options().item_sub

    @property
    def item_sub(self) -> str | None:
        """The item sub of DDGS search."""
        return self.get_item_sub()

    @item_sub.setter
    def item_sub(self, item_sub: str | None = None) -> None:
        self.set_item_sub(item_sub)

    def get_item_sub(self, default: str | None = None) -> str | None:
        """Gets the item sub of DDGS search.

        If the item sub is ``None``, returns `default`.

        Parameters:
           default: Default item_sub.

        Returns:
           Item sub or ``None``.
        """
        item_sub = self.options.item_sub
        if item_sub is None:
            item_sub = default
        return item_sub

    def set_item_sub(self, item_sub: str | None = None) -> None:
        """Sets the item sub of DDGS search.

        If `item_sub` is ``None``, resets it to the default.

        Parameters:
           item_sub: Item sub.
        """
        self._set_option_with_hooks(
            item_sub,
            self.options.get_item_sub,
            functools.partial(
                self.options.set_item_sub,
                function=self.set_item_sub,
                name='item_sub',
                position=1),
            self._set_item_sub)

    def _set_item_sub(self, item_sub: str | None) -> bool:
        self._re_item = None
        return True

# -- Lexeme match regex ----------------------------------------------------

    @property
    def default_lexeme_match(self) -> str | None:
        """The default value for :attr:`DDGS_Search.lexeme_match`."""
        return self.get_default_lexeme_match()

    def get_default_lexeme_match(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.lexeme_match`.

        Returns:
           Default lexeme match regex.
        """
        return self.get_default_options().lexeme_match

    @property
    def lexeme_match(self) -> str | None:
        """The lexeme match regex of DDGS search."""
        return self.get_lexeme_match()

    @lexeme_match.setter
    def lexeme_match(self, lexeme_match: str | None = None) -> None:
        self.set_lexeme_match(lexeme_match)

    def get_lexeme_match(self, default: str | None = None) -> str | None:
        """Gets the lexeme match regex of DDGS search.

        If the lexeme match regex is ``None``, returns `default`.

        Parameters:
           default: Default lexeme_match.

        Returns:
           Lexeme match regex or ``None``.
        """
        lexeme_match = self.options.lexeme_match
        if lexeme_match is None:
            lexeme_match = default
        return lexeme_match

    def set_lexeme_match(self, lexeme_match: str | None = None) -> None:
        """Sets the lexeme match regex of DDGS search.

        If `lexeme_match` is ``None``, resets it to the default.

        Parameters:
           lexeme_match: Lexeme match regex.
        """
        self._set_option_with_hooks(
            lexeme_match,
            self.options.get_lexeme_match,
            functools.partial(
                self.options.set_lexeme_match,
                function=self.set_lexeme_match,
                name='lexeme_match',
                position=1),
            self._set_lexeme_match)

    def _set_lexeme_match(self, lexeme_match: str | None) -> bool:
        self._re_lexeme = None
        return True

# -- Lexeme sub ------------------------------------------------------------

    @property
    def default_lexeme_sub(self) -> str | None:
        """The default value for :attr:`DDGS_Search.lexeme_sub`."""
        return self.get_default_lexeme_sub()

    def get_default_lexeme_sub(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.lexeme_sub`.

        Returns:
           Default lexeme sub.
        """
        return self.get_default_options().lexeme_sub

    @property
    def lexeme_sub(self) -> str | None:
        """The lexeme sub of DDGS search."""
        return self.get_lexeme_sub()

    @lexeme_sub.setter
    def lexeme_sub(self, lexeme_sub: str | None = None) -> None:
        self.set_lexeme_sub(lexeme_sub)

    def get_lexeme_sub(self, default: str | None = None) -> str | None:
        """Gets the lexeme sub of DDGS search.

        If the lexeme sub is ``None``, returns `default`.

        Parameters:
           default: Default lexeme_sub.

        Returns:
           Lexeme sub or ``None``.
        """
        lexeme_sub = self.options.lexeme_sub
        if lexeme_sub is None:
            lexeme_sub = default
        return lexeme_sub

    def set_lexeme_sub(self, lexeme_sub: str | None = None) -> None:
        """Sets the lexeme sub of DDGS search.

        If `lexeme_sub` is ``None``, resets it to the default.

        Parameters:
           lexeme_sub: Lexeme sub.
        """
        self._set_option_with_hooks(
            lexeme_sub,
            self.options.get_lexeme_sub,
            functools.partial(
                self.options.set_lexeme_sub,
                function=self.set_lexeme_sub,
                name='lexeme_sub',
                position=1),
            self._set_lexeme_sub)

    def _set_lexeme_sub(self, lexeme_sub: str | None) -> bool:
        self._re_lexeme = None
        return True

# -- Property match regex --------------------------------------------------

    @property
    def default_property_match(self) -> str | None:
        """The default value for :attr:`DDGS_Search.property_match`."""
        return self.get_default_property_match()

    def get_default_property_match(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.property_match`.

        Returns:
           Default property match regex.
        """
        return self.get_default_options().property_match

    @property
    def property_match(self) -> str | None:
        """The property match regex of DDGS search."""
        return self.get_property_match()

    @property_match.setter
    def property_match(self, property_match: str | None = None) -> None:
        self.set_property_match(property_match)

    def get_property_match(self, default: str | None = None) -> str | None:
        """Gets the property match regex of DDGS search.

        If the property match regex is ``None``, returns `default`.

        Parameters:
           default: Default property_match.

        Returns:
           Property match regex or ``None``.
        """
        property_match = self.options.property_match
        if property_match is None:
            property_match = default
        return property_match

    def set_property_match(self, property_match: str | None = None) -> None:
        """Sets the property match regex of DDGS search.

        If `property_match` is ``None``, resets it to the default.

        Parameters:
           property_match: Property match regex.
        """
        self._set_option_with_hooks(
            property_match,
            self.options.get_property_match,
            functools.partial(
                self.options.set_property_match,
                function=self.set_property_match,
                name='property_match',
                position=1),
            self._set_property_match)

    def _set_property_match(self, property_match: str | None) -> bool:
        self._re_property = None
        return True

# -- Property sub ----------------------------------------------------------

    @property
    def default_property_sub(self) -> str | None:
        """The default value for :attr:`DDGS_Search.property_sub`."""
        return self.get_default_property_sub()

    def get_default_property_sub(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.property_sub`.

        Returns:
           Default property sub.
        """
        return self.get_default_options().property_sub

    @property
    def property_sub(self) -> str | None:
        """The property sub of DDGS search."""
        return self.get_property_sub()

    @property_sub.setter
    def property_sub(self, property_sub: str | None = None) -> None:
        self.set_property_sub(property_sub)

    def get_property_sub(self, default: str | None = None) -> str | None:
        """Gets the property sub of DDGS search.

        If the property sub is ``None``, returns `default`.

        Parameters:
           default: Default property_sub.

        Returns:
           Property sub or ``None``.
        """
        property_sub = self.options.property_sub
        if property_sub is None:
            property_sub = default
        return property_sub

    def set_property_sub(self, property_sub: str | None = None) -> None:
        """Sets the property sub of DDGS search.

        If `property_sub` is ``None``, resets it to the default.

        Parameters:
           property_sub: Property sub.
        """
        self._set_option_with_hooks(
            property_sub,
            self.options.get_property_sub,
            functools.partial(
                self.options.set_property_sub,
                function=self.set_property_sub,
                name='property_sub',
                position=1),
            self._set_property_sub)

    def _set_property_sub(self, property_sub: str | None) -> bool:
        self._re_property = None
        return True

# -- Site ------------------------------------------------------------------

    @property
    def default_site(self) -> str | None:
        """The default value for :attr:`DDGS_Search.site`."""
        return self.get_default_site()

    def get_default_site(self) -> str | None:
        """Gets the default value for :attr:`DDGS_Search.site`.

        Returns:
           Default site.
        """
        return self.get_default_options().site

    @property
    def site(self) -> str | None:
        """The site of DDGS search."""
        return self.get_site()

    @site.setter
    def site(self, site: str | None = None) -> None:
        self.set_site(site)

    def get_site(self, default: str | None = None) -> str | None:
        """Gets the site of DDGS search.

        If the site is ``None``, returns `default`.

        Parameters:
           default: Default site.

        Returns:
           Site or ``None``.
        """
        site = self.options.site
        if site is None:
            site = default
        return site

    def set_site(self, site: str | None = None) -> None:
        """Sets the site of DDGS search.

        If `site` is ``None``, resets it to the default.

        Parameters:
           site: Site.
        """
        self._set_option_with_hooks(
            site,
            self.options.get_site,
            functools.partial(
                self.options.set_site,
                function=self.set_site,
                name='site',
                position=1),
            self._set_site)

    def _set_site(self, site: str | None) -> bool:
        return True

# -- Parsing ---------------------------------------------------------------

    @override
    def _to_item(self, data: DDGS_Search.TData) -> Item:
        return Item(data['href'])

    @override
    def to_item_descriptor(
            self,
            data: DDGS_Search.TData
    ) -> tuple[Item, Item.Descriptor]:
        return (self._to_item(data), cast(
            Item.Descriptor, self._to_x_descriptor(data)))

    @override
    def _to_lexeme(self, data: DDGS_Search.TData) -> Lexeme:
        return Lexeme(data['href'])

    @override
    def to_lexeme_descriptor(
            self,
            data: DDGS_Search.TData
    ) -> tuple[Lexeme, Lexeme.Descriptor]:
        return self._to_lexeme(data), {}

    @override
    def _to_property(self, data: DDGS_Search.TData) -> Property:
        return Property(data['href'])

    @override
    def to_property_descriptor(
            self,
            data: DDGS_Search.TData
    ) -> tuple[Property, Property.Descriptor]:
        return (self._to_property(data), cast(
            Property.Descriptor, self._to_x_descriptor(data)))

    def _to_x_descriptor(
            self,
            data: DDGS_Search.TData,
            empty: dict[str, Any] = {}
    ) -> dict[str, Any]:
        try:
            res: dict[str, Any] = collections.defaultdict(dict)
            if 'title' in data:
                res['labels']['en'] = Text(data['title'], 'en')
            if 'body' in data:
                res['descriptions']['en'] = Text(data['body'], 'en')
            return dict(res)
        except KeyError:
            return empty

# -- Search ----------------------------------------------------------------

    @override
    def _item_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[DDGS_Search.TData]:
        return self._x_data('item', search, options, *self.re_item)

    @override
    def _lexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[DDGS_Search.TData]:
        return self._x_data('lexeme', search, options, *self.re_lexeme)

    @override
    def _property_data(
            self,
            search: str,
            options: TOptions
    ) -> Iterator[DDGS_Search.TData]:
        return self._x_data('lexeme', search, options, *self.re_property)

    def _x_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions,
            regex: re.Pattern[str] | None,
            repl: str | None
    ) -> Iterator[DDGS_Search.TData]:
        backend, debug, in_url, limit, site, timeout =\
            self._check_options(options)
        return self._x_data_tail(
            type, search, backend, debug, in_url, limit, site, timeout,
            functools.partial(self._match_and_sub_href, regex, repl, debug))

    def _x_data_tail(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            backend: str,
            debug: bool,
            in_url: str | None,
            limit: int,
            site: str | None,
            timeout: int | None,
            match_and_sub: Callable[
                [DDGS_Search.TData], DDGS_Search.TData | None],
    ) -> Iterator[DDGS_Search.TData]:
        try:
            from ddgs import DDGS  # type: ignore
            from ddgs.exceptions import DDGSException  # type: ignore
        except ImportError as err:
            raise ImportError(
                f'{self.__class__.__qualname__} '
                f'requires {_DDGS_URL}') from err
        assert isinstance(self.ddgs, DDGS)
        if in_url:
            search += ' inurl:' + in_url
        if site:
            search += ' site:' + site
        ###
        # TODO: Move the max_results constant (100) to an option. (?)
        ###
        ddgs_text_kwargs = {
            'backend': backend,
            'max_results': 100,
            'timelimit': timeout,
        }
        ddgs_text = functools.partial(
            self.ddgs.text, search, **ddgs_text_kwargs)
        count, page = 0, 1
        while count < limit:
            try:
                if _logger.isEnabledFor(logging.DEBUG):
                    import pprint
                    _logger.debug(
                        '%s()\n%s',
                        self._x_data_tail.__qualname__, pprint.pformat(dict(
                            search=search, page=page, **ddgs_text_kwargs)))
                for t in map(match_and_sub, ddgs_text(page=page)):
                    if t is not None:
                        yield t
                        count += 1
                page += 1
            except DDGSException as err:
                _logger.debug(err)
                break

    def _check_options(
            self,
            options: TOptions
    ) -> tuple[str, bool, str | None, int, str | None, int | None]:
        backend = options.backend
        if backend is None:
            backend = 'auto'
        debug = bool(options.debug)
        in_url = options.in_url
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        else:
            limit = min(limit, options.max_limit)
        site = options.site
        timeout = (
            int(options.timeout) if options.timeout is not None else None)
        return backend, debug, in_url, limit, site, timeout

    def _match_and_sub_href(
            self,
            regex: re.Pattern[str] | None,
            repl: str | None,
            debug: bool,
            data: DDGS_Search.TData
    ) -> DDGS_Search.TData | None:
        if 'href' not in data:
            return None
        if regex is None:
            return data
        href = data['href']
        if regex.match(href):
            if repl is not None:
                data['href'] = regex.sub(repl, href)
            return data
        elif debug:
            _logger.debug('skipping %s', href)
        return None

    @override
    def _aitem_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[DDGS_Search.TData]:
        return self._ax_data('item', search, options, *self.re_item)

    @override
    def _alexeme_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[DDGS_Search.TData]:
        return self._ax_data('item', search, options, *self.re_lexeme)

    @override
    def _aproperty_data(
            self,
            search: str,
            options: TOptions
    ) -> AsyncIterator[DDGS_Search.TData]:
        return self._ax_data('item', search, options, *self.re_property)

    async def _ax_data(
            self,
            type: Literal['item', 'lexeme', 'property'],
            search: str,
            options: TOptions,
            regex: re.Pattern[str] | None,
            repl: str | None
    ) -> AsyncIterator[DDGS_Search.TData]:
        backend, debug, in_url, limit, site, timeout =\
            self._check_options(options)
        match_and_sub = functools.partial(
            self._match_and_sub_href, regex, repl, debug)
        for t in await asyncio.create_task(asyncio.to_thread(
            lambda: self._x_data_tail(
                type, search, backend, debug, in_url, limit, site, timeout,
                match_and_sub))):
            yield t
