# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Quantity, Store, Statement
from kif_lib.vocabulary import wd
from kif_lib.typing import Iterable, Iterator

from ...tests import kif_StoreTestCase


class Test(kif_StoreTestCase):

    def assert_filter_contains(
        self,
        it: Iterable[Statement],
        *stmts: Statement
    ):
        it_set = set(it)
        for stmt in stmts:
            self.assertTrue(stmt in it_set, f'{stmt} not in it_set')

    def test_filter(self):
        kb = Store('wikidata')
        # subject
        self.assert_filter_contains(
            kb.filter(wd.Monte_Pascoal),
            wd.instance_of(wd.Monte_Pascoal, wd.mountain),
            wd.named_after(wd.Monte_Pascoal, wd.Easter),
            wd.continent(wd.Monte_Pascoal, wd.Americas),
            wd.elevation_above_sea_level(
                wd.Monte_Pascoal, Quantity(536, wd.metre)))


if __name__ == '__main__':
    Test.main()
