# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class PROV(DefinedNamespace):
    """W3's PROV namespace."""

    _NS = Namespace('http://www.w3.org/ns/prov#')
    wasDerivedFrom: URIRef
