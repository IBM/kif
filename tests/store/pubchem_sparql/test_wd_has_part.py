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
        a(True, F(pc.CID(19020918), wd.has_part))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(3, F(pc.CID(19020918), wd.has_part))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(pc.CID(19020918), wd.has_part),
           {wd.has_part(pc.CID(19020918), pc.CID(19020919)),
            wd.has_part(pc.CID(19020918), pc.CID(23986)),
            wd.has_part(pc.CID(19020918), pc.CID(241))})


if __name__ == '__main__':
    Test.main()
