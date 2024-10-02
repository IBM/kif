# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    Filter,
    NoValueSnak,
    SomeValueSnak,
    Statement,
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

    def test_value_fp_value(self) -> None:
        self._test_filter_matches(
            Filter(wd.Adam, snak_mask=Filter.VALUE_SNAK),
            Statement(wd.Adam, ValueSnak(x, y)))
        self._test_filter_matches(
            Filter(None, wd.date_of_birth, snak_mask=Filter.VALUE_SNAK),
            Statement(x, ValueSnak(wd.date_of_birth, y)))

    def test_value_fp_some_value(self) -> None:
        self._test_filter_matches(
            Filter(wd.Adam, snak_mask=Filter.SOME_VALUE_SNAK),
            Statement(wd.Adam, SomeValueSnak(y)))
        self._test_filter_matches(
            Filter(None, wd.date_of_birth, snak_mask=Filter.SOME_VALUE_SNAK),
            Statement(x, SomeValueSnak(wd.date_of_birth)))

    def test_value_fp_no_value(self) -> None:
        self._test_filter_matches(
            Filter(wd.Adam, snak_mask=Filter.NO_VALUE_SNAK),
            Statement(wd.Adam, NoValueSnak(y)))
        self._test_filter_matches(
            Filter(None, wd.father, snak_mask=Filter.NO_VALUE_SNAK),
            Statement(x, NoValueSnak(wd.father)))


if __name__ == '__main__':
    Test.main()
