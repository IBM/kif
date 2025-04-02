# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from .pubchem_options import PubChemMappingOptions
from .wikidata_options import WikidataMappingOptions


@dataclasses.dataclass
class MappingOptions(Section, name='mapping'):
    """SPARQL mapping options."""

    pubchem: PubChemMappingOptions = dataclasses.field(
        default_factory=PubChemMappingOptions)

    wikidata: WikidataMappingOptions = dataclasses.field(
        default_factory=WikidataMappingOptions)
