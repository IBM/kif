# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..context import Context
from ..engine import _EngineOptions, Engine, EngineOptions
from ..model import KIF_Object
from ..typing import Any, cast, ClassVar, Iterable, Mapping, override, TypeVar


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

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.search


@dataclasses.dataclass
class SearchOptions(_SearchOptions):
    """Base class for search options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Search ==============================================================

TOptions = TypeVar('TOptions', bound=SearchOptions)


class Search(Engine[TOptions]):
    """Abstract base class for entity search engines."""

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
