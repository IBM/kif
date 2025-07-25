# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..engine import _EngineOptions
from ..typing import Any, override
from .abc import _SearcherOptions
from .empty import EmptySearcherOptions


@dataclasses.dataclass
class SearcherOptions(_SearcherOptions, name='searcher'):
    """Searcher options."""

    empty: EmptySearcherOptions = dataclasses.field(
        default_factory=EmptySearcherOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptySearcherOptions()

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.engine
