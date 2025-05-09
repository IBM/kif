# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any
from .abc import Store
from .empty import EmptyStore
from .mixer import MixerStore
from .sparql import SPARQL_Store


@dataclasses.dataclass
class StoreOptions(Store._Options, name='store'):
    """Store options."""

    empty: EmptyStore.Options = dataclasses.field(
        default_factory=EmptyStore.Options)

    mixer: MixerStore.Options = dataclasses.field(
        default_factory=MixerStore.Options)

    sparql: SPARQL_Store.Options = dataclasses.field(
        default_factory=SPARQL_Store.Options)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptyStore.Options()
        self.mixer = MixerStore.Options()
        self.sparql = SPARQL_Store.Options()
