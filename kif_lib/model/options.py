# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..context import Section
from .value.options import ValueOptions


@dataclasses.dataclass
class ModelOptions(Section, name='model'):
    """Model options."""

    value: ValueOptions = dataclasses.field(default_factory=ValueOptions)
