# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..rdflib import DefinedNamespace, Namespace, URIRef


class WIKIBASE(DefinedNamespace):
    _NS = Namespace('http://wikiba.se/ontology#')
    BestRank: URIRef
    DeprecatedRank: URIRef
    ExternalId: URIRef
    Monolingualtext: URIRef
    NormalRank: URIRef
    PreferredRank: URIRef
    Property: URIRef
    Quantity: URIRef
    QuantityValue: URIRef
    String: URIRef
    Time: URIRef
    TimeValue: URIRef
    Url: URIRef
    WikibaseItem: URIRef
    WikibaseLexeme: URIRef
    WikibaseProperty: URIRef
    claim: URIRef
    directClaim: URIRef
    isSomeValue: URIRef
    lemma: URIRef
    lexicalCategory: URIRef
    novalue: URIRef
    propertyType: URIRef
    quantityAmount: URIRef
    quantityLowerBound: URIRef
    quantityUnit: URIRef
    quantityUpperBound: URIRef
    rank: URIRef
    statementProperty: URIRef
    timeCalendarModel: URIRef
    timePrecision: URIRef
    timeTimezone: URIRef
    timeValue: URIRef
