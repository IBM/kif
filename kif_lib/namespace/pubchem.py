# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import Namespace
from ..typing import Final


class PubChem:
    """The PubChem namespace."""

    PUBCHEM: Final[Namespace] = Namespace(
        'http://rdf.ncbi.nlm.nih.gov/pubchem/')

    COMPOUND: Final[Namespace] = Namespace(PUBCHEM['compound/'])

    PATENT: Final[Namespace] = Namespace(PUBCHEM['patent/'])

    namespaces: Final[dict[str, Namespace]] = {
        str(PUBCHEM): PUBCHEM,
        str(COMPOUND): COMPOUND,
        str(PATENT): PATENT,
    }
