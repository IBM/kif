# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, Item, Snak, String, Time
from kif_lib.vocabulary import wd

from .tests import kif_PubChemSPARQL_StoreTestCase


class TestStoreMapperMappingPubChemStatements(
        kif_PubChemSPARQL_StoreTestCase):

    def test_filter_sanity(self):
        pass

    def check_empty_filter(self, kb, *args, **kwargs):
        limit = kwargs.pop('limit', 1)
        self.assertFalse(bool(list(kb.filter(*args, limit=limit, **kwargs))))

    def check_filter(self, kb, f, *args, **kwargs):
        limit = kwargs.pop('limit', 10)
        stmts = list(kb.filter(*args, limit=limit, **kwargs))
        self.assertEqual(len(stmts), limit)
        for (s, (p, v)) in stmts:
            f(kb, s, p, v)
        self.assertIn(stmts[0], kb)

    def check_filter_property(
            self, kb, property, datatype,
            subject_check=None, value_check=None, **kwargs):
        if subject_check is None:
            subject_check = (lambda kb, v: True)
        if value_check is None:
            value_check = (lambda kb, v: True)
        self.check_empty_filter(
            kb, None, property, snak_mask=Snak.SOME_VALUE_SNAK)
        self.check_empty_filter(kb, Item('x'), property)
        if datatype.is_string_datatype():
            value = Item('x')
        else:
            value = String('x')
        self.check_empty_filter(kb, None, property, value)

        def check(kb, s, p, v):
            self.assertIsInstance(s, Item)
            self.assertTrue(subject_check(kb, s))
            self.assertEqual(p, property)
            self.assertIsInstance(v, datatype.to_value_class())
            self.assertTrue(value_check(kb, v))
        self.check_filter(kb, check, property=property)

# -- Compound --------------------------------------------------------------

    def check_filter_compound_property(
            self, kb, property, datatype, value_check=None, **kwargs):
        return self.check_filter_property(
            kb, property, datatype,
            (lambda kb, v: v.is_item()
             and kb.mapping.is_pubchem_compound_iri(v.iri)),
            value_check, **kwargs)

    def test_filter_property_canonical_SMILES(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.canonical_SMILES, Datatype.string)

    def test_filter_property_chemical_formula(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.canonical_SMILES, Datatype.string)

    def test_filter_property_CAS_Registry_Number(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.CAS_Registry_Number, Datatype.string)

    def test_filter_property_ChEBI_ID(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.ChEBI_ID, Datatype.string)

    def test_filter_property_ChEMBL(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.ChEMBL_ID, Datatype.string)

    def test_filter_property_trading_name(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.trading_name, Datatype.text,
            lambda kb, v: v.language == 'en')

    def test_filter_property_described_by_source(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.described_by_source, Datatype.item,
            lambda kb, v: kb.mapping.is_pubchem_patent_iri(v.iri))

    def test_filter_property_has_part(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.has_part, Datatype.item,
            lambda kb, v: kb.mapping.is_pubchem_compound_iri(v.iri))

    def test_filter_property_InChI(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.InChI, Datatype.string)

    def test_filter_property_mass(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.mass, Datatype.quantity,
            (lambda kb, v: v.unit == wd.gram_per_mole
             and v.lower_bound is None and v.upper_bound is None))

    def test_filter_property_manufacturer(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.manufacturer, Datatype.item,
            lambda kb, v: kb.mapping.is_pubchem_source_iri(v.iri))

    def test_filter_property_PubChem_CID(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.PubChem_CID, Datatype.string)

    def test_filter_property_stereoisomer_of(self):
        self.check_filter_compound_property(
            self.new_Store(), wd.stereoisomer_of, Datatype.item,
            lambda kb, v: kb.mapping.is_pubchem_compound_iri(v.iri))

# -- Patent ----------------------------------------------------------------

    def check_filter_patent_property(
            self, kb, property, datatype, value_check=None, **kwargs):
        return self.check_filter_property(
            kb, property, datatype,
            (lambda kb, v: v.is_item()
             and kb.mapping.is_pubchem_patent_iri(v.iri)), **kwargs)

    def test_filter_property_author_name_string(self):
        self.check_filter_patent_property(
            self.new_Store(), wd.author_name_string, Datatype.string)

    def test_filter_property_main_subject(self):
        self.check_filter_patent_property(
            self.new_Store(), wd.main_subject, Datatype.item,
            lambda kb, v: kb.mapping.is_pubchem_compound_iri(v.iri))

    def test_filter_property_patent_number(self):
        self.check_filter_patent_property(
            self.new_Store(), wd.patent_number, Datatype.string)

    def test_filter_property_publication_date(self):
        self.check_filter_patent_property(
            self.new_Store(), wd.publication_date, Datatype.time,
            (lambda kb, v: v.precision == Time.DAY and v.timezone == 0
             and v.calendar == wd.proleptic_Gregorian_calendar))

    def test_filter_property_sponsor(self):
        self.check_filter_patent_property(
            self.new_Store(), wd.sponsor, Datatype.string)

    def test_filter_property_title(self):
        self.check_filter_patent_property(
            self.new_Store(), wd.title, Datatype.text,
            lambda kb, v: v.language == 'en')


if __name__ == '__main__':
    TestStoreMapperMappingPubChemStatements.main()
