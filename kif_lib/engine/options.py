# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..typing import Any
from .abc import _EngineOptions


@dataclasses.dataclass
class EngineOptions(_EngineOptions, name='engine'):
    """Engine options."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
