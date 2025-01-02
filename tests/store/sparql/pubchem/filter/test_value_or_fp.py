# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Quantity, Variables
from kif_lib.vocabulary import pc, wd

from .....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    def test_item_compound(self) -> None:
        self._test_filter(
            equals=[
                (Filter(         # VV
                    pc.CID(340032), wd.has_part, pc.CID(241) | pc.CID(421)),
                 wd.has_part(pc.CID(340032), pc.CID(241))),
                (Filter(         # VF
                    pc.CID(340032), None, pc.CID(241) | pc.CID(421)
                    | pc.patent('BR-PI0506496-B1')),
                 wd.has_part(pc.CID(340032), pc.CID(241))),
            ],
            contains=[
                (Filter(        # FV
                    None, wd.has_part, pc.CID(2441) | pc.CID(421)), [
                        wd.has_part(pc.CID(159215079), pc.CID(2441)),
                        wd.has_part(pc.CID(138400403), pc.CID(2441)),
                        wd.has_part(pc.CID(161714267), pc.CID(421)),
                        wd.has_part(pc.CID(161353624), pc.CID(421)),
                ]),
            ])

    def test_quantity(self) -> None:
        self._test_filter(
            equals=[
                (Filter(        # VV
                    pc.CID(57497247), wd.mass,
                    '208.81'@wd.gram_per_mole | '208.82'@wd.gram_per_mole),
                 wd.mass(pc.CID(57497247), '208.81'@wd.gram_per_mole)),
                (Filter(        # VF
                    pc.CID(57497247), None,
                    Quantity('208.81') | '208.82'@wd.gram_per_mole),
                 wd.mass(pc.CID(57497247), '208.81'@wd.gram_per_mole)),
            ],
            contains=[
                (Filter(        # FV
                    None, wd.mass, Quantity('208.81')
                    | '208.82'@wd.gram_per_mole | '208.81'@wd.kilogram), [
                        wd.mass(pc.CID(57497247), '208.81'@wd.gram_per_mole),
                        wd.mass(pc.CID(102500770), '208.82'@wd.gram_per_mole)
                ]),
            ])


if __name__ == '__main__':
    Test.main()
