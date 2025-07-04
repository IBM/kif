# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import db

from ....tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from ..test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_item(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(db.Alan_Turing, db.birthPlace),
           {db.birthPlace(db.Alan_Turing, db.Maida_Vale)})

    def test_property(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
