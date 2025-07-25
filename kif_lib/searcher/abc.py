# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..context import Context
from ..engine import _EngineOptions, Engine, EngineOptions
from ..model import KIF_Object
from ..typing import Any, cast, ClassVar, Iterable, Mapping, override, TypeVar


@dataclasses.dataclass
class _SearcherOptions(EngineOptions):
    """Base class for searcher options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_SEARCHER_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCHER_MAX_LIMIT',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCHER_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCHER_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCHER_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_SEARCHER_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_SEARCHER_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_SEARCHER_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.searcher


@dataclasses.dataclass
class SearcherOptions(_SearcherOptions):
    """Base class for searcher options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Searcher ==============================================================

TOptions = TypeVar('TOptions', bound=SearcherOptions)


class Searcher(Engine[TOptions]):
    """Abstract base class for entity searchers."""

    #: The searcher plugin registry.
    registry: ClassVar[Mapping[str, type[Searcher]]] = {}  # pyright: ignore

    #: The name of this searcher plugin.
    searcher_name: ClassVar[str]

    #: The description of this searcher plugin.
    searcher_description: ClassVar[str]

    @classmethod
    def __init_subclass__(
            cls,
            searcher_name: str,
            searcher_description: str
    ) -> None:
        Searcher._register_plugin(cls, searcher_name, searcher_description)
        cls.searcher_name = cls.plugin_name
        cls.searcher_description = cls.plugin_description

    def __new__(cls, searcher_name: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            searcher_name, searcher_name in cls.registry,
            f"no such searcher plugin '{searcher_name}'",
            Searcher, 'searcher_name', 1, ValueError)
        return super().__new__(cls.registry[searcher_name])  # pyright: ignore

    class Error(Engine.Error):
        """Base class for searcher errors."""

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cast(TOptions, cls.get_context(context).options.searcher.empty)
