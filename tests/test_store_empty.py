# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif.vocabulary as wd
from kif import (
    Descriptor,
    NoValueSnak,
    Quantity,
    SnakMask,
    SomeValueSnak,
    Statement,
    Store,
    Time,
)
from kif.store import EmptyStore

from .tests import kif_TestCase, main


class TestEmptyStore(kif_TestCase):

    def test_sanity(self):
        self.store_sanity_checks(Store('empty'))

    def test__init__(self):
        kb = Store('empty')
        self.assertIsInstance(kb, EmptyStore)
        # namespaces
        ns = {'ex': 'http://example.org/'}
        kb = Store('empty', namespaces=ns)
        self.assertEqual(kb._nsm.qname(
            'http://www.wikidata.org/entity/Q1'), 'wd:Q1')
        self.assertEqual(kb._nsm.qname('http://example.org/x'), 'ex:x')

    # -- Set interface -----------------------------------------------------

    def test__iter__(self):
        kb = Store('empty')
        self.assertRaises(StopIteration, next, iter(kb))

    def test__len__(self):
        kb = Store('empty')
        self.assertEqual(len(kb), 0)

    # -- Queries -----------------------------------------------------------

    def test_contains(self):
        kb = Store('empty')
        self.store_test_not_contains(
            kb,
            wd.instance_of(wd.benzene, wd.type_of_a_chemical_entity),
            # quantity
            wd.density(wd.benzene, Quantity('0.88')),
            wd.density(wd.benzene, Quantity(
                '0.88', wd.gram_per_cubic_centimetre)),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, None, '.89')),
            wd.density(wd.benzene, Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87', '.89')),
            # time
            wd.inception(wd.Brazil, Time('1822-09-07')),
            wd.inception(wd.Brazil, Time('1822-09-07', Time.Precision.DAY)),
            wd.inception(wd.Brazil, Time('1822-09-07', Time.DAY, 0)),
            wd.inception(wd.Brazil, Time(
                '1822-09-07', Time.DAY, 0, wd.proleptic_Gregorian_calendar)),
            # some value
            Statement(wd.Adam, SomeValueSnak(wd.family_name)),
            # no value
            Statement(wd.Adam, NoValueSnak(wd.date_of_birth)))

    def test_count(self):
        kb = Store('empty')
        self.store_test_count(kb, 0)
        self.store_test_count(kb, 0, snak_mask=SnakMask.VALUE_SNAK)
        self.store_test_count(kb, 0, wd.InChIKey)
        self.store_test_count(kb, 0, wd.Brazil)
        self.store_test_count(kb, 0, wd.benzene, wd.mass)
        self.store_test_count(kb, 0, None, wd.part_of, wd.Latin_America)

    def test_filter(self):
        kb = Store('empty')
        self.store_test_filter(kb, [], subject=wd.benzene)
        self.store_test_filter(kb, [], property=wd.mass)
        self.store_test_filter(kb, [], value=wd.Latin_America)

    # -- Annotations -------------------------------------------------------

    def test_get_annotations(self):
        kb = Store('empty')
        self.store_test_get_annotations(
            kb,
            [(Statement(wd.Adam, NoValueSnak(wd.date_of_birth)), None),
             (wd.date_of_birth(wd.Adam, Time(
                 '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)), None),
             (wd.inception(wd.Brazil, Time('1822-09-07')), None)],
            Statement(wd.Adam, NoValueSnak(wd.date_of_birth)),
            wd.date_of_birth(wd.Adam, Time(
                '4003-01-01', 9, 0, wd.proleptic_Julian_calendar)),
            wd.inception(wd.Brazil, Time('1822-09-07')))

    # -- Descriptor --------------------------------------------------------

    def test_get_descriptor(self):
        kb = Store('empty')
        self.store_test_get_descriptor(
            kb,
            [(wd.Brazil, Descriptor()),
             (wd.instance_of, Descriptor())],
            'en',
            wd.Brazil, wd.instance_of)


if __name__ == '__main__':
    main()
