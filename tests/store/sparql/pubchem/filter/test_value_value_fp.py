# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Quantity, Variables
from kif_lib.vocabulary import pc, wd

from .....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    def test_quantity(self) -> None:
        self._test_filter(
            empty=[
                Filter(pc.CID(57497247), wd.mass, Quantity('208.82')),
                Filter(pc.CID(57497247), wd.mass, Quantity(
                    '208.81', wd.kilogram)),
                Filter(pc.CID(57497247), wd.mass, Quantity(
                    '208.81', None, '208.8')),
                Filter(pc.CID(57497247), wd.mass, Quantity(
                    '208.81', None, None, '208.9')),
            ],
            equals=[
                (Filter(        # VV
                    pc.CID(57497247), wd.mass, '208.81'@wd.gram_per_mole),
                 wd.mass(pc.CID(57497247), '208.81'@wd.gram_per_mole)),
                (Filter(
                    pc.CID(57497247), wd.mass, Quantity('208.81')),
                 wd.mass(pc.CID(57497247), '208.81'@wd.gram_per_mole)),
            ])


if __name__ == '__main__':
    Test.main()
