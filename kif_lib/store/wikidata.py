# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..compiler.sparql.filter_compiler import SPARQL_FilterCompiler
from ..model import IRI, T_IRI
from ..typing import Any, ClassVar
from .sparql import SPARQL_Store


class WikidataStore(
        SPARQL_Store,
        store_name='wikidata',
        store_description='Wikidata store'
):
    """Wikidata store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       iri: Wikidata SPARQL endpoint IRI.
    """

    #: The default Wikidata SPARQL endpoint IRI.
    _default_iri: ClassVar[IRI] = IRI('https://query.wikidata.org/sparql')

    #: Flags to be passed to filter compiler.
    _compile_filter_flags: ClassVar[SPARQL_FilterCompiler.Flags] = (
        SPARQL_FilterCompiler.default_flags
        | SPARQL_FilterCompiler.WIKIDATA_EXTENSIONS)

    def __init__(
            self,
            store_name: str,
            iri: T_IRI | None = None,
            **kwargs: Any
    ) -> None:
        iri = iri if iri is not None else self._default_iri
        super().__init__(store_name, iri, **kwargs)
