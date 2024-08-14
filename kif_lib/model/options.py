# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses

from ..context import Section
from .value.options import ValueOptions


@dataclasses.dataclass
class ModelOptions(Section):
    """Model options."""

    value: 'ValueOptions' = dataclasses.field(default_factory=ValueOptions)
