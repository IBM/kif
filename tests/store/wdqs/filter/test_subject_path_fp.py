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
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F((wd.instance_of/wd.subclass_of)(
            wd.administrative_territorial_entity_of_Brazil),
             wd.inception, '1549-01-01'),
           {wd.inception(
               wd.Salvador,
               Time('1549-01-01', 9, 0, wd.proleptic_Julian_calendar),
               qualifiers=[wd.statement_is_subject_of(wd.Q(107575514))],
               references=[[
                   wd.imported_from_Wikimedia_project(wd.Q(206855))]])})

    def test_property(self) -> None:
        raise self.TODO()

    def test_lexeme(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
