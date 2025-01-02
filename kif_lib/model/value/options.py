# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ...context import Section
from .text import TextOptions


@dataclasses.dataclass
class ValueOptions(Section, name='value'):
    """Value options."""

    text: TextOptions = dataclasses.field(default_factory=TextOptions)
