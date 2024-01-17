# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import (
    DecoderError,
    EntityFingerprint,
    FilterPattern,
    KIF_Object,
    Quantity,
    Value,
)

from .tests import kif_TestCase, main


class TestSPARQL_Decoder(kif_TestCase):

    def test_from_sparql(self):
        # bad query
        self.assertRaisesRegex(DecoderError, 'bad query',
                               FilterPattern.from_sparql, 'xxx')
        # bad return
        self.assertRaises(
            TypeError, Value.from_sparql, 'select * where {?s ?p ?o}')
        # no restrictions
        q = 'select * where {?s ?p ?o}'
        self.assert_filter_pattern(KIF_Object.from_sparql(q))
        # subject: item
        q = 'select * where {wd:Q2270 ?p ?o}'
        self.assert_filter_pattern(KIF_Object.from_sparql(q), wd.benzene)
        # subject: property
        q = 'select * where {wd:P31 ?p ?o}'
        self.assert_filter_pattern(KIF_Object.from_sparql(q), wd.instance_of)
        # property: property
        q = 'select * where {?s wd:P31 ?o}'
        self.assert_filter_pattern(
            KIF_Object.from_sparql(q), None, wd.instance_of)
        # value: item
        q = 'select * where {?s ?p wd:Q2270}'
        self.assert_filter_pattern(
            KIF_Object.from_sparql(q), None, None, wd.benzene)

    def test_text2sparql(self):
        # Give me the mass of benzene.
        q = '''
SELECT ?value WHERE {
    wd:Q2270 wdt:P2067 ?value .
} LIMIT 50'''
        self.assert_filter_pattern(
            KIF_Object.from_sparql(q),
            EntityFingerprint(wd.benzene),
            wd.mass)
        # Give me the LD50 of benzene.
        q = '''
SELECT ?value WHERE {
    wd:Q2270 wdt:P2240 ?value .
} LIMIT 50'''
        self.assert_filter_pattern(
            FilterPattern.from_sparql(q),
            wd.benzene,
            wd.median_lethal_dose)
        # What is the solubility of benzene?
        q = '''
SELECT ?value WHERE {
    wd:Q2270 wdt:P2177 ?value .
} LIMIT 50'''
        self.assert_filter_pattern(
            FilterPattern.from_sparql(q),
            wd.benzene,
            wd.solubility)
        # Give me the mass of the compound with
        # InChIKey "UHOVQNZJYSORNB-UHFFFAOYSA-N".
        q = '''
SELECT ?mass WHERE {
    ?compound wdt:P235 "UHOVQNZJYSORNB-UHFFFAOYSA-N".
    ?compound wdt:P31/wdt:P279* wd:Q11173 .
    ?compound wdt:P2067 ?mass .
} LIMIT 50'''
        self.assert_filter_pattern(
            FilterPattern.from_sparql(q),
            wd.InChIKey('UHOVQNZJYSORNB-UHFFFAOYSA-N'),
            wd.mass)
        q = '''
SELECT ?value WHERE {
?compound wdt:P234 "InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H" .
?compound wdt:P31 wd:Q11173 .
?compound wdt:P2067 ?value .
} LIMIT 50
'''
        self.assert_filter_pattern(
            FilterPattern.from_sparql(q),
            [wd.InChI('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H'),
             wd.instance_of(wd.chemical_compound)],
            wd.mass)
        # What are the chemical entity types with solubility 0.07?
        q = '''
SELECT ?entity_type WHERE {
    ?entity_type wdt:P2305 wd:Q43460564 .
    ?entity_type wdt:P2177 "0.07"^^xsd:decimal .
} LIMIT 50'''
        self.assert_filter_pattern(
            FilterPattern.from_sparql(q),
            [wd.solubility(Quantity('0.07')),
             wd.P(2305)(wd.chemical_entity)])
        # Give me the reports that are about benzene
        q = '''
SELECT ?report WHERE {
    ?report wdt:P31/wdt:P279* wd:Q10870555 .
    ?report wdt:P361 wd:Q2270 .
} LIMIT 50
'''
        self.assert_filter_pattern(
            FilterPattern.from_sparql(q),
            None, wd.part_of, wd.benzene)


if __name__ == '__main__':
    main()
