# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any, ClassVar, Iterable
from .abc import Search, SearchOptions


@dataclasses.dataclass
class EmptySearchOptions(SearchOptions, name='empty'):
    """Empty search options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_EMPTY_SEARCH_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_SEARCH_MAX_LIMIT',), None)

    _v_language: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_EMPTY_SEARCH_LANGUAGE',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_SEARCH_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_SEARCH_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_SEARCH_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_SEARCH_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_EMPTY_SEARCH_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_EMPTY_SEARCH_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class EmptySearch(
        Search[EmptySearchOptions],
        search_name='empty',
        search_description='Empty search'
):
    """Empty search.

    Parameters:
       search_name: Name of the search plugin to instantiate.
    """

    def __init__(self, search_name: str, *args: Any, **kwargs: Any) -> None:
        assert search_name == self.search_name
        super().__init__(*args, **kwargs)
