# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class EUVOC(DefinedNamespace):
    """The EU vocabulary."""

    _NS = Namespace('http://publications.europa.eu/ontology/euvoc#')
    DataTheme: URIRef
