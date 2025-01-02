# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import Filter, Fingerprint, Quantity, Variables
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

    def test_property_dt_item(self) -> None:
        fps = [
            Fingerprint.check(wd.inverse_property(wd.has_part)),
            -(wd.subproperty_of(wd.P(16))),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(wd.Brazil, fp, wd.South_America),  # VV
                     wd.part_of(wd.Brazil, wd.South_America)),
                ],
                contains=[
                    (Filter(wd.Brazil, fp), [  # VF
                        wd.part_of(wd.Brazil, wd.South_America),
                        wd.part_of(wd.Brazil, wd.Latin_America),
                    ]),
                    (Filter(None, fp, wd.South_America), [  # FV
                        wd.part_of(wd.Argentina, wd.South_America),
                        wd.part_of(wd.Brazil, wd.South_America),
                    ]),
                ])

    def test_property_dt_property(self) -> None:
        fps = [
            Fingerprint.check(wd.Wikidata_item_of_this_property(wd.mass_)),
            -(wd.subproperty_of(wd.payload_mass)),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(wd.caffeine, fp, '194.08'@wd.dalton),  # VV
                     wd.mass(wd.caffeine, '194.08'@wd.dalton)),
                    (Filter(wd.caffeine, fp, Quantity('194.08')),
                     wd.mass(wd.caffeine, '194.08'@wd.dalton)),
                    (Filter(wd.caffeine, fp, None),  # VF
                     wd.mass(wd.caffeine, '194.08'@wd.dalton)),
                ],
                contains=[
                    (Filter(None, fp, '194.08'@wd.dalton), [  # FV
                        (wd.mass(wd.caffeine, '194.08'@wd.dalton)),
                    ]),
                ])

    def test_property_dt_lexeme(self) -> None:
        pass

    def test_property_dt_iri(self) -> None:
        pass

    def test_property_dt_text(self) -> None:
        pass

    def test_property_dt_string(self) -> None:
        pass

    def test_property_dt_external_id(self) -> None:
        pass

    def test_property_dt_quantity(self) -> None:
        pass

    def test_property_dt_time(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
