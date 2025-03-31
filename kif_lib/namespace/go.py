# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class GO(DefinedNamespace):
    """Gene ontology."""

    _NS = Namespace('http://www.geneontology.org/formats/oboInOwl#')
    hasExactSynonym: URIRef
    hasRelatedSynonym: URIRef
    inSubset: URIRef
