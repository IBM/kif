# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..context import Section
from .rdf.options import RDF_Options


@dataclasses.dataclass
class CodecOptions(Section, name='codec'):
    """Codec options."""

    rdf: RDF_Options = dataclasses.field(default_factory=RDF_Options)
