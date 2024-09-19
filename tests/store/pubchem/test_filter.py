# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Filter, Quantity, String
from kif_lib.vocabulary import pc, wd

from ...tests import PubChemStoreTestCase


class Test(PubChemStoreTestCase):

    def test_Exx(self) -> None:
        kb = self.new_Store()
        self.assert_it_empty(kb.filter(Quantity(0)))

    def test_xEx(self) -> None:
        kb = self.new_Store()
        self.assert_it_empty(kb.filter(None, Quantity(0)))

    def test_xxE(self) -> None:
        kb = self.new_Store()
        self.assert_it_empty(kb.filter(
            None, None, Quantity(0), snak_mask=Filter.SOME_VALUE_SNAK))

    def test_FFF(self) -> None:
        kb = self.new_Store()
        stmt = next(kb.filter())
        self.assert_statement(stmt, *stmt)

    def test_compound_FF(self) -> None:
        kb = self.new_Store()
        it = kb.filter(pc.CID(241))
        self.assert_it_contains(
            it,
            pc.Isotope_Atom_Count(pc.CID(241), 0),
            wd.canonical_SMILES(pc.CID(241), 'C1=CC=CC=C1'),
            wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole),
            wd.PubChem_CID(pc.CID(241), '241'))

    def test_V_canonical_SMILES_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, wd.canonical_SMILES))
        self.assert_it_empty(
            kb.filter(pc.Isotope_Atom_Count, wd.canonical_SMILES))
        # success
        it = kb.filter(pc.CID(241), wd.canonical_SMILES)
        self.assert_it_equal(
            it, wd.canonical_SMILES(pc.CID(241), 'C1=CC=CC=C1'))

    def test_V_has_part_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, wd.has_part))
        self.assert_it_empty(kb.filter(pc.Isotope_Atom_Count, wd.has_part))
        # success
        it = kb.filter(pc.CID(241), wd.has_part)
        self.assert_it_empty(it)
        it = kb.filter(pc.CID(340032), wd.has_part)
        self.assert_it_equal(it, wd.has_part(pc.CID(340032), pc.CID(241)))

    def test_V_instance_of_F(self) -> None:
        kb = self.new_Store()
        # success
        self.assert_it_empty(kb.filter(wd.benzene, wd.instance_of))
        self.assert_it_empty(kb.filter(pc.CID(421), wd.instance_of))
        # failure
        it = kb.filter(pc.Isotope_Atom_Count, wd.instance_of)
        self.assert_it_equal(it, wd.instance_of(
            pc.Isotope_Atom_Count, wd.Wikidata_property_related_to_chemistry))

    def test_V_Isotope_Atom_Count_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, pc.Isotope_Atom_Count))
        # success
        it = kb.filter(pc.CID(241), pc.Isotope_Atom_Count)
        self.assert_it_equal(it, pc.Isotope_Atom_Count(pc.CID(241), 0))

    def test_F_Isotope_Atom_Count_V(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(
            kb.filter(None, pc.Isotope_Atom_Count, 201@wd.kilogram))
        # success
        it = kb.filter(snak=pc.Isotope_Atom_Count(201))
        self.assert_it_contains(
            it, pc.Isotope_Atom_Count(pc.CID(160456303), 201))

    def test_V_mass_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, wd.mass))
        self.assert_it_empty(kb.filter(pc.Isotope_Atom_Count, wd.mass))
        # success
        it = kb.filter(pc.CID(241), wd.mass)
        self.assert_it_equal(
            it, wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole))

    def test_F_mass_V(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity('78.11', wd.kilogram)))
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity('78.11', wd.gram_per_mole, 1)))
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity(
                '78.11', wd.gram_per_mole, None, 80)))
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity(10**8, wd.gram_per_mole)))
        # success
        it = kb.filter(None, wd.mass, Quantity('78.11', wd.gram_per_mole))
        self.assert_it_contains(
            it, wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole))

    def test_V_PubChem_CID_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, wd.PubChem_CID))
        self.assert_it_empty(kb.filter(pc.Isotope_Atom_Count, wd.PubChem_CID))
        # success
        it = kb.filter(pc.CID(241), wd.PubChem_CID)
        self.assert_it_equal(it, wd.PubChem_CID(pc.CID(241), '241'))

    def test_F_PubChem_CID_V(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(None, wd.PubChem_CID, String('241')))
        self.assert_it_empty(
            kb.filter(None, wd.PubChem_CID, ExternalId('abc')))
        # success
        it = kb.filter(None, wd.PubChem_CID, ExternalId('241'))
        self.assert_it_equal(it, wd.PubChem_CID(pc.CID(241), '241'))


if __name__ == '__main__':
    Test.main()
