# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Item, Store
from kif_lib.vocabulary import db, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_ask(self) -> None:
        a, F = self.store_ask_assertion(self.KB())
        a(True, F(db.r('Alan_Turing'), wd.label))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(3, F(
            db.op('almaMater')
            | db.op('doctoralAdvisor').replace(range=Item)
            | db.r('Alan_Turing'), wd.label, language='en'))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(
            db.op('almaMater')
            | db.op('doctoralAdvisor').replace(range=Item)
            | db.r('Alan_Turing'), wd.label, language='en'),
           {wd.label(db.op('almaMater'), 'alma mater'),
            wd.label(db.op('doctoralAdvisor').replace(range=Item),
                     'doctoral advisor'),
            wd.label(db.r('Alan_Turing'), 'Alan Turing')})


if __name__ == '__main__':
    Test.main()
