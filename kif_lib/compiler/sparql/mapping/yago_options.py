# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from ....typing import Any


@dataclasses.dataclass
class YagoMappingOptions(Section, name='yago'):
    """Yago SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        pass
