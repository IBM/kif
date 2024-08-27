# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class ONTOLEX(DefinedNamespace):
    """W3's OntoLex namespace."""

    _NS = Namespace('http://www.w3.org/ns/lemon/ontolex#')
    LexicalEntry: URIRef
