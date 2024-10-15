# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from .pubchem import PubChemMapping
from .wikidata import WikidataOptions


@dataclasses.dataclass
class MappingOptions(Section, name='mapping'):
    """SPARQL mapping options."""

    pubchem: PubChemMapping.Options = dataclasses.field(
        default_factory=PubChemMapping.Options)

    wikidata: WikidataOptions = dataclasses.field(
        default_factory=WikidataOptions)
