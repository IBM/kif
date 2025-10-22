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
        a(True, F(pc.CID(241), wd.label))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(4, F(pc.isotope_atom_count | pc.CID(241), wd.label))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(
            pc.CID(241)
            | pc.isotope_atom_count
            | pc.IUPAC_name
            | pc.patent('AR-033431-A1')
            | pc.source('ID25790'),
            wd.label),
           {wd.label(pc.CID(241), 'benzene'),
            wd.label(pc.CID(241), '[6]annulene'),
            wd.label(pc.isotope_atom_count, 'isotope atom count'),
            wd.label(pc.IUPAC_name, 'IUPAC name'),
            wd.label(
                pc.patent('AR-033431-A1'),
                'PHARMACEUTICAL COMPOSITIONS OF MASKED FLAVOR.'),
            wd.label(pc.source('ID25790'), '25790')})


if __name__ == '__main__':
    Test.main()
