# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class SCHEMA(DefinedNamespace):
    """Schema.org namespace."""

    _NS = Namespace('http://schema.org/')

    description: URIRef
