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
        a(True, F(pc.CID(241), wd.said_to_be_the_same_as))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(2, F(pc.CID(241), wd.said_to_be_the_same_as))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(pc.CID(241), wd.said_to_be_the_same_as),
           {wd.said_to_be_the_same_as(pc.CID(241), wd.benzene),
            wd.said_to_be_the_same_as(pc.CID(241), wd.Q(26841227))})


if __name__ == '__main__':
    Test.main()
