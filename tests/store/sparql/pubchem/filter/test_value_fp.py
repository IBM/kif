# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Quantity, String, Text, Time, Variables
from kif_lib.vocabulary import pc, wd

from .....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    # -- pseudo-entries --

    def test_wd_instance_of_Wikidata_property_related_to_chemistry(
            self
    ) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.Isotope_Atom_Count,
            equals=[
                ((wd.instance_of,
                  wd.Wikidata_property_related_to_chemistry),  # VV
                 wd.instance_of(wd.Wikidata_property_related_to_chemistry)),
                ((wd.instance_of, None),  # VF
                 wd.instance_of(wd.Wikidata_property_related_to_chemistry)),
                ((None, wd.Wikidata_property_related_to_chemistry),  # FV
                 wd.instance_of(wd.Wikidata_property_related_to_chemistry)),
            ])
        self._test_filter_with_fixed_value(
            value=wd.Wikidata_property_related_to_chemistry,
            equals=[
                ((pc.Isotope_Atom_Count, wd.instance_of),  # VV
                 (pc.Isotope_Atom_Count, wd.instance_of)),
                ((pc.Isotope_Atom_Count, None),  # VF
                 (pc.Isotope_Atom_Count, wd.instance_of)),
                ((None, wd.instance_of),  # FV
                 (pc.Isotope_Atom_Count, wd.instance_of)),
            ])

    # -- compound --

    def test_wd_canonical_SMILES(self) -> None:
        smiles = String('C(CCC(=O)O)CC(CCS)S')
        self._test_filter_with_fixed_subject(
            subject=pc.CID(421),
            equals=[
                ((wd.canonical_SMILES, smiles),  # VV
                 wd.canonical_SMILES(smiles)),
                ((wd.canonical_SMILES, None),  # VF
                 wd.canonical_SMILES(smiles)),
            ],
            contains=[
                ((None, smiles), [  # FV
                    wd.canonical_SMILES(smiles),
                    wd.isomeric_SMILES(smiles),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=String('C(CCC(=O)O)CC(CCS)S'),
            equals=[
                ((pc.CID(421), wd.canonical_SMILES),  # VV
                 (pc.CID(421), wd.canonical_SMILES)),
            ],
            contains=[
                ((pc.CID(421), None), [  # VF
                    (pc.CID(421), wd.canonical_SMILES),
                    (pc.CID(421), wd.isomeric_SMILES),
                ]),
                ((None, wd.canonical_SMILES), [  # FV
                    (pc.CID(421), wd.canonical_SMILES),
                    (pc.CID(449141), wd.canonical_SMILES),
                    (pc.CID(9834298), wd.canonical_SMILES),
                ]),
            ])

    def test_wd_CAS_Registry_Number(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.CAS_Registry_Number, ExternalId('26181-88-4')),  # VV
                 wd.CAS_Registry_Number(ExternalId('26181-88-4'))),
                ((None, ExternalId('26181-88-4')),  # FV
                 wd.CAS_Registry_Number(ExternalId('26181-88-4'))),
            ],
            contains=[
                ((wd.CAS_Registry_Number, None), [  # VF
                    wd.CAS_Registry_Number(ExternalId('2396-01-2')),
                    wd.CAS_Registry_Number(ExternalId('26181-88-4')),
                    wd.CAS_Registry_Number(ExternalId('54682-86-9')),
                    wd.CAS_Registry_Number(ExternalId('71-43-2')),
                    wd.CAS_Registry_Number(ExternalId('cas-71-43-2')),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=ExternalId('26181-88-4'),
            equals=[
                ((pc.CID(241), wd.CAS_Registry_Number),  # VV
                 (pc.CID(241), wd.CAS_Registry_Number)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.CAS_Registry_Number)),
                ((None, wd.CAS_Registry_Number),  # FV
                 (pc.CID(241), wd.CAS_Registry_Number)),
            ])

    def test_wd_ChEBI_ID(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.ChEBI_ID, ExternalId('16716')),  # VV
                 wd.ChEBI_ID(ExternalId('16716'))),
                ((wd.ChEBI_ID, None),  # VF
                 wd.ChEBI_ID(ExternalId('16716'))),
                ((None, ExternalId('16716')),  # FV
                 wd.ChEBI_ID(ExternalId('16716'))),
            ])
        self._test_filter_with_fixed_value(
            value=ExternalId('16716'),
            equals=[
                ((pc.CID(241), wd.ChEBI_ID),  # VV
                 (pc.CID(241), wd.ChEBI_ID)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.ChEBI_ID)),
                ((None, wd.ChEBI_ID),  # FV
                 (pc.CID(241), wd.ChEBI_ID)),
            ])

    def test_wd_ChEMBL_ID(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.ChEMBL_ID, ExternalId('CHEMBL277500')),  # VV
                 wd.ChEMBL_ID(ExternalId('CHEMBL277500'))),
                ((wd.ChEMBL_ID, None),  # VF
                 wd.ChEMBL_ID(ExternalId('CHEMBL277500'))),
                ((None, ExternalId('CHEMBL277500')),  # FV
                 wd.ChEMBL_ID(ExternalId('CHEMBL277500'))),
            ])
        self._test_filter_with_fixed_value(
            value=ExternalId('CHEMBL277500'),
            equals=[
                ((pc.CID(241), wd.ChEMBL_ID),  # VV
                 (pc.CID(241), wd.ChEMBL_ID)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.ChEMBL_ID)),
                ((None, wd.ChEMBL_ID),  # FV
                 (pc.CID(241), wd.ChEMBL_ID)),
            ])

    def test_wd_said_to_be_the_same_as(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.said_to_be_the_same_as, wd.benzene),  # VV
                 wd.said_to_be_the_same_as(wd.benzene)),
                ((None, wd.benzene),  # FV
                 wd.said_to_be_the_same_as(wd.benzene)),
            ],
            contains=[
                ((wd.said_to_be_the_same_as, None), [  # VF
                    wd.said_to_be_the_same_as(wd.benzene),
                    wd.said_to_be_the_same_as(wd.Q(26841227)),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=wd.benzene,
            equals=[
                ((pc.CID(241), wd.said_to_be_the_same_as),  # VV
                 (pc.CID(241), wd.said_to_be_the_same_as)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.said_to_be_the_same_as)),
                ((None, wd.said_to_be_the_same_as),  # FV
                 (pc.CID(241), wd.said_to_be_the_same_as)),
            ])

    def test_wd_has_part(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(162297440),
            equals=[
                ((wd.has_part, pc.CID(421)),  # VV
                 wd.has_part(pc.CID(421))),
                ((None, pc.CID(421)),  # FV
                 wd.has_part(pc.CID(421))),
            ],
            contains=[
                ((wd.has_part, None), [  # VF
                    wd.has_part(pc.CID(118615053)),
                    wd.has_part(pc.CID(23925)),
                    wd.has_part(pc.CID(23985)),
                    wd.has_part(pc.CID(297)),
                    wd.has_part(pc.CID(421)),
                    wd.has_part(pc.CID(7296)),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=pc.CID(421),
            equals=[
                ((pc.CID(162297440), wd.has_part),  # VV
                 (pc.CID(162297440), wd.has_part)),
                ((pc.CID(162297440), None),  # VF
                 (pc.CID(162297440), wd.has_part)),
            ],
            contains=[
                ((None, wd.has_part), [  # FV
                    (pc.CID(162297440), wd.has_part),
                    (pc.CID(157334304), wd.has_part),
                    (pc.CID(88108163), wd.has_part),
                ]),
            ])

    def test_wd_part_of(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(421),
            equals=[
                ((wd.part_of, pc.CID(162297440)),  # VV
                 wd.part_of(pc.CID(162297440))),
                ((None, pc.CID(162297440)),  # FV
                 wd.part_of(pc.CID(162297440))),
            ],
            contains=[
                ((wd.part_of, None), [  # VF
                    wd.part_of(pc.CID(10236840)),
                    wd.part_of(pc.CID(159688127)),
                    wd.part_of(pc.CID(87798102)),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=pc.CID(162297440),
            equals=[
                ((pc.CID(421), wd.part_of),  # VV
                 (pc.CID(421), wd.part_of)),
                ((pc.CID(421), None),  # VF
                 (pc.CID(421), wd.part_of)),
            ],
            contains=[
                ((None, wd.part_of), [  # FV
                    (pc.CID(162297441), wd.part_of),
                    (pc.CID(140801419), wd.part_of),
                    (pc.CID(118615175), wd.part_of),
                ]),
            ])

    def test_wd_InChI(self) -> None:
        inchi = ExternalId('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H')
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.InChI, inchi),  # VV
                 wd.InChI(inchi)),
                ((wd.InChI, None),  # VF
                 wd.InChI(inchi)),
                ((None, inchi),  # FV
                 wd.InChI(inchi)),
            ])
        self._test_filter_with_fixed_value(
            value=ExternalId('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H'),
            equals=[
                ((pc.CID(241), wd.InChI),  # VV
                 (pc.CID(241), wd.InChI)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.InChI)),
                ((None, wd.InChI),  # FV
                 (pc.CID(241), wd.InChI)),
            ])

    def test_wd_InChIKey(self) -> None:
        inchikey = ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N')
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.InChIKey, inchikey),  # VV
                 wd.InChIKey(inchikey)),
                ((wd.InChIKey, None),  # VF
                 wd.InChIKey(inchikey)),
                ((None, inchikey),  # FV
                 wd.InChIKey(inchikey)),
            ])
        self._test_filter_with_fixed_value(
            value=ExternalId('UHOVQNZJYSORNB-UHFFFAOYSA-N'),
            equals=[
                ((pc.CID(241), wd.InChIKey),  # VV
                 (pc.CID(241), wd.InChIKey)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.InChIKey)),
                ((None, wd.InChIKey),  # FV
                 (pc.CID(241), wd.InChIKey)),
            ])

    def test_wd_instance_of_type_of_a_chemical_entity(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.instance_of, wd.type_of_a_chemical_entity),  # VV
                 wd.instance_of(wd.type_of_a_chemical_entity)),
                ((wd.instance_of, None),  # VF
                 wd.instance_of(wd.type_of_a_chemical_entity)),
                ((None, wd.type_of_a_chemical_entity),  # FV
                 wd.instance_of(wd.type_of_a_chemical_entity)),
            ])
        self._test_filter_with_fixed_value(
            value=wd.type_of_a_chemical_entity,
            equals=[
                ((pc.CID(241), wd.instance_of),  # VV
                 (pc.CID(241), wd.instance_of)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.instance_of)),
            ])

    def test_pc_Isotope_Atom_Count(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(160456303),
            equals=[
                ((pc.Isotope_Atom_Count, 201),  # VV
                 pc.Isotope_Atom_Count(201)),
                ((pc.Isotope_Atom_Count, None),  # VF
                 pc.Isotope_Atom_Count(201)),
                ((pc.Isotope_Atom_Count, None),  # FV
                 pc.Isotope_Atom_Count(201)),
            ])
        self._test_filter_with_fixed_value(
            value=Quantity(201),
            equals=[
                ((pc.CID(160456303), pc.Isotope_Atom_Count),  # VV
                 (pc.CID(160456303), pc.Isotope_Atom_Count)),
                ((pc.CID(160456303), None),  # VF
                 (pc.CID(160456303), pc.Isotope_Atom_Count)),
            ],
            contains=[
                ((None, pc.Isotope_Atom_Count), [  # FV
                    (pc.CID(159391717), pc.Isotope_Atom_Count),
                    (pc.CID(159408424), pc.Isotope_Atom_Count),
                    (pc.CID(160456303), pc.Isotope_Atom_Count),
                ]),
            ])

    def test_wd_isomeric_SMILES(self) -> None:
        ismiles = String('C(CCC(=O)O)CC(CCS)S')
        self._test_filter_with_fixed_subject(
            subject=pc.CID(421),
            equals=[
                ((wd.isomeric_SMILES, ismiles),  # VV
                 wd.isomeric_SMILES(ismiles)),
                ((wd.isomeric_SMILES, None),  # VF
                 wd.isomeric_SMILES(ismiles)),
            ],
            contains=[
                ((None, ismiles), [  # FV
                    wd.canonical_SMILES(ismiles),
                    wd.isomeric_SMILES(ismiles),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=String('C(CCC(=O)O)CC(CCS)S'),
            equals=[
                ((pc.CID(421), wd.isomeric_SMILES),  # VV
                 (pc.CID(421), wd.isomeric_SMILES)),
                ((None, wd.isomeric_SMILES),  # FV
                 (pc.CID(421), wd.isomeric_SMILES)),
            ],
            contains=[
                ((pc.CID(421), None), [  # VF
                    (pc.CID(421), wd.canonical_SMILES),
                    (pc.CID(421), wd.isomeric_SMILES)
                ]),
            ])

    def test_wd_legal_status_medicine(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(10111431),
            equals=[
                ((wd.legal_status_medicine, wd.FDA_approved),  # VV
                 wd.legal_status_medicine(wd.FDA_approved)),
                ((wd.legal_status_medicine, None),  # VF
                 wd.legal_status_medicine(wd.FDA_approved)),
                ((None, wd.FDA_approved),  # FV
                 wd.legal_status_medicine(wd.FDA_approved)),
            ])
        self._test_filter_with_fixed_value(
            value=wd.FDA_approved,
            equals=[
                ((pc.CID(10111431), wd.legal_status_medicine),  # VV
                 (pc.CID(10111431), wd.legal_status_medicine)),
                ((pc.CID(10111431), None),  # VF
                 (pc.CID(10111431), wd.legal_status_medicine)),
            ])

    def test_wd_mass(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(170558098),
            equals=[
                ((wd.mass, '397.61'@wd.gram_per_mole),  # VV
                 wd.mass('397.61'@wd.gram_per_mole)),
                ((wd.mass, None),  # VF
                 wd.mass('397.61'@wd.gram_per_mole)),
                ((None, '397.61'@wd.gram_per_mole),  # FV
                 wd.mass('397.61'@wd.gram_per_mole)),
            ])
        self._test_filter_with_fixed_value(
            value='397.61'@wd.gram_per_mole,
            equals=[
                ((pc.CID(170558098), wd.mass),  # VV
                 (pc.CID(170558098), wd.mass)),
                ((pc.CID(170558098), None),  # VF
                 (pc.CID(170558098), wd.mass)),
            ],
            contains=[
                ((None, wd.mass), [  # VF
                    (pc.CID(168586903), wd.mass),
                    (pc.CID(170558098), wd.mass),
                    (pc.CID(171312105), wd.mass),
                ]),
            ])

    def test_wd_manufacturer(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(421),
            equals=[
                ((wd.manufacturer, pc.source('ID24800')),  # VV
                 wd.manufacturer(pc.source('ID24800'))),
                ((None, pc.source('ID24800')),  # FV
                 wd.manufacturer(pc.source('ID24800'))),
            ],
            contains=[
                ((wd.manufacturer, None), [  # VF
                    wd.manufacturer(pc.source('ID24800')),
                    wd.manufacturer(pc.source('NovoSeek')),
                    wd.manufacturer(pc.source('TCI_')),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=pc.source('ID24800'),
            equals=[
                ((pc.CID(421), wd.manufacturer),  # VV
                 (pc.CID(421), wd.manufacturer)),
                ((pc.CID(421), None),  # VF
                 (pc.CID(421), wd.manufacturer)),
            ])

    def test_wd_partition_coefficient_water_octanol(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(421),
            equals=[
                ((wd.partition_coefficient_water_octanol,  # VV
                  Quantity('1.8')),
                 wd.partition_coefficient_water_octanol(Quantity('1.8'))),
                ((wd.partition_coefficient_water_octanol, None),  # VF
                 wd.partition_coefficient_water_octanol(Quantity('1.8'))),
                ((None,  # FV
                  Quantity('1.8')),
                 wd.partition_coefficient_water_octanol(Quantity('1.8'))),
            ])
        self._test_filter_with_fixed_value(
            value=Quantity('1.8'),
            equals=[
                ((pc.CID(421), wd.partition_coefficient_water_octanol),  # VV
                 (pc.CID(421), wd.partition_coefficient_water_octanol)),
                ((pc.CID(421), None),  # VF
                 (pc.CID(421), wd.partition_coefficient_water_octanol)),
            ])

    def test_wd_PubChem_CID(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            equals=[
                ((wd.PubChem_CID, ExternalId('241')),  # VV
                 wd.PubChem_CID('241')),
                ((wd.PubChem_CID, None),  # VF
                 wd.PubChem_CID('241')),
                ((wd.PubChem_CID, None),  # FV
                 wd.PubChem_CID('241')),
            ])
        self._test_filter_with_fixed_value(
            value=ExternalId('241'),
            equals=[
                ((pc.CID(241), wd.PubChem_CID),  # VV
                 (pc.CID(241), wd.PubChem_CID)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), wd.PubChem_CID)),
                ((None, wd.PubChem_CID),  # FV
                 (pc.CID(241), wd.PubChem_CID)),
            ])

    def test_wd_stereoisomer_of(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(421),
            equals=[
                ((wd.stereoisomer_of, pc.CID(9834298)),  # VV
                 wd.stereoisomer_of(pc.CID(9834298))),
                ((None, pc.CID(9834298)),  # FV
                 wd.stereoisomer_of(pc.CID(9834298))),
            ],
            contains=[
                ((wd.stereoisomer_of, None), [  # VF
                    wd.stereoisomer_of(pc.CID(449141)),
                    wd.stereoisomer_of(pc.CID(9834298)),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=pc.CID(9834298),
            equals=[
                ((pc.CID(421), wd.stereoisomer_of),  # VV
                 (pc.CID(421), wd.stereoisomer_of)),
                ((pc.CID(421), None),  # VF
                 (pc.CID(421), wd.stereoisomer_of)),
            ],
            contains=[
                ((None, wd.stereoisomer_of), [  # FV
                    (pc.CID(421), wd.stereoisomer_of),
                    (pc.CID(449141), wd.stereoisomer_of),
                ]),
            ])

    # -- patent --

    def test_wd_author_name_string(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.patent('CN-208863666-U'),
            equals=[
                ((wd.author_name_string, String('PAN JUNBO')),  # VV
                 wd.author_name_string(String('PAN JUNBO'))),
                ((None, String('PAN JUNBO')),  # FV
                 wd.author_name_string(String('PAN JUNBO'))),
            ],
            contains=[
                ((wd.author_name_string, None), [  # VF
                    wd.author_name_string(String('PAN JUNBO')),
                    wd.author_name_string(String('SHI ZENGHUI')),
                    wd.author_name_string(String('Wang Qingrou')),
                    wd.author_name_string(String('YU ZHIYUAN')),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=String('PAN JUNBO'),
            equals=[
                ((pc.patent('CN-208863666-U'), wd.author_name_string),  # VV
                 (pc.patent('CN-208863666-U'), wd.author_name_string)),
                ((pc.patent('CN-208863666-U'), None),  # VF
                 (pc.patent('CN-208863666-U'), wd.author_name_string)),
            ],
            contains=[
                ((None, wd.author_name_string), [  # FV
                    (pc.patent('CN-208863666-U'), wd.author_name_string),
                    (pc.patent('CN-210399454-U'), wd.author_name_string),
                    (pc.patent('CN-210512710-U'), wd.author_name_string),
                ]),
            ])

    def test_wd_instance_of_patent(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.patent('CN-210512710-U'),
            equals=[
                ((wd.instance_of, wd.patent),  # VV
                 wd.instance_of(wd.patent)),
                ((wd.instance_of, None),  # VF
                 wd.instance_of(wd.patent)),
                ((None, wd.patent),  # FV
                 wd.instance_of(wd.patent)),
            ])
        self._test_filter_with_fixed_value(
            value=wd.patent,
            equals=[
                ((pc.patent('CN-210512710-U'), wd.instance_of),  # VV
                 (pc.patent('CN-210512710-U'), wd.instance_of)),
                ((pc.patent('CN-210512710-U'), None),  # VF
                 (pc.patent('CN-210512710-U'), wd.instance_of)),
            ])

    def test_wd_main_subject(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.patent('US-2019276396-A1'),
            equals=[
                ((wd.main_subject, pc.CID(449141)),  # VV
                 wd.main_subject(pc.CID(449141))),
                ((None, pc.CID(449141)),  # FV
                 wd.main_subject(pc.CID(449141))),
            ],
            contains=[
                ((wd.main_subject, None), [  # VF
                    wd.main_subject(pc.CID(139465320)),
                    wd.main_subject(pc.CID(449141)),
                    wd.main_subject(pc.CID(76963271)),
                    wd.main_subject(pc.CID(92171210)),
                    wd.main_subject(pc.CID(92171211)),
                ]),
            ])
        self._test_filter_with_fixed_value(
            value=pc.CID(449141),
            equals=[
                ((pc.patent('US-2019276396-A1'), wd.main_subject),  # VV
                 (pc.patent('US-2019276396-A1'), wd.main_subject)),
                ((pc.patent('US-2019276396-A1'), None),  # VF
                 (pc.patent('US-2019276396-A1'), wd.main_subject)),
            ],
            contains=[
                ((None, wd.main_subject), [  # FV
                    (pc.patent('US-2019276396-A1'), wd.main_subject),
                    (pc.patent('US-2013210908-A1'), wd.main_subject),
                    (pc.patent('EP-1307442-A2'), wd.main_subject),
                ]),
            ])

    def test_wd_patent_number(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.patent('US-2019276396-A1'),
            equals=[
                ((wd.patent_number, ExternalId('US-2019276396-A1')),  # VV
                 wd.patent_number('US-2019276396-A1')),
                ((wd.patent_number, None),  # VF
                 wd.patent_number('US-2019276396-A1')),
                ((None, ExternalId('US-2019276396-A1')),  # FV
                 wd.patent_number('US-2019276396-A1')),
            ])
        self._test_filter_with_fixed_value(
            value=ExternalId('US-2019276396-A1'),
            equals=[
                ((pc.patent('US-2019276396-A1'), wd.patent_number),  # VV
                 (pc.patent('US-2019276396-A1'), wd.patent_number)),
                ((pc.patent('US-2019276396-A1'), None),  # VF
                 (pc.patent('US-2019276396-A1'), wd.patent_number)),
                ((None, wd.patent_number),  # FV
                 (pc.patent('US-2019276396-A1'), wd.patent_number)),
            ])

    def test_wd_publication_date(self) -> None:
        dt = Time('2019-09-12+04:00', 11, 0, wd.proleptic_Gregorian_calendar)
        self._test_filter_with_fixed_subject(
            subject=pc.patent('US-2019276396-A1'),
            equals=[
                ((wd.publication_date, dt),  # VV
                 wd.publication_date(dt)),
                ((wd.publication_date, None),  # VF
                 wd.publication_date(dt)),
                ((None, dt),  # FV
                 wd.publication_date(dt)),
            ])
        self._test_filter_with_fixed_value(
            value=Time('2019-09-12+04:00', 11, 0,
                       wd.proleptic_Gregorian_calendar),
            equals=[
                ((pc.patent('US-2019276396-A1'), wd.publication_date),  # VV
                 (pc.patent('US-2019276396-A1'), wd.publication_date)),
                ((pc.patent('US-2019276396-A1'), None),  # VF
                 (pc.patent('US-2019276396-A1'), wd.publication_date)),
            ])

    def test_wd_title(self) -> None:
        title = Text(
            'Novel functionalized 5-(phenoxymethyl)-1,3-dioxane '
            'analogs exhibiting cytochrome p450 inhibition and '
            'their method of use', 'en')
        self._test_filter_with_fixed_subject(
            subject=pc.patent('US-2016244436-A1'),
            equals=[
                ((wd.title, title),  # VV
                 wd.title(title)),
                ((wd.title, None),  # VF
                 wd.title(title)),
                ((None, title),  # FV
                 wd.title(title)),
            ])
        self._test_filter_with_fixed_value(
            value=title,
            equals=[
                ((pc.patent('US-2016244436-A1'), wd.title),  # VV
                 (pc.patent('US-2016244436-A1'), wd.title)),
                ((pc.patent('US-2016244436-A1'), None),  # VF
                 (pc.patent('US-2016244436-A1'), wd.title)),
                ((None, wd.title),  # FV
                 (pc.patent('US-2016244436-A1'), wd.title)),
            ])

    # -- source --

    def test_wd_instance_of_vendor(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.source('ID24800'),
            equals=[
                ((wd.instance_of, wd.vendor),  # VV
                 wd.instance_of(wd.vendor)),
                ((wd.instance_of, None),  # VF
                 wd.instance_of(wd.vendor)),
                ((None, wd.vendor),  # FV
                 wd.instance_of(wd.vendor)),
            ])
        self._test_filter_with_fixed_value(
            value=wd.vendor,
            equals=[
                ((pc.source('ID24800'), wd.instance_of),  # VV
                 (pc.source('ID24800'), wd.instance_of)),
                ((pc.source('ID24800'), None),  # VF
                 (pc.source('ID24800'), wd.instance_of)),
            ])


if __name__ == '__main__':
    Test.main()
