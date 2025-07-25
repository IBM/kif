# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import functools

from ..context import Context
from ..engine import _EngineOptions, Engine, EngineOptions
from ..model import KIF_Object, String, TTextLanguage
from ..typing import (
    Any,
    cast,
    ClassVar,
    Iterable,
    Location,
    Mapping,
    Optional,
    override,
    TypeVar,
)


@dataclasses.dataclass
class _SearchOptions(EngineOptions):
    """Base class for search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCH_MAX_LIMIT',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_SEARCH_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._init_language(kwargs)

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.search

    # -- language --

    @classmethod
    def _check_language(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> str:
        return String.check(arg, function, name, position).content

    @classmethod
    def _check_optional_language(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> str | None:
        return cls._do_check_optional(
            cls._check_language, arg, default, function, name, position)

    #: The default value for the language option.
    DEFAULT_LANGUAGE: ClassVar[Optional[str]] = None

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_SEARCH_LANGUAGE',), DEFAULT_LANGUAGE)

    _language: str | None

    def _init_language(self, kwargs: dict[str, Any]) -> None:
        self.language = cast(str, kwargs.get(
            '_language', self.getenv_optional_str(*self._v_language)))

    @property
    def language(self) -> str | None:
        """The language option."""
        return self.get_language()

    @language.setter
    def language(self, language: TTextLanguage | None) -> None:
        self.set_language(language)

    def get_language(self) -> str | None:
        """Gets the language option.

        Returns:
           Language or ``None``.
        """
        return self._language

    def set_language(
            self,
            language: TTextLanguage | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the language option.

        If `language` is ``None``, assumes the default language.

        Parameters:
           language: Language.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._language = self._check_optional_language(
            language, None, function, name, position)


@dataclasses.dataclass
class SearchOptions(_SearchOptions):
    """Base class for search options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @override
    def get_language(self) -> str | None:
        return self._do_get('_language', super().get_language)

    @override
    def set_language(
            self,
            language: TTextLanguage | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(language, '_language', functools.partial(
            super().set_language,
            function=function, name=name, position=position))


# == Search ==============================================================

TOptions = TypeVar('TOptions', bound=SearchOptions, default=SearchOptions)


class Search(Engine[TOptions]):
    """Abstract base class for search engines."""

    #: The search plugin registry.
    registry: ClassVar[Mapping[str, type[Search]]] = {}  # pyright: ignore

    #: The name of this search plugin.
    search_name: ClassVar[str]

    #: The description of this search plugin.
    search_description: ClassVar[str]

    @classmethod
    def __init_subclass__(
            cls,
            search_name: str,
            search_description: str
    ) -> None:
        Search._register_plugin(cls, search_name, search_description)
        cls.search_name = cls.plugin_name
        cls.search_description = cls.plugin_description

    def __new__(cls, search_name: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            search_name, search_name in cls.registry,
            f"no such search plugin '{search_name}'",
            Search, 'search_name', 1, ValueError)
        return super().__new__(cls.registry[search_name])  # pyright: ignore

    class Error(Engine.Error):
        """Base class for search errors."""

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cast(TOptions, cls.get_context(context).options.search.empty)


# -- Initialization --------------------------------------------------------

    #: Search options.
    _options: TOptions

    def __init__(
            self,
            *args: Any,
            debug: bool | None = None,
            language: TTextLanguage | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            context: Context | None = None,
            **kwargs: Any
    ) -> None:
        """
        Initializes :class:`Search`.

        Parameters:
           search_name: Name of the search plugin to instantiate.
           args: Arguments.
           debug: Whether to enable debugging mode.
           language: Language to restrict search to.
           limit: Limit (maximum number) of responses.
           lookahead: Number of pages to lookahead asynchronously.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           context: Context.
           kwargs: Other keyword arguments.
        """
        super().__init__(
            *args,
            debug=debug,
            language=language,
            limit=limit,
            lookahead=lookahead,
            page_size=page_size,
            timeoutt=timeout,
            context=context,
            **kwargs)

    @override
    def _update_options(self, **kwargs: Any) -> None:
        super()._update_options(**kwargs)
        if 'language' in kwargs:
            self.set_language(kwargs['language'])

# -- Language --------------------------------------------------------------

    @property
    def default_language(self) -> str | None:
        """The default value for :attr:`Search.language`."""
        return self.get_default_language()

    def get_default_language(self) -> str | None:
        """Gets the default value for :attr:`Search.language`.

        Returns:
           Default Language.
        """
        return self.get_default_options().language

    @property
    def language(self) -> str | None:
        """The language of search."""
        return self.get_language()

    @language.setter
    def language(self, language: TTextLanguage | None = None) -> None:
        self.set_language(language)

    def get_language(self, default: str | None = None) -> str | None:
        """Gets the language of search.

        If the language is ``None``, returns `default`.

        Parameters:
           default: Default language.

        Returns:
           Language or ``None``.
        """
        language = self.options.language
        if language is None:
            language = default
        return language

    def set_language(
            self,
            language: TTextLanguage | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the language of search.

        If `language` is ``None``, resets it to the default.

        Parameters:
           language: Language.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._set_option_with_hooks(
            language,
            self.options.get_language,
            functools.partial(
                self.options.set_language,
                function=self.set_language,
                name='language',
                position=1),
            self._set_language)

    def _set_language(self, language: str | None) -> bool:
        return True
