# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import Namespace
from ..typing import Final


class DBpedia:
    """The DBpedia namespace."""

    DBPEDIA: Final[Namespace] = Namespace('http://dbpedia.org/')
    ONTOLOGY: Final[Namespace] = Namespace(DBPEDIA['ontology/'])
    PROPERTY: Final[Namespace] = Namespace(DBPEDIA['property/'])
    RESOURCE: Final[Namespace] = Namespace(DBPEDIA['resource/'])

    namespaces: Final[dict[str, Namespace]] = {
        str(ONTOLOGY): ONTOLOGY,
        str(PROPERTY): PROPERTY,
        str(RESOURCE): RESOURCE,
    }

    prefixes: Final[dict[str, Namespace]] = {
        'dbo': ONTOLOGY,
        'dbp': PROPERTY,
        'dbr': RESOURCE,
    }
