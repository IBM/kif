# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, Filter, Item, Quantity, String, Variables
from kif_lib.vocabulary import pc, wd

from ....tests import PubChemStoreTestCase

x, y, z = Variables(*'xyz')


class Test(PubChemStoreTestCase):

    def test_empty(self) -> None:
        self._test_filter_preset_empty()

    def test_property_canonical_SMILES(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.canonical_SMILES,
            empty=[
                (pc.CID(241), 'x'),  # VV
                (wd.benzene, 'x'),
                (wd.benzene, None),  # VF
                (pc.Isotope_Atom_Count, None),
                (None, 'x'),    # FV
            ],
            equals=[
                ((pc.CID(241), 'C1=CC=CC=C1'),  # VV
                 (pc.CID(241), 'C1=CC=CC=C1')),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), 'C1=CC=CC=C1')),
            ],
            contains=[
                ((None, 'C1=CC=CC=C1'), [  # FV
                    (pc.CID(241), 'C1=CC=CC=C1'),
                    (pc.CID(12196274), 'C1=CC=CC=C1'),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(None, wd.canonical_SMILES, None),
            wd.canonical_SMILES(Item(x), String(y)))

    def test_property_has_part(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.has_part,
            empty=[
                (wd.benzene, wd.caffeine),  # VV
                (pc.Isotope_Atom_Count, pc.CID(421)),
                (pc.CID(241), pc.CID(340032)),
                (wd.benzene, None),  # VF
                (pc.Isotope_Atom_Count, None),
                (pc.CID(241), None),
                (None, wd.benzene),  # FV
                (None, pc.CID(340032)),
            ],
            equals=[
                ((pc.CID(340032), None),  # VF
                 (pc.CID(340032), pc.CID(241))),
            ],
            contains=[
                ((None, pc.CID(421)), [  # FV
                    (pc.CID(10236840), pc.CID(421)),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(None, wd.has_part, None),
            wd.has_part(Item(x), Item(y)))

    def test_property_instance_of(self) -> None:
        # self._test_filter_with_fixed_property(
        #     property=wd.instance_of,
        #     empty=[
        #         (wd.chemical_formula,  # VV
        #          wd.Wikidata_property_related_to_medicine),
        #         (wd.benzene, None),  # VF
        #         (pc.CID(421), None),
        #         (None, wd.benzene),  # FV
        #     ],
        #     equals=[
        #         ((pc.Isotope_Atom_Count,  # VV
        #           wd.Wikidata_property_related_to_chemistry),
        #          (pc.Isotope_Atom_Count,
        #           wd.Wikidata_property_related_to_chemistry)),
        #         ((pc.Isotope_Atom_Count, None),  # VF
        #          (pc.Isotope_Atom_Count,
        #           wd.Wikidata_property_related_to_chemistry)),
        #         ((None, wd.Wikidata_property_related_to_chemistry),  # FV
        #          (pc.Isotope_Atom_Count,
        #           wd.Wikidata_property_related_to_chemistry)),
        #     ])
        self._test_filter_matches(  # FF
            Filter(None, wd.instance_of, None),
            wd.instance_of(x, Item(y)))

    def test_property_Isotope_Atom_Count(self) -> None:
        self._test_filter_with_fixed_property(
            property=pc.Isotope_Atom_Count,
            empty=[
                (pc.CID(241), 1),    # VV
                (wd.benzene, None),  # VF
                (pc.Isotope_Atom_Count, None),
                (None, 201@wd.kilogram),  # FV
            ],
            equals=[
                ((pc.CID(241), 0),  # VV
                 (pc.CID(241), 0)),
            ],
            contains=[
                ((None, 201), [  # FV
                    (pc.CID(160456303), 201)
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(None, pc.Isotope_Atom_Count, None),
            pc.Isotope_Atom_Count(Item(x), Quantity(y)))

    def test_property_mass(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.mass,
            empty=[
                (pc.CID(241), '78.10'@wd.gram_per_mole),  # VV
                (pc.CID(241), '78.11'@wd.dalton),
                (pc.CID(241), Quantity('78.11', wd.gram_per_mole, 0)),
                (pc.CID(241), Quantity('78.11', wd.gram_per_mole, None, 1)),
                (wd.benzene, '78.11'@wd.gram_per_mole),
                (wd.benzene, None),  # VF
                (pc.Isotope_Atom_Count, None),
                (None, 10**8@wd.gram_per_mole),  # FV
            ],
            equals=[
                ((pc.CID(241), '78.11'@wd.gram_per_mole),  # VV
                 (pc.CID(241), '78.11'@wd.gram_per_mole)),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), '78.11'@wd.gram_per_mole)),
            ],
            contains=[
                ((None, '78.11'@wd.gram_per_mole), [  # VF
                    (pc.CID(241), '78.11'@wd.gram_per_mole),
                    (pc.CID(168743091), '78.11'@wd.gram_per_mole),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(None, wd.mass, None),
            wd.mass(Item(x), Quantity(y, wd.gram_per_mole)))

    def test_property_PubChem_CID(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.PubChem_CID,
            empty=[
                (wd.benzene, ExternalId('421')),  # VV
                (pc.CID(421), ExternalId('422')),
                (wd.benzene, None),  # VF
                (pc.Isotope_Atom_Count, None),
                (None, ExternalId('abc')),  # FV
            ],
            equals=[
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), ExternalId('241'))),
                ((None, ExternalId('241')),  # FV
                 (pc.CID(241), ExternalId('241'))),
                ((None, String('241')),  # FV
                 (pc.CID(241), ExternalId('241'))),
            ],
        )
        self._test_filter_matches(  # FF
            Filter(None, wd.PubChem_CID, None),
            wd.PubChem_CID(Item(x), ExternalId(y)))


if __name__ == '__main__':
    Test.main()
