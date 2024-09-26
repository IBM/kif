# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..compiler.sparql import SPARQL_Mapping
from ..model import T_IRI
from ..typing import Any
from .sparql2 import SPARQL_Store2


class PubChemStore(
        SPARQL_Store2,
        store_name='pubchem',
        store_description='PubChem store'
):
    """Wikidata store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       iri: PubChem SPARQL endpoint IRI.
       mapping: PubChem SPARQL mapping.
    """

    def __init__(
            self,
            store_name: str,
            iri: T_IRI,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        if mapping is None:
            from ..compiler.sparql.mapping.pubchem import PubChemMapping
            mapping = PubChemMapping()
        super().__init__(store_name, iri, mapping, **kwargs)
