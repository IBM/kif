# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    ExternalId,
    Filter,
    IRI,
    Lexeme,
    Quantity,
    Statement,
    String,
    Text,
    Time,
    ValueSnak,
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
        self._test_filter_with_fixed_value(
            value=wd.Pico_da_Neblina,
            empty=[
                (wd.Brazil, wd.country),  # VV
                (wd.Adam, None),          # VF
                (None, wd.country),       # FV
            ],
            equals=[
                ((wd.Brazil, wd.highest_point),  # VV
                 (wd.Brazil, wd.highest_point)),
                ((wd.Brazil, None),  # VF
                 (wd.Brazil, wd.highest_point)),
                ((None, wd.parent_peak),  # FV
                 (wd.Pico_31_de_Março, wd.parent_peak)),
            ],
            contains=[
                ((None, None), [  # FF
                    (wd.Amazonas, wd.highest_point),
                    (wd.Brazil, wd.highest_point),
                    (wd.Pico_31_de_Março, wd.parent_peak),
                ]),
            ])

    def test_property(self) -> None:
        self._test_filter_with_fixed_value(
            value=wd.grammatical_gender,
            empty=[
                (wd.sex_or_gender, wd.subproperty_of),
            ],
            equals=[
                ((wd.sex_or_gender, wd.related_property),  # VV
                 (wd.sex_or_gender, wd.related_property)),
                ((wd.sex_or_gender, None),  # VF
                 (wd.sex_or_gender, wd.related_property)),
            ],
            contains=[
                ((None, wd.related_property), [  # FV
                    (wd.P(10339), wd.related_property),
                    (wd.P(5109), wd.related_property),
                    (wd.P(5713), wd.related_property),
                    (wd.sex_or_gender, wd.related_property),
                ]),
            ])

    def test_lexeme(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.LEXEME, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Lexeme(z))))

    def test_iri(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.IRI, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, IRI(z))))

    def test_text(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.TEXT, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Text(z, w))))

    def test_string(self) -> None:
        pass
        # self._test_filter_matches(
        #     Filter(value_mask=Filter.STRING, snak_mask=Filter.VALUE_SNAK),
        #     Statement(x, ValueSnak(y, String(z))))

    def test_external_id(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.EXTERNAL_ID, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, ExternalId(z))))

    def test_quantity(self) -> None:
        self._test_filter(
            empty=[
                Filter(wd.caffeine, wd.mass, Quantity('194.08', None, 1)),
                Filter(wd._1, wd.numeric_value, Quantity(1, wd._1, None, 1)),
                Filter(wd.Q(27289566), wd.mass, Quantity(
                    '194.08', None, '194.07')),
            ],
            equals=[
                (Filter(        # VV
                    wd.caffeine, wd.mass, '194.08'@wd.dalton),
                 wd.mass(wd.caffeine, '194.08'@wd.dalton)),
                (Filter(
                    wd.caffeine, wd.mass, Quantity('194.08')),
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
                    None, wd.mass, '194.08'@wd.dalton), [
                        wd.mass(wd.caffeine, '194.08'@wd.dalton),
                        wd.mass(wd.Q(27289566), Quantity(
                            '194.08', wd.dalton, '194.08', '194.08')),
                ]),
            ])

    def test_time(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.TIME, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Time(z).generalize())))


if __name__ == '__main__':
    Test.main()
