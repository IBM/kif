# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, Quantity, Statement, String, Time
from kif_lib.vocabulary import wd

from .tests import kif_PubChemSPARQL_StoreTestCase


class TestStoreMapperMappingPubChemStatements(
        kif_PubChemSPARQL_StoreTestCase):

    def test_filter_sanity(self):
        pass

    def check_filter_call(self, kb, f, *args, **kwargs):
        limit = kwargs.pop('limit', 10)
        stmts = list(kb.filter(*args, limit=limit, **kwargs))
        self.assertEqual(len(stmts), limit)
        for (s, (p, v)) in stmts:
            f(kb, s, p, v)

    def test_filter_property_described_by_source(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_compound_iri(s.iri))
            self.assertEqual(p, wd.described_by_source)
            self.assertIsInstance(v, Item)
            self.assertTrue(kb.mapping.is_pubchem_patent_iri(v.iri))
        self.check_filter_call(
            self.new_Store(), check, property=wd.described_by_source)

    def test_filter_property_InChI(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_compound_iri(s.iri))
            self.assertEqual(p, wd.InChI)
            self.assertIsInstance(v, String)
            self.assertEqual(kb.mapping.Spec.check_InChI(v), v.value)
        self.check_filter_call(
            self.new_Store(), check, property=wd.InChI)

    def test_filter_property_mass(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_compound_iri(s.iri))
            self.assertEqual(p, wd.mass)
            self.assertIsInstance(v, Quantity)
            self.assertEqual(v.unit, wd.gram_per_mole)
            self.assertIsNone(v.lower_bound)
            self.assertIsNone(v.upper_bound)
        self.check_filter_call(
            self.new_Store(), check, property=wd.mass)

    def test_filter_property_author_name_string(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_patent_iri(s.iri))
            self.assertEqual(p, wd.author_name_string)
            self.assertIsInstance(v, String)
        self.check_filter_call(
            self.new_Store(), check, property=wd.author_name_string)

    def test_filter_property_main_subject(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_patent_iri(s.iri))
            self.assertEqual(p, wd.main_subject)
            self.assertIsInstance(v, Item)
            self.assertTrue(kb.mapping.is_pubchem_compound_iri(v.iri))
        self.check_filter_call(
            self.new_Store(), check, property=wd.main_subject)

    def test_filter_property_patent_number(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_patent_iri(s.iri))
            self.assertEqual(p, wd.patent_number)
            self.assertIsInstance(v, String)  # FIXME: ExternalId
        self.check_filter_call(
            self.new_Store(), check, property=wd.patent_number)

    def test_filter_property_publication_date(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_patent_iri(s.iri))
            self.assertEqual(p, wd.publication_date)
            self.assertIsInstance(v, Time)
            self.assertEqual(v.precision, Time.DAY)
            self.assertEqual(v.timezone, 0)
            self.assertEqual(v.calendar, wd.proleptic_Gregorian_calendar)
        self.check_filter_call(
            self.new_Store(), check, property=wd.publication_date)

    def test_filter_property_sponsor(self):
        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(kb.mapping.is_pubchem_patent_iri(s.iri))
            self.assertEqual(p, wd.sponsor)
            self.assertIsInstance(v, String)
        self.check_filter_call(self.new_Store(), check, property=wd.sponsor)


if __name__ == '__main__':
    TestStoreMapperMappingPubChemStatements.main()
