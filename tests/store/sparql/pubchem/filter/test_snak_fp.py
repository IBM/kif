# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Fingerprint, Variables
from kif_lib.vocabulary import pc, wd

from .....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    # -- pseudo-entries --

    def test_wd_instance_of_Wikidata_property_related_to_chemistry(
            self
    ) -> None:
        fp = wd.instance_of(wd.Wikidata_property_related_to_chemistry)
        self._test_filter(
            equals=[
                (Filter(fp),
                 wd.instance_of(
                     pc.Isotope_Atom_Count,
                     wd.Wikidata_property_related_to_chemistry)),
                (Filter(pc.CID(241), fp),
                 pc.Isotope_Atom_Count(pc.CID(241), 0)),
            ])

    # -- compound --

    def test_wd_canonical_SMILES(self) -> None:
        fp = wd.canonical_SMILES('C(CCC(=O)O)CC(CCS)S')
        self._test_filter(
            equals=[
                (Filter(fp, wd.PubChem_CID, '421'),
                 wd.PubChem_CID(pc.CID(421), '421')),
                (Filter(pc.CID(161714267), wd.has_part, fp),
                 wd.has_part(pc.CID(161714267), pc.CID('421'))),
            ])

    def test_wd_CAS_Registry_Number(self) -> None:
        fp = wd.CAS_Registry_Number('462-20-4')
        self._test_filter(
            equals=[
                (Filter(fp, wd.ChEBI_ID, '18047'),
                 wd.ChEBI_ID(pc.CID(421), '18047')),
                (Filter(pc.CID(9834298), wd.stereoisomer_of, fp),
                 wd.stereoisomer_of(pc.CID(9834298), pc.CID(421)))
            ])

    def test_wd_ChEBI_ID(self) -> None:
        fp = wd.ChEBI_ID('18047')
        self._test_filter(
            equals=[
                (Filter(fp, wd.PubChem_CID, '421'),
                 wd.PubChem_CID(pc.CID(421), '421')),
                (Filter(pc.CID(449141), wd.stereoisomer_of, fp),
                 wd.stereoisomer_of(pc.CID(449141), pc.CID(421))),
            ])

    def test_wd_ChEMBL_ID(self) -> None:
        fp = wd.ChEMBL_ID('CHEMBL277500')
        self._test_filter(
            equals=[
                (Filter(fp, wd.PubChem_CID, '241'),
                 wd.PubChem_CID(pc.CID(241), '241')),
                (Filter(pc.CID(21297776), wd.has_part, fp),
                 wd.has_part(pc.CID(21297776), pc.CID(241))),
            ])

    def test_wd_said_to_be_the_same_as(self) -> None:
        fp = wd.said_to_be_the_same_as(wd.benzene)
        self._test_filter(
            equals=[
                (Filter(fp, wd.mass, 78.11@wd.gram_per_mole),
                 wd.mass(pc.CID(241), 78.11@wd.gram_per_mole)),
                (Filter(pc.CID(21297776), wd.has_part, fp),
                 wd.has_part(pc.CID(21297776), pc.CID(241))),
            ])

    def test_wd_has_part(self) -> None:
        fp = wd.has_part(pc.CID(421))
        self._test_filter(
            equals=[
                (Filter(fp, wd.PubChem_CID, '161714267'),
                 wd.PubChem_CID(pc.CID(161714267), '161714267')),
                (Filter(pc.patent('US-6897305-B2'), wd.main_subject, fp),
                 wd.main_subject(
                     pc.patent('US-6897305-B2'),
                     pc.CID(160094235))),
            ])

    def test_wd_part_of(self) -> None:
        fp = wd.part_of(pc.CID('161714267'))
        self._test_filter(
            equals=[
                (Filter(fp, wd.PubChem_CID, '421'),
                 wd.PubChem_CID(pc.CID(421), '421')),
            ],
            contains=[
                (Filter(pc.source('ID25790'), wd.material_produced, fp), [
                    wd.material_produced(pc.source('ID25790'), pc.CID(10902)),
                    wd.material_produced(pc.source('ID25790'), pc.CID(297)),
                ]),
            ])

    def test_wd_InChI(self) -> None:
        fp = wd.InChI('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H')
        self._test_filter(
            equals=[
                (Filter(fp, wd.PubChem_CID, '241'),
                 wd.PubChem_CID(pc.CID(241), '241')),
                (Filter(pc.CID(21297776), wd.has_part, fp),
                 wd.has_part(pc.CID(21297776), pc.CID(241))),
            ])

    def test_wd_InChIKey(self) -> None:
        fp = wd.InChIKey('IZFHEQBZOYJLPK-UHFFFAOYSA-N')
        self._test_filter(
            equals=[
                (Filter(fp, wd.PubChem_CID, '421'),
                 wd.PubChem_CID(pc.CID(421), '421')),
                (Filter(pc.source('ID15294'), wd.material_produced, fp),
                 wd.material_produced(pc.source('ID15294'), pc.CID(421))),
            ])

    def test_wd_instance_of_type_of_a_chemical_entity(self) -> None:
        pass

    def test_pc_Isotope_Atom_Count(self) -> None:
        pass

    def test_wd_isomeric_SMILES(self) -> None:
        pass

    def test_wd_legal_status_medicine(self) -> None:
        pass

    def test_wd_mass(self) -> None:
        pass

    def test_wd_manufacturer(self) -> None:
        pass

    def test_wd_partition_coefficient_water_octanol(self) -> None:
        pass

    def test_wd_PubChem_CID(self) -> None:
        pass

    def test_wd_stereoisomer_of(self) -> None:
        fps = [
            Fingerprint.check(wd.stereoisomer_of(pc.CID(449141))),
            -(wd.stereoisomer_of(pc.CID(449141))),
        ]
        for fp in fps:
            self._test_filter(
                contains=[
                    (Filter(fp, wd.ChEBI_ID), [
                        wd.ChEBI_ID(pc.CID(421), '18047'),
                        wd.ChEBI_ID(pc.CID(9834298), '45230'),
                    ]),
                ])

    # def test_item_compound(self) -> None:
    #     fps = [
    #         Fingerprint.check(wd.ChEMBL_ID('CHEMBL277500')),
    #         -(wd.has_part(pc.CID(139250634))),
    #     ]
    #     for fp in fps:
    #         self._test_filter(
    #             equals=[
    #                 (Filter(    # VV
    #                     fp, wd.PubChem_CID, '241'),
    #                  wd.PubChem_CID(pc.CID(241), '241')),
    #                 (Filter(    # FV
    #                     fp, None, ExternalId('16716')),
    #                  wd.ChEBI_ID(pc.CID(241), '16716')),
    #             ],
    #             contains=[
    #                 (Filter(    # VF
    #                     fp, wd.mass, None), [
    #                     wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole),
    #                 ]),
    #             ])

    # -- patent --

    def test_wd_author_name_string(self) -> None:
        pass

    def test_wd_instance_of_patent(self) -> None:
        pass

    def test_wd_main_subject(self) -> None:
        pass

    def test_wd_patent_number(self) -> None:
        pass

    def test_wd_publication_date(self) -> None:
        pass

    def test_wd_title(self) -> None:
        pass

    # def test_item_patent(self) -> None:
    #     fps = [
    #         Fingerprint.check(wd.patent_number('BR-PI0506496-B1')),
    #         Fingerprint.check(wd.title(
    #             'Improved injection site tolerance pharmaceutical '
    #             'composition comprising sulfobutylether-ß-cyclodextrin '
    #             'and its use in the treatment of emesisEmproved '
    #             'injection site tolerance pharmaceutical composition '
    #             'comprising sulfobutylether-ß-cyclodextrin and its '
    #             'use in the treatment of emesisEmproved tolerance '
    #             'pharmaceutical composition injection comprising '
    #             'sulfobutylether-ß-cyclodextrin and its use in the '
    #             'treatment of emesis')),
    #     ]
    #     for fp in fps:
    #         self._test_filter(
    #             equals=[
    #                 (Filter(    # VV
    #                     fp, wd.patent_number, 'BR-PI0506496-B1'),
    #                  wd.patent_number(
    #                      pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
    #                 (Filter(    # VF
    #                     fp, wd.patent_number, None),
    #                  wd.patent_number(
    #                      pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
    #                 (Filter(    # FV
    #                     fp, None, ExternalId('BR-PI0506496-B1')),
    #                  wd.patent_number(
    #                      pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
    #             ])

    # -- source --

    def test_wd_instance_of_vendor(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
