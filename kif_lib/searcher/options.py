# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any
from . import abc
from .empty import EmptySearcherOptions


@dataclasses.dataclass
class SearcherOptions(abc._SearcherOptions, name='searcher'):
    """Searcher options."""

    empty: EmptySearcherOptions = dataclasses.field(
        default_factory=EmptySearcherOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptySearcherOptions()
