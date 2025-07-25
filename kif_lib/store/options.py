# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..engine import _EngineOptions
from ..typing import Any, override
from .abc import _StoreOptions
from .empty import EmptyStoreOptions
from .memory import MemoryStoreOptions
from .mixer import MixerStoreOptions
from .sparql import SPARQL_StoreOptions


@dataclasses.dataclass
class StoreOptions(_StoreOptions, name='store'):
    """Store options."""

    empty: EmptyStoreOptions = dataclasses.field(
        default_factory=EmptyStoreOptions)

    memory: MemoryStoreOptions = dataclasses.field(
        default_factory=MemoryStoreOptions)

    mixer: MixerStoreOptions = dataclasses.field(
        default_factory=MixerStoreOptions)

    sparql: SPARQL_StoreOptions = dataclasses.field(
        default_factory=SPARQL_StoreOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptyStoreOptions()
        self.memory = MemoryStoreOptions()
        self.mixer = MixerStoreOptions()
        self.sparql = SPARQL_StoreOptions()

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.engine
