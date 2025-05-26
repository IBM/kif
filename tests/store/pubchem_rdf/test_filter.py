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
            'tests/data/benzene-pubchem.ttl')

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    def test_full(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(),
            {wd.instance_of(pc.CID(241), wd.type_of_a_chemical_entity),
             wd.instance_of(pc.isotope_atom_count,
                            wd.Wikidata_property_related_to_chemistry),
             wd.label(pc.isotope_atom_count, 'isotope atom count'),
             wd.instance_of(pc.IUPAC_name,
                            wd.Wikidata_property_related_to_chemistry),
             wd.label(pc.IUPAC_name, 'IUPAC name'),
             wd.mass(pc.CID(241), '78.047'@wd.dalton)})


if __name__ == '__main__':
    Test.main()
