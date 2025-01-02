# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..context import Section
from .sparql.options import SPARQL_Options


@dataclasses.dataclass
class CompilerOptions(Section, name='compiler'):
    """Compiler options."""

    sparql: SPARQL_Options = dataclasses.field(default_factory=SPARQL_Options)
