# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses

from ...context import Section
from .text import TextOptions


@dataclasses.dataclass
class ValueOptions(Section):
    """Value options."""

    text: 'TextOptions' = dataclasses.field(default_factory=TextOptions)
