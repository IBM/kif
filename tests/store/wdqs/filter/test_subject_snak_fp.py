# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
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
        xf(F(wd.publication_date('1998-01-01')
             & wd.main_subject(wd.flying_saucer),
             wd.genre, wd.drama_film),
           {wd.genre(wd.Q(1129381), wd.drama_film)})


if __name__ == '__main__':
    Test.main()
