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
        a(True, F(pc.CID(241), wd.description))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(2, F(pc.CID(241) | pc.patent('AR-033431-A1'), wd.description))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(
            pc.CID(241) | pc.patent('AR-033431-A1'),
            wd.description),
           {wd.description(
               pc.CID(241),
               'A six-carbon aromatic annulene in which each carbon '
               'atom donates one of its two 2p electrons into a delocalised '
               'pi system. A toxic, flammable liquid byproduct of coal '
               'distillation, it is used as an industrial solvent. '
               'Benzene is a carcinogen that also damages bone marrow '
               'and the central nervous system.'),
            wd.description(
                pc.patent('AR-033431-A1'),
                'A pharmaceutical masked flavor composition comprising a '
                'microcapsule wherein the microcapsule comprises a '
                'pharmaceutically active agent core coated with an '
                'effective taste masking amount of an enteric water '
                'insoluble coating where the coating comprises a weakly '
                'acidic methacrylic acid-ethyl acrylate copolymer .')})


if __name__ == '__main__':
    Test.main()
