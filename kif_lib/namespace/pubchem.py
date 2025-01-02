# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import Namespace
from ..typing import Final


class PubChem:
    """The PubChem namespace."""

    PUBCHEM: Final[Namespace] = Namespace(
        'http://rdf.ncbi.nlm.nih.gov/pubchem/')

    COMPOUND: Final[Namespace] = Namespace(PUBCHEM['compound/'])
    CONCEPT: Final[Namespace] = Namespace(str(PUBCHEM) + 'concept/')
    PATENT: Final[Namespace] = Namespace(PUBCHEM['patent/'])
    SOURCE: Final[Namespace] = Namespace(str(PUBCHEM) + 'source/')
    VOCABULARY: Final[Namespace] = Namespace(str(PUBCHEM) + 'vocabulary#')

    namespaces: Final[dict[str, Namespace]] = {
        str(COMPOUND): COMPOUND,
        str(CONCEPT): CONCEPT,
        str(PATENT): PATENT,
        str(PUBCHEM): PUBCHEM,
        str(SOURCE): SOURCE,
        str(VOCABULARY): VOCABULARY,
    }
