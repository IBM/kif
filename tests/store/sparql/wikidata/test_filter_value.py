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
    Property,
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

    def test_empty(self) -> None:
        self._test_filter_preset_empty()

    def test_value_fp_item(self) -> None:
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

    def test_value_fp_property(self) -> None:
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

    def test_value_fp_lexeme(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.LEXEME, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Lexeme(z))))

    def test_value_fp_iri(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.IRI, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, IRI(z))))

    def test_value_fp_text(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.TEXT, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Text(z, w))))

    def test_value_fp_string(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.STRING, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, String(z))))

    def test_value_fp_external_id(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.EXTERNAL_ID, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, ExternalId(z))))

    def test_value_fp_quantity(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.QUANTITY, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Quantity(z).generalize())))

    def test_value_fp_time(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.TIME, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Time(z).generalize())))

    def test_snak_fp_item(self) -> None:
        fps = [
            Fingerprint.check(wd.Freebase_ID('/m/09_c5v')),
            -(wd.father(wd.Q(107626))),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(wd.Adam_and_Eve, wd.significant_person, fp),  # VV
                     wd.significant_person(wd.Adam_and_Eve, wd.Adam)),
                    (Filter(wd.Garden_of_Eden, None, fp),  # VF
                     wd.significant_person(wd.Garden_of_Eden, wd.Adam))
                ],
                contains=[
                    (Filter(None, wd.significant_person, fp), [  # FV
                        wd.significant_person(wd.Adam_and_Eve, wd.Adam),
                        wd.significant_person(wd.Garden_of_Eden, wd.Adam),
                    ]),
                ])

    def test_snak_fp_property(self) -> None:
        pass

    def test_snak_fp_lexeme(self) -> None:
        pass

    def test_snak_fp_uri(self) -> None:
        pass

    def test_snak_fp_text(self) -> None:
        pass

    def test_snak_fp_string(self) -> None:
        pass

    def test_snak_fp_external_id(self) -> None:
        pass

    def test_snak_fp_quantity(self) -> None:
        pass

    def test_snak_fp_time(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
