# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import Filter, Item, Text, Variables
from kif_lib.compiler.sparql.mapping.wikidata import WikidataMapping
from kif_lib.store.sparql2 import SPARQL_Store2
from kif_lib.typing import Any, Final, override
from kif_lib.vocabulary import wd

from ....tests import SPARQL_Store2TestCase

x, y, z = Variables(*'xyz')


class Test(SPARQL_Store2TestCase):

    WIKIDATA: Final[str | None] = os.getenv('WIKIDATA')

    @classmethod
    def setUpClass(cls):
        if not cls.WIKIDATA:
            raise unittest.SkipTest('WIKIDATA is not set')

    @override
    @classmethod
    def new_Store(cls, *args: Any, **kwargs: Any) -> SPARQL_Store2:
        assert cls.WIKIDATA is not None
        return SPARQL_Store2(
            'sparql2', cls.WIKIDATA,
            WikidataMapping(strict=True), *args, **kwargs)

    def test_empty(self) -> None:
        self._test_filter_preset_empty()

    def test_subject_item(self) -> None:
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
                    wd.participant_in(wd.Fall_of_man),
                    wd.Freebase_ID('/m/09_c5v'),
                    wd.WordNet_31_Synset_ID('09609728-n'),
                ]),
            ])


if __name__ == '__main__':
    Test.main()
