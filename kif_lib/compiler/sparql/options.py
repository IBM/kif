# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ...context import Section
from .mapping.options import MappingOptions


@dataclasses.dataclass
class SPARQL_Options(Section, name='sparql'):
    """SPARQL compiler options."""

    mapping: MappingOptions = dataclasses.field(
        default_factory=MappingOptions)
