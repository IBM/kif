# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef


class PATENT(DefinedNamespace):
    """Linked Open EP Data's Patent Ontology.

    See <https://pilot-data.epo.org/linked-data/documentation/
         patent-ontology-overview>.
    """

    _NS = Namespace('http://data.epo.org/linked-data/def/patent/')
    applicantVC: URIRef
    inventorVC: URIRef
    Publication: URIRef
    publicationDate: URIRef
    publicationNumber: URIRef
    titleOfInvention: URIRef
