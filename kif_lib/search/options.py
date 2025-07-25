# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..engine import _EngineOptions
from ..typing import Any, override
from .abc import _SearchOptions
from .empty import EmptySearchOptions


@dataclasses.dataclass
class SearchOptions(_SearchOptions, name='search'):
    """Search options."""

    empty: EmptySearchOptions = dataclasses.field(
        default_factory=EmptySearchOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptySearchOptions()

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.engine
