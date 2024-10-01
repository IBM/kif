# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    ExternalId,
    Filter,
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
        self._test_filter_matches(
            Filter(value_mask=Filter.ITEM, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Item(z))))

    def test_value_fp_property(self) -> None:
        self._test_filter_matches(
            Filter(value_mask=Filter.PROPERTY, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(y, Property(z).generalize())))

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


if __name__ == '__main__':
    Test.main()
