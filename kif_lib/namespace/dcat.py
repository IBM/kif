# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class DCAT(DefinedNamespace):
    """DCAT 3 Vocabulary. Open EP Data's Patent Ontology.

    See <https://www.w3.org/ns/dcat>.
    """

    _NS = Namespace('http://www.w3.org/ns/dcat#')
    Dataset: URIRef
    landingPage: URIRef
    theme: URIRef
