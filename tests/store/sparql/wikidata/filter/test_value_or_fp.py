# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import Filter, Item, Property, Quantity, Variables
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
            equals=[
                (Filter(        # VV
                    wd.Brazil, wd.shares_border_with,
                    wd.Argentina | wd.Chile | Item('x')),
                 wd.shares_border_with(wd.Brazil, wd.Argentina)),
            ],
            contains=[
                (Filter(        # VV
                    wd.Brazil, wd.shares_border_with,
                    wd.Argentina | wd.Chile | wd.Peru), [
                        wd.shares_border_with(wd.Brazil, wd.Argentina),
                        wd.shares_border_with(wd.Brazil, wd.Peru),
                ]),
                (Filter(        # FV
                    wd.Adam, None, wd.Adam_and_Eve | wd.Eve), [
                        wd.part_of(wd.Adam, wd.Adam_and_Eve),
                        wd.spouse(wd.Adam, wd.Eve),
                        wd.partner_in_business_or_sport(wd.Adam, wd.Eve),
                ]),
                (Filter(        # VF
                    None, wd.shares_border_with,
                    wd.Argentina | wd.Chile | wd.Peru
                    | Item('x') | Property('y')), [
                        wd.shares_border_with(wd.Argentina, wd.Chile),
                        wd.shares_border_with(wd.Bolivia, wd.Chile),
                        wd.shares_border_with(wd.Brazil, wd.Argentina),
                        wd.shares_border_with(wd.Brazil, wd.Peru),
                        wd.shares_border_with(wd.Uruguay, wd.Argentina),
                ]),
            ])

    def test_property(self) -> None:
        self._test_filter(
            equals=[
                (Filter(        # VV
                    wd.has_part, wd.inverse_property,
                    wd.part_of | wd.has_part),
                 wd.inverse_property(wd.has_part, wd.part_of)),
                (Filter(        # VF
                    wd.field_of_work, None,
                    wd.occupation | wd.mass | Property('x')),
                 wd.related_property(wd.field_of_work, wd.occupation)),
            ],
            contains=[
                (Filter(        # FV
                    None, wd.subproperty_of, wd.mass | wd.part_of), [
                        wd.subproperty_of(wd.participant_in, wd.part_of),
                        wd.subproperty_of(wd.payload_mass, wd.mass),
                        wd.subproperty_of(wd.season, wd.part_of),
                        wd.subproperty_of(wd.transport_network, wd.part_of),
                ]),
            ])

    def test_lexeme(self) -> None:
        pass

    def test_iri(self) -> None:
        pass

    def test_text(self) -> None:
        pass

    def test_string(self) -> None:
        pass

    def test_external_id(self) -> None:
        pass

    def test_quantity(self) -> None:
        self._test_filter(
            equals=[
                (Filter(         # VV
                    wd.caffeine, wd.mass,
                    '194.08'@wd.dalton | 1@wd.kilogram),
                 wd.mass(wd.caffeine, '194.08'@wd.dalton)),
                (Filter(
                    wd.caffeine, wd.mass,
                    Quantity('194.08') | '194.08'@wd.kilogram),
                 wd.mass(wd.caffeine, '194.08'@wd.dalton))
            ],
            contains=[
                (Filter(        # VF
                    wd._1, None, 1), [
                        wd.conversion_to_SI_unit(
                            wd._1, Quantity(1, wd._1, 1, 1)),
                        wd.number_of_decimal_digits(wd._1, 1@wd._1),
                        wd.numeric_value(wd._1, 1@wd._1),
                ]),
                (Filter(        # FV
                    None, wd.mass, '194.08'@wd.dalton | 194@wd.kilogram), [
                        wd.mass(wd.Q(27277733), Quantity(
                            '194.08', wd.dalton, '194.08', '194.08')),
                        wd.mass(wd.caffeine, '194.08'@wd.dalton),
                        wd.mass(wd.Q(122973289), 194@wd.kilogram),
                ])
            ])

    def test_time(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
