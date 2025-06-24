# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store, Time
from kif_lib.vocabulary import pc, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_ask(self) -> None:
        a, F = self.store_ask_assertion(self.KB())
        a(True, F(pc.patent('AR-033431-A1'), wd.publication_date))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(1, F(pc.patent('AR-033431-A1'), wd.publication_date))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(pc.patent('AR-033431-A1'), wd.publication_date),
           {wd.publication_date(
               pc.patent('AR-033431-A1'),
               Time('2003-12-17T04:00', 11, 0,
                    wd.proleptic_Gregorian_calendar))})


if __name__ == '__main__':
    Test.main()
