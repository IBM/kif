# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.exceptions import Error as RDFLibError
from rdflib.namespace import DCTERMS as DCT
from rdflib.namespace import (
    DefinedNamespace,
    FOAF,
    Namespace,
    NamespaceManager,
    OWL,
    RDF,
    RDFS,
    SKOS,
    split_uri,
    XSD,
)
from rdflib.parser import InputSource
from rdflib.query import Result
from rdflib.term import _NUMERIC_LITERAL_TYPES, Identifier, Variable

__all__ = (
    '_NUMERIC_LITERAL_TYPES',
    'BNode',
    'DCT',
    'DefinedNamespace',
    'FOAF',
    'Graph',
    'Identifier',
    'InputSource',
    'Literal',
    'Namespace',
    'NamespaceManager',
    'OWL',
    'RDF',
    'RDFLibError',
    'RDFS',
    'Result',
    'SKOS',
    'split_uri',
    'URIRef',
    'Variable',
    'XSD',
)
