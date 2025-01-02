# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class OBO(DefinedNamespace):
    """Open Biological and Biomedical Ontology."""

    _NS = Namespace('http://purl.obolibrary.org/obo/')

    IAO_0000115: URIRef         # definition
    RO_0000087: URIRef          # has role


class IAO:
    """The OBO IAO namespace."""
    definition = OBO.IAO_0000115


class RO:
    """The OBO RO namespace."""
    has_role = OBO.RO_0000087
