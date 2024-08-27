# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import (
    DCT,
    FOAF,
    Graph,
    NamespaceManager,
    OWL,
    RDF,
    RDFS,
    SKOS,
    XSD,
)
from .ontolex import ONTOLEX
from .prov import PROV
from .schema import SCHEMA
from .wikibase import WIKIBASE
from .wikidata import T_NS as T_NS_
from .wikidata import T_URI as T_URI_
from .wikidata import Wikidata

__all__ = [
    'DCT',
    'FOAF',
    'ONTOLEX',
    'OWL',
    'P',
    'PQ',
    'PQN',
    'PQV',
    'PR',
    'PRN',
    'PROV',
    'PS',
    'PSN',
    'PSV',
    'RDF',
    'RDFS',
    'SCHEMA',
    'SKOS',
    'WD',
    'WDATA',
    'WDNO',
    'WDREF',
    'WDS',
    'WDT',
    'WDV',
    'WIKIBASE',
    'Wikidata',
    'XSD',
]

T_NS = T_NS_
T_URI = T_URI_

P = Wikidata.P
PQ = Wikidata.PQ
PQN = Wikidata.PQN
PQV = Wikidata.PQV
PR = Wikidata.PR
PRN = Wikidata.PRN
PRV = Wikidata.PRV
PS = Wikidata.PS
PSN = Wikidata.PSN
PSV = Wikidata.PSV
WD = Wikidata.WD
WDATA = Wikidata.WDATA
WDGENID = Wikidata.WDGENID
WDNO = Wikidata.WDNO
WDREF = Wikidata.WDREF
WDS = Wikidata.WDS
WDT = Wikidata.WDT
WDV = Wikidata.WDV

PREFIXES = {
    'dct': DCT,
    'owl': OWL,
    'prov': PROV,
    'rdf': RDF,
    'rdfs': RDFS,
    'schema': SCHEMA,
    'skos': SKOS,
    'wikibase': WIKIBASE,
    'xsd': XSD,
    **Wikidata.prefixes
}

_DEFAULT_NSM = NamespaceManager(Graph(), bind_namespaces='none')
for k, v in PREFIXES.items():
    _DEFAULT_NSM.bind(k, v)
