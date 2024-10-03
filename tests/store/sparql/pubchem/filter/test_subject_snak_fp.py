# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Filter, Fingerprint, Variables
from kif_lib.vocabulary import pc, wd

from .....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    def test_item_compound(self) -> None:
        fps = [
            Fingerprint.check(wd.ChEMBL_ID('CHEMBL277500')),
            -(wd.has_part(pc.CID(139250634))),
        ]
        for fp in fps:
            self._test_filter(
                equals=[
                    (Filter(    # VV
                        fp, wd.PubChem_CID, '241'),
                     wd.PubChem_CID(pc.CID(241), '241')),
                    (Filter(    # FV
                        fp, None, ExternalId('16716')),
                     wd.ChEBI_ID(pc.CID(241), '16716')),
                ],
                contains=[
                    (Filter(    # VF
                        fp, wd.mass, None), [
                        wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole),
                    ]),
                ])

    def test_item_patent(self) -> None:
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
                    (Filter(    # VV
                        fp, wd.patent_number, 'BR-PI0506496-B1'),
                     wd.patent_number(
                         pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
                    (Filter(    # VF
                        fp, wd.patent_number, None),
                     wd.patent_number(
                         pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
                    (Filter(    # FV
                        fp, None, ExternalId('BR-PI0506496-B1')),
                     wd.patent_number(
                         pc.patent('BR-PI0506496-B1'), 'BR-PI0506496-B1')),
                ])

    def test_item_source(self) -> None:
        pass

    def test_property_Isotope_Atom_Count(self) -> None:
        pass


if __name__ == '__main__':
    Test.main()
