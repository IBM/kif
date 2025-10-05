# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib
from urllib import parse as urllib_parse

from .. import itertools
from ..rdflib import DCT, FOAF, OWL, RDF, RDFS, SKOS, XSD
from ..typing import TypeVar
from .ontolex import ONTOLEX
from .prov import PROV
from .schema import SCHEMA
from .wikibase import WIKIBASE
from .wikidata import T_NS as T_NS_
from .wikidata import T_URI as T_URI_
from .wikidata import Wikidata

__all__ = (
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
)

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

PREFIXES: dict[str, object] = {
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

_T = TypeVar('_T', bound=T_URI)


def split_uri(
        uri: T_URI,
        _empty: urllib_parse.ParseResult = urllib_parse.urlparse('')
) -> tuple[str, str]:
    """Splits URI into namespace and name.

    Parameters:
       uri: URI.

    Returns:
       The namespace and name of URI.
    """
    t = urllib_parse.urlparse(str(uri))
    if t.fragment:
        return urllib_parse.urlunparse(
            itertools.chain(t[:3], _empty[3:])) + '#', t.fragment
    else:
        path = pathlib.PurePath(t.path or '/')
        parent = str(path.parent)
        if parent[-1] != '/':
            parent += '/'
        return urllib_parse.urlunparse(itertools.chain(
            t[:2], (parent,), _empty[3:])), path.name


def validate_uri(uri: _T) -> _T:
    """Validates URI.

    Parameters:
       uri: URI.

    Returns:
       The given URI.

    Raises:
       `ValueError`: `uri` is in valid.
    """
    t = urllib_parse.urlparse(str(uri))
    if t.scheme and t.netloc:
        return uri
    else:
        raise ValueError
