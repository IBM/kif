# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class CITO(DefinedNamespace):
    """CiTO, the Citation Typing Ontology.

    See <https://sparontologies.github.io/cito/current/cito.html>.
    """

    _NS = Namespace('http://purl.org/spar/cito/')
    isDiscussedBy: URIRef
