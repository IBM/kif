# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Time, Variables
from kif_lib.vocabulary import pc, wd

from .....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    def test_item_compound(self) -> None:
        canonical_SMILES = (
            'CN1CCC2=CC(=C3C=C2C1CC4=CC=C(C=C4)O'
            'C5=C(C=CC(=C5)CC6C7=C(O3)C(=C(C=C7CCN6C)OC)OC)O)OC.C1=CC=CC=C1'
        )
        InChI = (
            'InChI=1S/C37H40N2O6.C6H6/c1-38-14-12-24-19-32(41-3)33-21-27'
            '(24)28(38)16-22-6-9-26(10-7-22)44-31-18-23(8-11-30(31)40)17'
            '-29-35-25(13-15-39(29)2)20-34(42-4)36(43-5)37(35)45-33;1-2-'
            '4-6-5-3-1/h6-11,18-21,28-29,40H,12-17H2,1-5H3;1-6H/t28-,29+;'
            '/m0./s1'
        )
        isomeric_SMILES = (
            'CN1CCC2=CC(=C3C=C2[C@@H]1CC4=CC=C(C=C4)OC5=C'
            '(C=CC(=C5)C[C@@H]6C7=C(O3)C(=C(C=C7CCN6C)OC)OC)O)OC.C1=CC=CC=C1'
        )
        self._test_filter_with_fixed_subject(
            subject=pc.CID(340032),
            equals=[            # VV
                ((wd.canonical_SMILES, canonical_SMILES),
                 wd.canonical_SMILES(canonical_SMILES)),
                ((wd.ChEMBL_ID, 'CHEMBL1995935'),
                 wd.ChEMBL_ID('CHEMBL1995935')),
                ((wd.has_part, pc.CID(241)),
                 wd.has_part(pc.CID(241))),
                ((wd.InChI, InChI),
                 wd.InChI(InChI)),
                ((wd.InChIKey, 'BCRANABGBDJPMM-QBYKQQEBSA-N'),
                 wd.InChIKey('BCRANABGBDJPMM-QBYKQQEBSA-N')),
                ((wd.isomeric_SMILES, isomeric_SMILES),
                 wd.isomeric_SMILES(isomeric_SMILES)),
                ((wd.instance_of, wd.type_of_a_chemical_entity),
                 wd.instance_of(wd.type_of_a_chemical_entity)),
                ((pc.Isotope_Atom_Count, 0),
                 pc.Isotope_Atom_Count(0)),
                ((wd.manufacturer, pc.source('ID708')),
                 wd.manufacturer(pc.source('ID708'))),
                ((wd.mass, '686.8'@wd.gram_per_mole),
                 wd.mass('686.8'@wd.gram_per_mole)),
                ((wd.PubChem_CID, '340032'),
                 wd.PubChem_CID('340032')),
                ((wd.stereoisomer_of, pc.CID(498213)),
                 wd.stereoisomer_of(pc.CID(498213))),
            ],
            contains=[
                ((None, None), [  # FF
                    wd.canonical_SMILES(canonical_SMILES),
                    wd.ChEMBL_ID('CHEMBL1995935'),
                    wd.has_part(pc.CID(241)),
                    wd.InChI(InChI),
                    wd.InChIKey('BCRANABGBDJPMM-QBYKQQEBSA-N'),
                    wd.isomeric_SMILES(isomeric_SMILES),
                    wd.instance_of(wd.type_of_a_chemical_entity),
                    pc.Isotope_Atom_Count(0),
                    wd.manufacturer(pc.source('ID708')),
                    wd.mass('686.8'@wd.gram_per_mole),
                    wd.PubChem_CID('340032'),
                    wd.stereoisomer_of(pc.CID(498213)),
                ]),
            ])

    def test_item_patent(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.patent('BR-PI0506496-B1'),
            equals=[            # VV
                ((wd.patent_number, 'BR-PI0506496-B1'),
                 wd.patent_number('BR-PI0506496-B1')),
                ((wd.publication_date, None),
                 (wd.publication_date(Time(
                     '2018-10-09+04:00', 11, 0,
                     wd.proleptic_Gregorian_calendar)))),
            ],
            contains=[
                ((None, None), [
                    wd.author_name_string('JULIA ANN WOOD'),
                    wd.author_name_string('ROGER CHRISTOPHER ADAMI'),
                    wd.author_name_string('FREDERICK DAVID'),
                    wd.instance_of(wd.patent),
                    wd.main_subject(pc.CID(7314)),
                    wd.main_subject(pc.CID(6405)),
                    wd.patent_number('BR-PI0506496-B1'),
                    wd.publication_date(
                        Time('2018-10-09+04:00', 11, 0,
                             wd.proleptic_Gregorian_calendar)),
                    wd.title(
                        'Improved injection site tolerance pharmaceutical '
                        'composition comprising '
                        'sulfobutylether-ß-cyclodextrin '
                        'and its use in the treatment of emesisEmproved '
                        'injection site tolerance pharmaceutical composition '
                        'comprising sulfobutylether-ß-cyclodextrin and its '
                        'use in the treatment of emesisEmproved tolerance '
                        'pharmaceutical composition injection comprising '
                        'sulfobutylether-ß-cyclodextrin and its use in the '
                        'treatment of emesis'),
                ]),
            ])

    def test_item_source(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.source('ID25235'),
            equals=[            # VV
                ((wd.instance_of, wd.vendor),
                 wd.instance_of(wd.vendor)),
                ((wd.product_or_material_produced_or_service_provided,
                  pc.CID(23654840)),
                 wd.product_or_material_produced_or_service_provided(
                     pc.CID(23654840))),
                ((wd.product_or_material_produced_or_service_provided,
                  pc.CID(162394048)),
                 wd.product_or_material_produced_or_service_provided(
                     pc.CID(162394048))),
            ],
            contains=[
                ((None, None), [  # FF
                    wd.instance_of(wd.vendor),
                    wd.product_or_material_produced_or_service_provided(
                        pc.CID(6400537)),
                    wd.product_or_material_produced_or_service_provided(
                        pc.CID(23654840)),
                    wd.product_or_material_produced_or_service_provided(
                        pc.CID(162394048)),
                ]),
            ])

    def test_property_Isotope_Atom_Count(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.Isotope_Atom_Count,
            equals=[
                ((None, None),  # FF
                 wd.instance_of(wd.Wikidata_property_related_to_chemistry)),
            ])


if __name__ == '__main__':
    Test.main()
