# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from .dbpedia_options import DBpediaMappingOptions
from .europa_options import EuropaMappingOptions
from .factgrid_options import FactGridMappingOptions
from .pubchem_options import PubChemMappingOptions
from .uniprot_options import UniProtMappingOptions
from .wikidata_options import WikidataMappingOptions
from .yago_options import YagoMappingOptions


@dataclasses.dataclass
class MappingOptions(Section, name='mapping'):
    """SPARQL mapping options."""

    dbpedia: DBpediaMappingOptions = dataclasses.field(
        default_factory=DBpediaMappingOptions)

    europa: EuropaMappingOptions = dataclasses.field(
        default_factory=EuropaMappingOptions)

    factgrid: FactGridMappingOptions = dataclasses.field(
        default_factory=FactGridMappingOptions)

    pubchem: PubChemMappingOptions = dataclasses.field(
        default_factory=PubChemMappingOptions)

    uniprot: UniProtMappingOptions = dataclasses.field(
        default_factory=UniProtMappingOptions)

    wikidata: WikidataMappingOptions = dataclasses.field(
        default_factory=WikidataMappingOptions)

    yago: YagoMappingOptions = dataclasses.field(
        default_factory=YagoMappingOptions)
