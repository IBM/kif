# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any
from .empty import EmptyStore
from .mixer import MixerStore
from .options import _StoreOptions


@dataclasses.dataclass
class StoreOptionsRoot(_StoreOptions, name='store'):
    """Store options."""

    empty: EmptyStore.Options = dataclasses.field(
        default_factory=EmptyStore.Options)

    mixer: MixerStore.Options = dataclasses.field(
        default_factory=MixerStore.Options)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptyStore.Options()
        self.mixer = MixerStore.Options()
