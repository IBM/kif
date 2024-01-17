# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    Descriptor,
    Quantity,
    Statement,
    Store,
    String,
    Text,
    Time,
)
from kif_lib.store.mapping import PubChemMapping

from .tests import kif_TestCase, main, PUBCHEM, skip_if_set

skip_if_set('SKIP_TEST_STORE_PUBCHEM')


class TestSPARQL_MapperStorePubChem(kif_TestCase):

    def new(self, **kwargs):
        return Store('sparql-mapper', PUBCHEM, PubChemMapping, **kwargs)

    def test_sanity(self):
        self.store_sanity_checks(self.new())

    # -- Set interface -----------------------------------------------------

    def test__iter__(self):
        kb = self.new()
        stmt = next(iter(kb))
        self.assertIsInstance(stmt, Statement)
        # force pagination
        it = iter(self.new(page_size=1))
        for i in range(3):
            self.assertIsInstance(next(it), Statement)

    # -- Queries -----------------------------------------------------------

    def test_contains(self):
        kb = self.new()
        self.store_test_contains(
            kb,
            # entity
            wd.described_by_source(
                wd.Q('_PUBCHEM_COMPOUND_CID422'),
                wd.Q('_PUBCHEM_PATENT_EP-3888693-A1')),
            # text
            wd.title(
                wd.Q('_PUBCHEM_PATENT_AU-2010262786-A1'),
                Text('Improved method for quantifying DNA'
                     ' in a biological sample')),
            # string
            wd.patent_number(
                wd.Q('_PUBCHEM_PATENT_AP-0102072-A0'),
                String('AP-0102072-A0')),
            # quantity
            wd.mass(
                wd.Q('_PUBCHEM_COMPOUND_CID734888'),
                Quantity('340.1310119628906', wd.gram_per_mole)),
            # time
            wd.publication_date(
                wd.Q('_PUBCHEM_PATENT_AP-1072-A'), Time('2002-05-29:04')),
            wd.publication_date(
                wd.Q('_PUBCHEM_PATENT_AP-1072-A'),
                Time('2002-05-29:04', Time.DAY)),
        )
        self.store_test_not_contains(
            kb,
            # entity
            wd.described_by_source(
                wd.Q('_PUBCHEM_COMPOUND_CID734888'),
                wd.Q('_PUBCHEM_PATENT_EP-3888693-A1')),
            # text
            wd.title(
                wd.Q('_PUBCHEM_PATENT_AU-2010262786-A1'),
                Text('Improved method for quantifying dna'
                     ' in a biological sample')),
            # quantity
            wd.mass(
                wd.Q('_PUBCHEM_COMPOUND_CID734888'),
                Quantity('340.1310119628906', wd.kilogram)),
            wd.mass(
                wd.Q('_PUBCHEM_COMPOUND_CID734888'),
                Quantity('340.1310119628906', wd.gram_per_mole, 33)),
            wd.mass(
                wd.Q('_PUBCHEM_COMPOUND_CID734888'),
                Quantity('340.1310119628906', wd.gram_per_mole, None, 3333)),
            # time
            wd.publication_date(
                wd.Q('_PUBCHEM_PATENT_AP-1072-A'), Time('2002-05-29:00')),
            wd.publication_date(
                wd.Q('_PUBCHEM_PATENT_AP-1072-A'),
                Time('2002-05-29:04', Time.YEAR)),
            wd.publication_date(
                wd.Q('_PUBCHEM_PATENT_AP-1072-A'),
                Time('2002-05-29:04', None, 1)),
            wd.publication_date(
                wd.Q('_PUBCHEM_PATENT_AP-1072-A'),
                Time('2002-05-29:04', None, None,
                     wd.proleptic_Julian_calendar)),
        )

    def test_count(self):
        kb = self.new()
        self.store_test_count(
            kb, 1, wd.Q('_PUBCHEM_PATENT_AP-1072-A'), wd.publication_date)

    def test_filter(self):
        kb = self.new()
        self.store_test_filter(
            kb,
            [wd.title(
                wd.Q('_PUBCHEM_PATENT_AU-2010262786-A1'),
                Text('Improved method for quantifying DNA'
                     ' in a biological sample'))],
            subject=wd.Q('_PUBCHEM_PATENT_AU-2010262786-A1'),
            property=wd.title)

    # -- Annotations -------------------------------------------------------

    def test_get_annotations(self):
        kb = self.new()
        stmt1 = wd.title(
            wd.Q('_PUBCHEM_PATENT_AU-2010262786-A1'),
            Text('Improved method for quantifying DNA in a biological sample'))
        self.assertIn(stmt1, kb)
        stmt2 = stmt1.replace(wd.Q('_PUBCHEM_PATENT_AU-2010262786-A2'))
        self.store_test_get_annotations(
            kb,
            [(stmt1, AnnotationRecordSet(AnnotationRecord())),
             (stmt2, None)],
            stmt1,
            stmt2)

    # -- Descriptor --------------------------------------------------------

    def test_get_descriptor(self):
        kb = self.new()
        self.store_test_get_descriptor(
            kb,
            [(wd.Brazil, Descriptor()),
             (wd.instance_of, Descriptor())],
            'en',
            wd.Brazil, wd.instance_of)


if __name__ == '__main__':
    main()
