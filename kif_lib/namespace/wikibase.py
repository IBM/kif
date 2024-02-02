# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class WIKIBASE(DefinedNamespace):
    _NS = Namespace('http://wikiba.se/ontology#')
    BestRank: URIRef
    DeprecatedRank: URIRef
    ExternalId: URIRef
    isSomeValue: URIRef
    lemma: URIRef
    lexicalCategory: URIRef
    Monolingualtext: URIRef
    NormalRank: URIRef
    PreferredRank: URIRef
    propertyType: URIRef
    Quantity: URIRef
    quantityAmount: URIRef
    quantityLowerBound: URIRef
    quantityUnit: URIRef
    quantityUpperBound: URIRef
    QuantityValue: URIRef
    rank: URIRef
    String: URIRef
    Time: URIRef
    timeCalendarModel: URIRef
    timePrecision: URIRef
    timeTimezone: URIRef
    TimeValue: URIRef
    timeValue: URIRef
    Url: URIRef
    WikibaseItem: URIRef
    WikibaseLexeme: URIRef
    WikibaseProperty: URIRef
