# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any, ClassVar, Iterable
from .abc import Searcher, SearcherOptions


@dataclasses.dataclass
class EmptySearcherOptions(SearcherOptions, name='empty'):
    """Empty searcher options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_EMPTY_SEARCHER_DEBUG',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class EmptySearcher(
        Searcher[EmptySearcherOptions],
        searcher_name='empty',
        searcher_description='Empty searcher'
):
    """Empty searcher.

    Parameters:
       searcher_name: Name of the searcher plugin to instantiate.
    """

    def __init__(self, searcher_name: str, *args: Any, **kwargs: Any) -> None:
        assert searcher_name == self.searcher_name
        super().__init__(*args, **kwargs)
