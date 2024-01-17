# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class PROV(DefinedNamespace):
    _NS = Namespace('http://www.w3.org/ns/prov#')
    wasDerivedFrom: URIRef
