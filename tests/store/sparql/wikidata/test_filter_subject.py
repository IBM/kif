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
    Item,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    SomeValueSnak,
    Statement,
    Text,
    Time,
    Variables,
)
from kif_lib.compiler.sparql.mapping.wikidata import WikidataMapping
from kif_lib.store.sparql2 import SPARQL_Store2
from kif_lib.typing import Any, Final, override
from kif_lib.vocabulary import wd

from ....tests import SPARQL_Store2TestCase

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

    def test_value_fp_item(self) -> None:
        self._test_filter(
            empty=[
                Filter(Item('x')),    # bad item IRI
                Filter(wd.Q('xxx')),  # bad item IRI
                Filter(wd.Q(10**10)),  # no such item
            ])
        self._test_filter_with_fixed_subject(
            subject=wd.Adam,
            empty=[
                (wd.instance_of, wd.type_of_a_chemical_entity),  # VV
                (wd.continent, None),                            # VF
                (None, 1@wd.kilogram),                           # FV
            ],
            equals=[
                ((wd.part_of, wd.Adam_and_Eve),  # VV
                 wd.part_of(wd.Adam_and_Eve)),
                ((wd.date_of_birth, None),  # VF
                 wd.date_of_birth.some_value()),
                ((wd.father, None),
                 wd.father.no_value()),
                ((wd.part_of, None),
                 wd.part_of(wd.Adam_and_Eve)),
                ((None, Text('אָדָם', 'he')),  # FV
                 wd.name_in_native_language(Text('אָדָם', 'he'))),
            ],
            contains=[
                ((None, None), [  # FF
                    wd.instance_of(wd.human_biblical_figure),
                    wd.instance_of(wd.protoplast),
                    wd.instance_of(wd.mythical_character),
                    wd.part_of(wd.Adam_and_Eve),
                    wd.sex_or_gender(wd.male),
                    wd.name_in_native_language(Text('אָדָם', 'he')),
                    wd.family_name.some_value(),
                    wd.date_of_birth.some_value(),
                    wd.place_of_birth(wd.Garden_of_Eden),
                    wd.father.no_value(),
                    wd.mother.no_value(),
                    wd.spouse(wd.Eve),
                    wd.Freebase_ID('/m/09_c5v'),
                    wd.WordNet_31_Synset_ID('09609728-n'),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(subject_mask=Filter.ITEM), Statement(Item(x), y))

    def test_value_fp_property(self) -> None:
        self._test_filter(
            empty=[
                Filter(Property('x')),  # bad property IRI
                Filter(wd.P('xxx')),    # bad property IRI
                Filter(wd.P(10**10)),   # no such property
            ])
        self._test_filter_with_fixed_subject(
            subject=wd.mass,
            empty=[
                (wd.instance_of, wd.type_of_a_chemical_entity),  # VV
                (wd.continent, None),                            # VF
                (None, 1@wd.kilogram),                           # FV
            ],
            equals=[
                ((wd.Wikidata_item_of_this_property, wd.mass_),  # VV
                 wd.Wikidata_item_of_this_property(wd.mass_)),
                ((wd.equivalent_property, IRI('https://schema.org/weight')),
                 (wd.equivalent_property(IRI('https://schema.org/weight')))),
                ((wd.equivalent_property, None),  # VF
                 (wd.equivalent_property(IRI('https://schema.org/weight')))),
                ((None, IRI('https://schema.org/weight')),  # FV
                 (wd.equivalent_property(IRI('https://schema.org/weight')))),
            ],
            contains=[          # FF
                ((None, None), [
                    wd.instance_of(
                        wd.Wikidata_property_for_physical_quantities),
                    wd.instance_of(
                        wd.Wikidata_property_related_to_animals_and_zoology),
                    wd.Wikidata_item_of_this_property(wd.mass_),
                    wd.equivalent_property(IRI('https://schema.org/weight')),
                    wd.type_of_unit_for_this_property(wd.unit_of_mass),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(subject_mask=Filter.PROPERTY),
            Statement(Property(x, y), z))

    def test_value_fp_lexeme(self) -> None:
        self._test_filter(
            empty=[
                Filter(Lexeme('x')),  # bad lexeme IRI
                Filter(wd.L('xxx')),  # bad lexeme IRI
                Filter(wd.L(10**10)),  # no such lexeme
            ])
        self._test_filter_with_fixed_subject(
            subject=wd.L(4129),
            empty=[
                (wd.instance_of, wd.type_of_a_chemical_entity),  # VV
                (wd.continent, None),                            # VF
                (None, 1@wd.kilogram),                           # FV
            ],
            contains=[          # FF
                ((None, None), [
                    wd.described_by_source(wd.Q(58489371)),
                    wd.derived_from_lexeme(wd.L(348331)),
                    wd.homograph_lexeme(wd.L(333796)),
                    wd.homograph_lexeme(wd.L(16927)),
                    wd.homograph_lexeme(wd.L(337374)),
                    wd.Dictionary_of_American_Regional_English_ID(
                        'ID_00029294'),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(subject_mask=Filter.LEXEME), Statement(Lexeme(x), y))

    def test_value_fp_entity_some_value(self) -> None:
        self._test_filter_matches(
            Filter(wd.Adam, snak_mask=Filter.SOME_VALUE_SNAK),
            Statement(wd.Adam, SomeValueSnak(y)))

    def test_value_fp_entity_no_value(self) -> None:
        self._test_filter_matches(
            Filter(wd.Adam, snak_mask=Filter.NO_VALUE_SNAK),
            Statement(wd.Adam, NoValueSnak(y)))

    def test_snak_fp_item_item(self) -> None:
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

    def test_snak_fp_item_property(self) -> None:
        fp = wd.Wikidata_property(wd.mass)
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

    def test_snak_fp_item_lexeme(self) -> None:
        fp = wd.subject_lexeme(wd.L(39504))
        self._test_filter(
            equals=[
                (Filter(fp, wd.subject_lexeme, wd.L(39504)),  # VV
                 wd.subject_lexeme(wd.Q(325872), wd.L(39504))),
                (Filter(fp, wd.instance_of, None),  # VF
                 wd.instance_of(wd.Q(325872), wd.female_given_name)),
                (Filter(fp, None, wd.female_given_name),  # FV
                 wd.instance_of(wd.Q(325872), wd.female_given_name)),
            ])

    def test_snak_fp_item_iri(self) -> None:
        fp = wd.official_website('https://www.ibm.com/')
        self._test_filter(
            equals=[
                (Filter(fp, wd.official_name,  # VV
                        'International Business Machines Corporation'),
                 wd.official_name(
                     wd.IBM, 'International Business Machines Corporation')),
                (Filter(fp, wd.country),  # VF
                 wd.country(wd.IBM, wd.United_States_of_America)),
                (Filter(fp, None, wd.Endicott),  # FV
                 wd.location_of_formation(wd.IBM, wd.Endicott)),
            ])

    def test_snak_fp_item_text(self) -> None:
        fp = wd.official_name('International Business Machines Corporation')
        self._test_filter(
            equals=[
                (Filter(fp, wd.official_website, 'https://www.ibm.com/'),
                 wd.official_website(wd.IBM, 'https://www.ibm.com/')),
                (Filter(fp, wd.country),  # VF
                 wd.country(wd.IBM, wd.United_States_of_America)),
                (Filter(fp, None, wd.Endicott),  # FV
                 wd.location_of_formation(wd.IBM, wd.Endicott)),
            ])

    def test_snak_fp_item_string(self) -> None:
        fp = wd.canonical_SMILES('CN1C=NC2=C1C(=O)N(C(=O)N2C)C')
        self._test_filter(
            equals=[
                (Filter(fp, wd.named_after, wd.coffee),
                 wd.named_after(wd.caffeine, wd.coffee)),
                (Filter(fp, wd.named_after, None),
                 wd.named_after(wd.caffeine, wd.coffee)),
                (Filter(fp, None, wd.coffee),
                 wd.named_after(wd.caffeine, wd.coffee)),
            ])

    def test_snak_fp_item_external_id(self) -> None:
        fp = wd.Freebase_ID('/m/09_c5v')
        self._test_filter(
            equals=[
                (Filter(fp, wd.Freebase_ID, '/m/09_c5v'),  # VV
                 wd.Freebase_ID(wd.Adam, '/m/09_c5v')),
                (Filter(fp, wd.part_of, None),  # VF
                 wd.part_of(wd.Adam, wd.Adam_and_Eve)),
                (Filter(fp, None, ExternalId('09609728-n')),  # FV
                 wd.WordNet_31_Synset_ID(wd.Adam, '09609728-n')),
            ])

    def test_snak_fp_item_quantity(self) -> None:
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

    def test_snak_fp_item_time(self) -> None:
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

    def test_snak_fp_property_item(self) -> None:
        fp = wd.Wikidata_item_of_this_property(wd.mass_)
        self._test_filter(
            equals=[
                (Filter(fp, wd.Wikidata_item_of_this_property, wd.mass_),  # VV
                 (wd.Wikidata_item_of_this_property(wd.mass, wd.mass_))),
                (Filter(fp, wd.equivalent_property),  # VF
                 wd.equivalent_property(wd.mass, 'https://schema.org/weight')),
                (Filter(fp, None, IRI('https://schema.org/weight')),  # FV
                 wd.equivalent_property(wd.mass, 'https://schema.org/weight')),
            ])

    def test_snak_fp_property_property(self) -> None:
        fp = wd.inverse_property(wd.part_of)
        self._test_filter(
            equals=[
                (Filter(fp, wd.negates_property, wd.does_not_have_part),  # VV
                 (wd.negates_property(wd.has_part, wd.does_not_have_part))),
                (Filter(fp, wd.negates_property),  # VF
                 wd.negates_property(wd.has_part, wd.does_not_have_part)),
            ],
            contains=[
                (Filter(fp, None, wd.does_not_have_part), [  # FV
                    wd.negates_property(wd.has_part, wd.does_not_have_part),
                    wd.complementary_property(
                        wd.has_part, wd.does_not_have_part),
                ])
            ])

    def test_snak_fp_property_lexeme(self) -> None:
        fp = wd.Wikidata_property_example_for_lexemes(wd.L(2879))
        self._test_filter(
            equals=[
                (Filter(        # VV
                    fp, wd.equivalent_property,
                    'http://www.lexinfo.net/ontology/2.0/lexinfo#gender'),
                 wd.equivalent_property(
                     wd.grammatical_gender,
                     'http://www.lexinfo.net/ontology/2.0/lexinfo#gender')),
                (Filter(fp, wd.equivalent_property),  # VF
                 wd.equivalent_property(
                     wd.grammatical_gender,
                     'http://www.lexinfo.net/ontology/2.0/lexinfo#gender')),
                (Filter(        # FV
                    fp, None,
                    IRI('http://www.lexinfo.net/ontology/2.0/lexinfo#gender')),
                 wd.equivalent_property(
                     wd.grammatical_gender,
                     'http://www.lexinfo.net/ontology/2.0/lexinfo#gender')),
            ])

    def test_snak_fp_property_iri(self) -> None:
        pass

    def test_snak_fp_property_text(self) -> None:
        pass

    def test_snak_fp_property_string(self) -> None:
        pass

    def test_snak_fp_property_external_id(self) -> None:
        pass

    def test_snak_fp_property_quantity(self) -> None:
        pass

    def test_snak_fp_property_time(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
