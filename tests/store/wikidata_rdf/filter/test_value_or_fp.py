# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store, Time
from kif_lib.vocabulary import wd

from ....tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from ..test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_item(self) -> None:
        raise self.TODO()

    def test_property(self) -> None:
        raise self.TODO()

    def test_lexeme(self) -> None:
        raise self.TODO()

    def test_time(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(value=Time('1822-09-07')|Time('4003-01-01')),
           {})


if __name__ == '__main__':
    Test.main()
