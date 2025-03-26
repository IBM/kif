# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Store
from kif_lib.vocabulary import pc, wd

from ...tests import TestCase


class Test(TestCase):

    KB = Store(
        'pubchem-rdf',
        'tests/data/benzene-pubchem.ttl',
    )

    def test_empty(self) -> None:
        self.assertEqual(
            set(self.KB.filter(snak_mask=Filter.SnakMask(0))), set())

    def test_full(self) -> None:
        self.assertEqual(
            set(self.KB.filter()),
            {
                wd.instance_of(pc.CID(241), wd.type_of_a_chemical_entity),
                wd.instance_of(pc.Isotope_Atom_Count,
                               wd.Wikidata_property_related_to_chemistry),
                wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole),
            })


if __name__ == '__main__':
    Test.main()
