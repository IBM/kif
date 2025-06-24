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
        a(True, F(pc.CID(241), wd.alias))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(17, F(pc.CID(241) | pc.source('ID11777'), wd.alias))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(
            pc.CID(241) | pc.source('ID11777'),
            wd.alias),
           {wd.alias(pc.CID(241), '[6]annulene'),
            wd.alias(pc.CID(241), 'Benzen'),
            wd.alias(pc.CID(241), 'benzene'),
            wd.alias(pc.CID(241), 'Benzene'),
            wd.alias(pc.CID(241), 'BENZENE'),
            wd.alias(pc.CID(241), 'Benzine'),
            wd.alias(pc.CID(241), 'Benzol'),
            wd.alias(pc.CID(241), 'benzole'),
            wd.alias(pc.CID(241), 'Bicarburet of hydrogen'),
            wd.alias(pc.CID(241), 'Coal naphtha'),
            wd.alias(pc.CID(241), 'cyclohexatriene'),
            wd.alias(pc.CID(241), 'Mineral naphtha'),
            wd.alias(pc.CID(241), 'Phene'),
            wd.alias(pc.CID(241), 'phenyl hydride'),
            wd.alias(pc.CID(241), 'Pyrobenzol'),
            wd.alias(pc.CID(241), 'Pyrobenzole'),
            wd.alias(pc.source('ID11777'), 'Bic Biotech')})


if __name__ == '__main__':
    Test.main()
