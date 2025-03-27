# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.vocabulary import pc, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        return cls.S(
            'pubchem-rdf',
            'tests/data/benzene-pubchem.ttl',
        )

    def test_empty(self) -> None:
        xf, F = self.xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    def test_full(self) -> None:
        xf, F = self.xfilter_assertion(self.KB())
        xf(F(),
            {wd.instance_of(pc.CID(241), wd.type_of_a_chemical_entity),
             wd.instance_of(pc.Isotope_Atom_Count,
                            wd.Wikidata_property_related_to_chemistry),
             wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole)})


if __name__ == '__main__':
    Test.main()
