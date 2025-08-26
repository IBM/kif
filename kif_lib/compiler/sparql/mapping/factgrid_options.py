# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....typing import Any
from .wikidata_options import WikidataMappingOptions


@dataclasses.dataclass
class FactGridMappingOptions(WikidataMappingOptions, name='factgrid'):
    """FactGrid SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
