# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any
from .empty import EmptyStoreOptions
from .mixer import MixerStoreOptions
from .options_ import _StoreOptions


@dataclasses.dataclass
class StoreOptions(_StoreOptions, name='store'):
    """Common store options."""

    empty: EmptyStoreOptions = dataclasses.field(
        default_factory=EmptyStoreOptions)

    mixer: MixerStoreOptions = dataclasses.field(
        default_factory=MixerStoreOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptyStoreOptions()
        self.mixer = MixerStoreOptions()
