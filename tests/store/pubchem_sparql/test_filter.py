# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Entity
from kif_lib.vocabulary import pc, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        import os
        pubchem = os.getenv('PUBCHEM')
        if not pubchem:
            raise cls.SKIP('PUBCHEM is not set')
        else:
            return cls.S('pubchem-sparql', pubchem)

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    # -- masks --

    def test_snak_mask(self) -> None:
        raise self.TODO()

    def test_subject_mask(self) -> None:
        raise self.TODO()

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        raise self.TODO()

    def test_language(self) -> None:
        raise self.TODO()

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        f, F = self.store_filter_assertion(self.KB())
        # pc.isotope_atom_count
        s: Entity = pc.isotope_atom_count
        f(F(subject=s, annotated=True),
          {wd.instance_of(s, wd.Wikidata_property_related_to_chemistry),
           wd.label(s, 'isotope atom count')})
        # pc.IUPAC_name
        s = pc.IUPAC_name
        f(F(subject=s, annotated=True),
          {wd.instance_of(s, wd.Wikidata_property_related_to_chemistry),
           wd.label(s, 'IUPAC name')})
        # compound
        s = pc.CID(12196274)
        f(F(subject=s, annotated=True),
          {pc.isotope_atom_count(s, 4),
           wd.canonical_SMILES(s, 'C1=CC=CC=C1'),
           wd.chemical_formula(s, 'C6H6'),
           wd.described_by_source(s, pc.patent('BR-PI0720756-A2')),
           wd.described_by_source(s, pc.patent('CN-104250332-B')),
           wd.described_by_source(s, pc.patent('CN-104640922-B')),
           wd.described_by_source(s, pc.patent('KR-101892162-B1')),
           wd.described_by_source(s, pc.patent('KR-102002435-B1')),
           wd.described_by_source(s, pc.patent('KR-102190777-B1')),
           wd.described_by_source(s, pc.patent('KR-20020080584-A')),
           wd.described_by_source(s, pc.patent('KR-20130064734-A')),
           wd.described_by_source(s, pc.patent('KR-20180097772-A')),
           wd.described_by_source(s, pc.patent('KR-20190087649-A')),
           wd.described_by_source(s, pc.patent('TW-201211136-A')),
           wd.described_by_source(s, pc.patent('US-11411182-B1')),
           wd.described_by_source(s, pc.patent('US-2012073956-A1')),
           wd.described_by_source(s, pc.patent('US-8481002-B2')),
           wd.described_by_source(s, pc.patent('WO-2022244864-A1')),
           wd.described_by_source(s, pc.patent('WO-2022270423-A1')),
           wd.described_by_source(s, pc.patent('WO-2022270428-A1')),
           wd.described_by_source(s, pc.patent('WO-2022270430-A1')),
           wd.InChI(s, 'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H/i1D,2D,3D,4D'),
           wd.InChIKey(s, 'UHOVQNZJYSORNB-RHQRLBAQSA-N'),
           wd.instance_of(s, wd.type_of_a_chemical_entity),
           wd.isomeric_SMILES(s, '[2H]C1=CC=C(C(=C1[2H])[2H])[2H]'),
           wd.mass(s, '82.14'@wd.gram_per_mole),
           wd.part_of(s, pc.CID(139250633)),
           wd.partition_coefficient_water_octanol(s, '2.1'),
           wd.PubChem_CID(s, '12196274')})


if __name__ == '__main__':
    Test.main()
