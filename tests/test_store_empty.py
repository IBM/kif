# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Filter,
    NoValueSnak,
    Quantity,
    SomeValueSnak,
    Statement,
    Time,
)
from kif_lib.vocabulary import wd

from .tests import EmptyStoreTestCase


class TestStoreEmpty(EmptyStoreTestCase):

    def test_sanity(self) -> None:
        self.store_sanity_checks(self.new_Store())

    def test__init__(self) -> None:
        from kif_lib.store import EmptyStore
        kb = self.new_Store()
        self.assertIsInstance(kb, EmptyStore)

    def test__iter__(self) -> None:
        kb = self.new_Store()
        self.assertRaises(StopIteration, next, iter(kb))

    def test__len__(self) -> None:
        kb = self.new_Store()
        self.assertEqual(len(kb), 0)

    def test_contains(self) -> None:
        kb = self.new_Store()
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

    def test_count(self) -> None:
        kb = self.new_Store()
        self.store_test_count(kb, 0)
        self.store_test_count(kb, 0, snak_mask=Filter.VALUE_SNAK)
        self.store_test_count(kb, 0, wd.InChIKey)
        self.store_test_count(kb, 0, wd.Brazil)
        self.store_test_count(kb, 0, wd.benzene, wd.mass)
        self.store_test_count(kb, 0, None, wd.part_of, wd.Latin_America)

    def test_filter(self) -> None:
        kb = self.new_Store()
        self.store_test_filter(kb, [], subject=wd.benzene)
        self.store_test_filter(kb, [], property=wd.mass)
        self.store_test_filter(kb, [], value=wd.Latin_America)

    def test_get_annotations(self) -> None:
        kb = self.new_Store()
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


if __name__ == '__main__':
    TestStoreEmpty.main()
