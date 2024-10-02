# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    Filter,
    Fingerprint,
    Item,
    Quantity,
    String,
    Time,
    Variables,
)
from kif_lib.vocabulary import pc, wd

from ....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    def test_empty(self) -> None:
        self._test_filter_preset_empty()

    def test_value_fp_compound(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            contains=[
                ((None, None), [  # FF
                    pc.Isotope_Atom_Count(0),
                    wd.canonical_SMILES('C1=CC=CC=C1'),
                    wd.CAS_Registry_Number('2396-01-2'),
                    wd.CAS_Registry_Number('71-43-2'),
                    wd.ChEBI_ID('16716'),
                    wd.ChEMBL_ID('CHEMBL277500'),
                    wd.InChI('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H'),
                    wd.InChIKey('UHOVQNZJYSORNB-UHFFFAOYSA-N'),
                    wd.instance_of(wd.type_of_a_chemical_entity),
                    wd.isomeric_SMILES('C1=CC=CC=C1'),
                    wd.manufacturer(
                        'http://rdf.ncbi.nlm.nih.gov/pubchem/source/ID924'),
                    wd.mass('78.11'@wd.gram_per_mole),
                    wd.partition_coefficient_water_octanol('2.1'),
                    wd.PubChem_CID('241'),
                ]),
            ])

    def test_snak_fp_compound(self) -> None:
        fps = [
            Fingerprint.check(wd.ChEMBL_ID('CHEMBL277500')),
            -(wd.has_part(pc.CID(139250634))),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, wd.PubChem_CID, '241'),  # VV
                     wd.PubChem_CID(pc.CID(241), '241')),
                    (Filter(fp, None, ExternalId('16716')),  # FV
                     wd.ChEBI_ID(pc.CID(241), '16716')),
                ],
                contains=[
                    (Filter(fp, wd.mass, None),  [  # VF
                        wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole),
                    ]),
                ])

    def test_value_fp_patent(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.patent('BR-PI0506496-B1'),
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
                        'composition comprising sulfobutylether-ß-cyclodextrin '
                        'and its use in the treatment of emesisEmproved '
                        'injection site tolerance pharmaceutical composition '
                        'comprising sulfobutylether-ß-cyclodextrin and its '
                        'use in the treatment of emesisEmproved tolerance '
                        'pharmaceutical composition injection comprising '
                        'sulfobutylether-ß-cyclodextrin and its use in the '
                        'treatment of emesis'),
                ]),
            ])

    def test_snak_fp_patent(self) -> None:
        fps = [
            Fingerprint.check(wd.patent_number('BR-PI0506496-B1')),
            Fingerprint.check(wd.title(
                'Improved injection site tolerance pharmaceutical '
                'composition comprising sulfobutylether-ß-cyclodextrin '
                'and its use in the treatment of emesisEmproved '
                'injection site tolerance pharmaceutical composition '
                'comprising sulfobutylether-ß-cyclodextrin and its '
                'use in the treatment of emesisEmproved tolerance '
                'pharmaceutical composition injection comprising '
                'sulfobutylether-ß-cyclodextrin and its use in the '
                'treatment of emesis')),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(fp, wd.patent_number, 'BR-PI0506496-B1'),  # VV
                     wd.patent_number(
                         pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
                    (Filter(fp, wd.patent_number, None),  # VF
                     wd.patent_number(
                         pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
                    (Filter(fp, None, ExternalId('BR-PI0506496-B1')),  # FV
                     wd.patent_number(
                         pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
                ])

    def test_value_fp_source(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.source('ChemBlock'),
            contains=[
                ((None, None), [  # FF
                    wd.instance_of(wd.business),
                ]),
            ])

    def test_value_fp_property(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.Isotope_Atom_Count,
            equals=[
                ((None, None),  # FF
                 wd.instance_of(wd.Wikidata_property_related_to_chemistry)),
            ])


if __name__ == '__main__':
    Test.main()
