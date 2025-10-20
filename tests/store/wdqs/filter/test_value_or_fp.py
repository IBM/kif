# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Or, Store, Time
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
        f, F = self.store_filter_assertion(self.KB())
        s = wd.Brazil
        f(F(s, value=(
            Or(Time('1822-09-07'), Time('4003-01-01'), Time('1500-05-02')))),
            {wd.inception(s, Time(
                '1822-09-07', 11, 0, wd.proleptic_Gregorian_calendar)),
             wd.time_of_discovery_or_invention(s, Time(
                 '1500-05-02', 11, 0, wd.proleptic_Julian_calendar))})


if __name__ == '__main__':
    Test.main()
