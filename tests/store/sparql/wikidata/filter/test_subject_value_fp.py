# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    Filter,
    IRI,
    Item,
    Lexeme,
    Property,
    Statement,
    Text,
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

    def test_item(self) -> None:
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
            ],
            contains=[
                ((None, Text('אָדָם', 'he')), [  # FV
                    wd.alias(Text('אָדָם', 'he')),
                    wd.name_in_native_language(Text('אָדָם', 'he')),
                ]),
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

    def test_property(self) -> None:
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

    def test_lexeme(self) -> None:
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


if __name__ == '__main__':
    Test.main()
