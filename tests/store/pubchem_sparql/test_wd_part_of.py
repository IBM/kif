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
        a(True, F(pc.CID(19020919), wd.part_of))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(2, F(pc.CID(19020919), wd.part_of))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(pc.CID(19020919), wd.part_of),
           {wd.part_of(pc.CID(19020919), pc.CID(19020918)),
            wd.part_of(pc.CID(19020919), pc.CID(22676441))})


if __name__ == '__main__':
    Test.main()
