# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import Filter, Fingerprint, Variables
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
            Fingerprint.check(wd.Freebase_ID('/m/09_c5v')),
            -(wd.father(wd.Q(107626))),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(    # VV
                        wd.Adam_and_Eve, wd.significant_person, fp),
                     wd.significant_person(wd.Adam_and_Eve, wd.Adam)),
                    (Filter(    # VF
                        wd.Garden_of_Eden, None, fp),
                     wd.significant_person(wd.Garden_of_Eden, wd.Adam))
                ],
                contains=[
                    (Filter(    # FV
                        None, wd.significant_person, fp), [
                        wd.significant_person(wd.Adam_and_Eve, wd.Adam),
                        wd.significant_person(wd.Garden_of_Eden, wd.Adam),
                    ]),
                ])

    def test_item_property(self) -> None:
        fps = [
            Fingerprint.check(wd.Wikidata_item_of_this_property(wd.mass_)),
            -(wd.subproperty_of(wd.payload_mass)),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(    # VV
                        wd.human, wd.properties_for_this_type, fp),
                     wd.properties_for_this_type(wd.human, wd.mass)),
                    (Filter(    # VF
                        wd.human, None, fp),
                     wd.properties_for_this_type(wd.human, wd.mass)),
                ],
                contains=[
                    (Filter(    # FV
                        None, wd.properties_for_this_type, fp), [
                        wd.properties_for_this_type(wd.human, wd.mass),
                    ]),
                ])

    def test_item_lexeme(self) -> None:
        pass

    def test_item_iri(self) -> None:
        pass

    def test_item_text(self) -> None:
        pass

    def test_item_string(self) -> None:
        pass

    def test_item_external_id(self) -> None:
        pass

    def test_item_quantity(self) -> None:
        pass

    def test_item_time(self) -> None:
        pass

    def test_property_item(self) -> None:
        fps = [
            Fingerprint.check(wd.Wikidata_item_of_this_property(wd.mass_)),
            -(wd.subproperty_of(wd.payload_mass)),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(    # VV
                        wd.payload_mass, wd.subproperty_of, fp),
                     (wd.subproperty_of(wd.payload_mass, wd.mass))),
                    (Filter(    # VF
                        wd.payload_mass, None, fp),
                     (wd.subproperty_of(wd.payload_mass, wd.mass))),
                    (Filter(    # FV
                        None, wd.subproperty_of, fp),
                     (wd.subproperty_of(wd.payload_mass, wd.mass)))
                ])

    def test_lexeme(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
