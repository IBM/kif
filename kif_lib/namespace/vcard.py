# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class VCARD(DefinedNamespace):
    """W3's vCard Ontology - for describing People and Organizations."""

    _NS = Namespace('http://www.w3.org/2006/vcard/ns#')
    fn: URIRef
