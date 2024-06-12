# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import AnnotationRecord, IRI, Normal, Quantity, ReferenceRecord
from kif_lib.vocabulary import wd

from .tests import kif_WikidataSPARQL_StoreTestCase


class TestStoreSPARQL_SPARQL_StoreAnnotations(
        kif_WikidataSPARQL_StoreTestCase):

    def test_get_annotations_bad_argument(self):
        kb = self.new_Store()
        self.assertRaises(TypeError, kb.get_annotations, 0)
        self.assertRaises(TypeError, next, kb.get_annotations(IRI('x')))

    def test_get_annotations_quantity(self):
        kb = self.new_Store()
        qt = Quantity('.88', wd.gram_per_cubic_centimetre, '.87', '.89')
        sin = wd.density(wd.benzene, qt)
        sout, annots = next(kb.get_annotations([sin]))
        self.assertEqual(sin, sout)
        self.assertIsNotNone(annots)
        assert annots is not None
        self.assert_annotation_record_set(
            annots,
            AnnotationRecord(
                [wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
                 wd.phase_of_matter(wd.liquid)],
                [ReferenceRecord(
                    wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
                    wd.stated_in(wd.Hazardous_Substances_Data_Bank))],
                Normal))

    def test_get_annotations_more_than_one(self):
        kb = self.new_Store()
        qt = Quantity(20000, wd.parts_per_million, 19999, 20001)
        sin = wd.minimal_lethal_dose(wd.benzene, qt)
        sout, annots = next(kb.get_annotations([sin]))
        self.assertEqual(sin, sout)
        self.assertIsNotNone(annots)
        assert annots is not None
        self.assert_annotation_record_set(
            annots,
            AnnotationRecord(
                [wd.duration(Quantity(2, wd.minute, 1, 3)),
                 wd.route_of_administration(wd.inhalation),
                 wd.afflicts(wd.human)],
                [ReferenceRecord(
                    wd.reference_URL(IRI(
                        'http://www.cdc.gov/niosh-rtecs/'
                        'CY155CC0.html#modalIdString_CDCTable_4')))],
                Normal),
            AnnotationRecord(
                [wd.duration(Quantity(5, wd.minute, 4, 6)),
                 wd.route_of_administration(wd.inhalation),
                 wd.afflicts(wd.human)],
                [ReferenceRecord(
                    wd.reference_URL(IRI(
                        'http://www.cdc.gov/niosh-rtecs/'
                        'CY155CC0.html#modalIdString_CDCTable_4'))),
                 ReferenceRecord(
                     wd.reference_URL(IRI(
                         'http://www.cdc.gov/niosh-rtecs/'
                         'CY155CC0.html#modalIdString_CDCTable_7')))],
                Normal),
            AnnotationRecord(
                [wd.duration(Quantity(5, wd.minute, 4, 6)),
                 wd.route_of_administration(wd.inhalation),
                 wd.afflicts(wd.mammal)],
                [ReferenceRecord(
                    wd.reference_URL(IRI(
                        'http://www.cdc.gov/niosh-rtecs/'
                        'CY155CC0.html#modalIdString_CDCTable_4')))],
                Normal))


if __name__ == '__main__':
    TestStoreSPARQL_SPARQL_StoreAnnotations.main()
