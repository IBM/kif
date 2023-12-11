# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class WIKIBASE(DefinedNamespace):
    _NS = Namespace('http://wikiba.se/ontology#')
    BestRank: URIRef
    DeprecatedRank: URIRef
    NormalRank: URIRef
    PreferredRank: URIRef
    QuantityValue: URIRef
    TimeValue: URIRef
    isSomeValue: URIRef
    quantityAmount: URIRef
    quantityLowerBound: URIRef
    quantityUnit: URIRef
    quantityUpperBound: URIRef
    rank: URIRef
    timeCalendarModel: URIRef
    timePrecision: URIRef
    timeTimezone: URIRef
    timeValue: URIRef
