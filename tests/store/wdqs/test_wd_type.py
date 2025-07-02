# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_ask(self) -> None:
        a, F = self.store_ask_assertion(self.KB())
        a(True, F(wd.Brazil, wd.type, wd.state))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(4, F(wd.Brazil, wd.instance_of))
        c(69, F(wd.Brazil, wd.type))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(wd.Brazil, wd.type, wd.subtype(wd.state)),
           {wd.type(wd.Brazil, wd.seculararchy),
            wd.type(wd.Brazil, wd.sovereign_state)})


if __name__ == '__main__':
    Test.main()
