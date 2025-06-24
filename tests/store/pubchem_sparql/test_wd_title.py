# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import pc, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_ask(self) -> None:
        a, F = self.store_ask_assertion(self.KB())
        a(True, F(pc.patent('AR-033431-A1'), wd.title))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(1, F(pc.patent('AR-033431-A1'), wd.title))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(pc.patent('AR-033431-A1'), wd.title),
           {wd.title(
               pc.patent('AR-033431-A1'),
               'PHARMACEUTICAL COMPOSITIONS OF MASKED FLAVOR.')})


if __name__ == '__main__':
    Test.main()
