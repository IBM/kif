# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import IRI, Quantity, ReferenceRecord
from kif_lib.vocabulary import wd

from .tests import WikidataStoreTestCase


class TestStoreSPARQL_SPARQL_StoreAnnotations(WikidataStoreTestCase):

    def test_get_annotations_bad_argument(self) -> None:
        kb = self.new_Store()
        self.assertRaises(TypeError, kb.get_annotations, 0)
        self.assertRaises(TypeError, next, kb.get_annotations(IRI('x')))

    def test_get_annotations_quantity(self) -> None:
        kb = self.new_Store()
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, '.87', '.89')
        sin = wd.density(wd.benzene, qt)
        sout, annots = next(kb.get_annotations([sin]))
        self.assertEqual(sin, sout)
        self.assertIsNotNone(annots)
        assert annots is not None
        self.assertEqual(len(annots), 1)
        annot = next(iter(annots))
        self.assert_qualifier_record(
            annot[0],
            wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
            wd.phase_of_matter(wd.liquid))
        self.assert_reference_record_set(
            annot[1], ReferenceRecord(
                wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
                wd.stated_in(wd.Hazardous_Substances_Data_Bank)))
        self.assert_normal_rank(annot[2])

    def test_get_annotations_more_than_one(self) -> None:
        kb = self.new_Store()
        qt = Quantity(20000, wd.parts_per_million, 19999, 20001)
        sin = wd.minimal_lethal_dose(wd.benzene, qt)
        sout, annots = next(kb.get_annotations([sin]))
        self.assertEqual(sin, sout)
        self.assertIsNotNone(annots)
        assert annots is not None
        self.assertEqual(len(annots), 3)
        annot0, annot1, annot2 = list(sorted(annots))
        self.assert_qualifier_record(
            annot0[0],
            wd.duration(Quantity(2, wd.minute, 1, 3)),
            wd.route_of_administration(wd.inhalation),
            wd.afflicts(wd.human))
        self.assert_reference_record_set(
            annot0[1],
            ReferenceRecord(
                wd.reference_URL(IRI(
                    'http://www.cdc.gov/niosh-rtecs/'
                    'CY155CC0.html#modalIdString_CDCTable_4'))))
        self.assert_normal_rank(annot0[2])
        self.assert_qualifier_record(
            annot1[0],
            wd.duration(Quantity(5, wd.minute, 4, 6)),
            wd.route_of_administration(wd.inhalation),
            wd.afflicts(wd.human))
        self.assert_reference_record_set(
            annot1[1],
            ReferenceRecord(
                wd.reference_URL(IRI(
                    'http://www.cdc.gov/niosh-rtecs/'
                    'CY155CC0.html#modalIdString_CDCTable_4'))),
            ReferenceRecord(
                wd.reference_URL(IRI(
                    'http://www.cdc.gov/niosh-rtecs/'
                    'CY155CC0.html#modalIdString_CDCTable_7'))))
        self.assert_normal_rank(annot1[2])
        self.assert_qualifier_record(
            annot2[0],
            wd.duration(Quantity(5, wd.minute, 4, 6)),
            wd.route_of_administration(wd.inhalation),
            wd.afflicts(wd.mammal))
        self.assert_reference_record_set(
            annot2[1],
            ReferenceRecord(
                wd.reference_URL(IRI(
                    'http://www.cdc.gov/niosh-rtecs/'
                    'CY155CC0.html#modalIdString_CDCTable_4'))))
        self.assert_normal_rank(annot2[2])


if __name__ == '__main__':
    TestStoreSPARQL_SPARQL_StoreAnnotations.main()
