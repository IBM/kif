# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    ExternalId,
    Filter,
    Fingerprint,
    IRI,
    Quantity,
    Time,
    Variables,
)
from kif_lib.compiler.sparql.mapping.wikidata import WikidataMapping
from kif_lib.store.sparql2 import SPARQL_Store2
from kif_lib.typing import Any, Final, override
from kif_lib.vocabulary import wd

from .....tests import SPARQL_Store2TestCase

w, x, y, z = Variables(*'wxyz')


class Test(SPARQL_Store2TestCase):

    WIKIDATA: Final[str | None] = os.getenv('WIKIDATA')

    @classmethod
    def setUpClass(cls) -> None:
        if not cls.WIKIDATA:
            raise unittest.SkipTest('WIKIDATA is not set')

    @override
    @classmethod
    def new_Store(cls, *args: Any, **kwargs: Any) -> SPARQL_Store2:
        assert cls.WIKIDATA is not None
        return SPARQL_Store2(
            'sparql2', cls.WIKIDATA,
            WikidataMapping(strict=True), *args, **kwargs)

    def test_item_item(self) -> None:
        fps = [
            Fingerprint.check(wd.part_of(wd.Adam_and_Eve)),
            -(wd.significant_person(wd.Adam_and_Eve)),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, wd.Freebase_ID, '/m/09_c5v'),  # VV
                     (wd.Freebase_ID(wd.Adam, '/m/09_c5v'))),
                ],
                contains=[
                    (Filter(fp, wd.WordNet_31_Synset_ID), [  # VF
                        wd.WordNet_31_Synset_ID(wd.Adam, '09609728-n'),
                        wd.WordNet_31_Synset_ID(wd.Eve, '09609918-n'),
                    ]),
                    (Filter(fp, None, wd.Adam_and_Eve), [  # FV
                        wd.part_of(wd.Adam, wd.Adam_and_Eve),
                        wd.part_of(wd.Eve, wd.Adam_and_Eve)
                    ]),
                ])

    def test_item_property(self) -> None:
        fps = [
            Fingerprint.check(wd.Wikidata_property(wd.mass)),
            -(wd.measured_physical_quantity(wd.Q(613726))),  # item-item
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, None, 'm'),  # FV
                     wd.quantity_symbol_string(wd.mass_, 'm')),
                ],
                contains=[
                    (Filter(fp, wd.Wikidata_property, wd.mass), [  # VV
                        wd.Wikidata_property(wd.mass_, wd.mass),
                    ]),
                    (Filter(fp, wd.quantity_symbol_string, None), [  # VF
                        wd.quantity_symbol_string(wd.mass_, 'M'),
                        wd.quantity_symbol_string(wd.mass_, 'm'),
                    ]),
                ])

    def test_item_lexeme(self) -> None:
        fps = [
            Fingerprint.check(wd.subject_lexeme(wd.L(39504))),
            -(wd.said_to_be_the_same_as(wd.Q(21285812))),  # item-item
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, wd.subject_lexeme, wd.L(39504)),  # VV
                     wd.subject_lexeme(wd.Q(325872), wd.L(39504))),
                    (Filter(fp, wd.instance_of, None),  # VF
                     wd.instance_of(wd.Q(325872), wd.female_given_name)),
                    (Filter(fp, None, wd.female_given_name),  # FV
                     wd.instance_of(wd.Q(325872), wd.female_given_name)),
                ])

    def test_item_iri(self) -> None:
        fps = [
            Fingerprint.check(wd.official_website('https://www.ibm.com/')),
            -(wd.manufacturer(wd.Watson)),  # item-item
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(
                        fp, wd.official_name,  # VV
                        'International Business Machines Corporation'),
                     wd.official_name(
                         wd.IBM,
                         'International Business Machines Corporation')),
                    (Filter(fp, wd.country),  # VF
                     wd.country(wd.IBM, wd.United_States_of_America)),
                    (Filter(fp, None, wd.Endicott),  # FV
                     wd.location_of_formation(wd.IBM, wd.Endicott)),
                ])

    def test_item_text(self) -> None:
        fps = [
            Fingerprint.check(wd.official_name(
                'International Business Machines Corporation')),
            -(wd.developer(wd.IBM_AIX)),  # item-item
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, wd.official_website, 'https://www.ibm.com/'),
                     wd.official_website(wd.IBM, 'https://www.ibm.com/')),
                    (Filter(fp, wd.country),  # VF
                     wd.country(wd.IBM, wd.United_States_of_America)),
                    (Filter(fp, None, wd.Endicott),  # FV
                     wd.location_of_formation(wd.IBM, wd.Endicott)),
                ])

    def test_item_string(self) -> None:
        fps = [
            Fingerprint.check(
                wd.canonical_SMILES('CN1C=NC2=C1C(=O)N(C(=O)N2C)C')),
            -(wd.has_active_ingredient(wd.Q(64148184))),  # item-item
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, wd.named_after, wd.coffee),
                     wd.named_after(wd.caffeine, wd.coffee)),
                    (Filter(fp, wd.named_after, None),
                     wd.named_after(wd.caffeine, wd.coffee)),
                    (Filter(fp, None, wd.coffee),
                     wd.named_after(wd.caffeine, wd.coffee)),
                ])

    def test_item_external_id(self) -> None:
        fps = [
            Fingerprint.check(wd.Freebase_ID('/m/09_c5v')),
            -(wd.father(wd.Q(107626))),  # item-item
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, wd.Freebase_ID, '/m/09_c5v'),  # VV
                     wd.Freebase_ID(wd.Adam, '/m/09_c5v')),
                    (Filter(fp, wd.part_of, None),  # VF
                     wd.part_of(wd.Adam, wd.Adam_and_Eve)),
                    (Filter(fp, None, ExternalId('09609728-n')),  # FV
                     wd.WordNet_31_Synset_ID(wd.Adam, '09609728-n')),
                ])

    def test_item_quantity(self) -> None:
        self._test_filter(
            empty=[
                Filter(wd.mass(Quantity('194.08', None, 1)),
                       wd.named_after, wd.coffee),
                Filter(wd.mass(Quantity('194.08', None, None, 200)),
                       wd.named_after, wd.coffee),
            ],
            equals=[
                (Filter(wd.mass('194.08'), wd.named_after, wd.coffee),  # VV
                 wd.named_after(wd.caffeine, wd.coffee)),
                (Filter(wd.mass('194.08'@wd.dalton), wd.named_after),  # VF
                 wd.named_after(wd.caffeine, wd.coffee)),
                (Filter(wd.mass('194.08'@wd.dalton), None, wd.coffee),  # FV
                 wd.named_after(wd.caffeine, wd.coffee)),
            ])

    def test_item_time(self) -> None:
        self._test_filter(
            empty=[
                Filter(wd.inception(Time('1911-06-16', 0)),
                       wd.official_website),
                Filter(wd.inception(Time('1911-06-16', None, 1)),
                       wd.official_website),
                Filter(wd.inception(Time(
                    '1911-06-16', None, None, wd.proleptic_Julian_calendar)),
                    wd.official_website),
            ],
            contains=[
                (Filter(wd.inception('1911-06-16'), wd.official_website), [
                    wd.official_website(wd.IBM, 'https://www.ibm.com/'),  # VV
                    wd.official_website(
                        wd.Q(11457573),
                        'https://map.japanpost.jp/p/search/dtl/300141053000/'),
                ]),
                (Filter(wd.inception('1822-09-07'), wd.continent), [  # VF
                    wd.continent(wd.Brazil, wd.South_America),
                    wd.continent(wd.Q(217230), wd.South_America),
                ]),
                (Filter(wd.inception('1822-09-07'), None, wd.South_America), [
                    wd.continent(wd.Brazil, wd.South_America),  # FV
                    wd.continent(wd.Q(217230), wd.South_America),
                ]),
            ])

    def test_property_item(self) -> None:
        fps = [
            Fingerprint.check(wd.Wikidata_item_of_this_property(wd.mass_)),
            -(wd.subproperty_of(wd.payload_mass)),  # property-property
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(    # VV
                        fp, wd.Wikidata_item_of_this_property, wd.mass_),
                     (wd.Wikidata_item_of_this_property(wd.mass, wd.mass_))),
                    (Filter(fp, wd.equivalent_property),  # VF
                     wd.equivalent_property(
                         wd.mass, 'https://schema.org/weight')),
                    (Filter(
                        fp, None, IRI('https://schema.org/weight')),  # FV
                     wd.equivalent_property(
                         wd.mass, 'https://schema.org/weight')),
                ])

    def test_property_property(self) -> None:
        fps = [
            Fingerprint.check(wd.inverse_property(wd.part_of)),
            -(wd.subproperty_of(  # property-property
                wd.contains_the_administrative_territorial_entity)),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(    # VV
                        fp, wd.negates_property, wd.does_not_have_part),
                     (wd.negates_property(
                         wd.has_part, wd.does_not_have_part))),
                    (Filter(fp, wd.negates_property),  # VF
                     wd.negates_property(wd.has_part, wd.does_not_have_part)),
                ],
                contains=[
                    (Filter(fp, None, wd.does_not_have_part), [  # FV
                        wd.negates_property(
                            wd.has_part, wd.does_not_have_part),
                        wd.complementary_property(
                            wd.has_part, wd.does_not_have_part),
                    ])
                ])

    def test_property_lexeme(self) -> None:
        fps = [
            Fingerprint.check(
                wd.Wikidata_property_example_for_lexemes(wd.L(2879))),
            -(wd.related_property(wd.grammatical_person)),  # property-property
        ]
        url = 'http://www.lexinfo.net/ontology/2.0/lexinfo#gender'
        for fp in fps:
            self._test_filter(
                contains=[
                    (Filter(fp, wd.equivalent_property, url), [  # VV
                        wd.equivalent_property(wd.grammatical_gender, url),
                    ]),
                    (Filter(fp, wd.equivalent_property), [  # VF
                        wd.equivalent_property(wd.grammatical_gender, url),
                    ]),
                    (Filter(fp, None, IRI(url)), [  # FV
                        wd.equivalent_property(wd.grammatical_gender, url),
                    ]),
                ])

    def test_property_iri(self) -> None:
        pass

    def test_property_text(self) -> None:
        pass

    def test_property_string(self) -> None:
        pass

    def test_property_external_id(self) -> None:
        pass

    def test_property_quantity(self) -> None:
        pass

    def test_property_time(self) -> None:
        pass

    def test_lexeme_item(self) -> None:
        pass

    def test_lexeme_property(self) -> None:
        pass

    def test_lexeme_lexeme(self) -> None:
        pass

    def test_lexeme_iri(self) -> None:
        pass

    def test_lexeme_text(self) -> None:
        pass

    def test_lexeme_string(self) -> None:
        pass

    def test_lexeme_external_id(self) -> None:
        pass

    def test_lexeme_quantity(self) -> None:
        pass

    def test_lexeme_time(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
