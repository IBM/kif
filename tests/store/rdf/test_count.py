# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Quantity, Store, Text, Time
from kif_lib.vocabulary import wd

from ...tests import TestCase


class Test(TestCase):

    KB = Store(
        'rdf',
        'tests/data/adam.ttl',
        'tests/data/andar.ttl',
        'tests/data/benzene.ttl',
        'tests/data/brazil.ttl',
    )

    def test_empty(self) -> None:
        self.assertEqual(self.KB.count(snak_mask=Filter.SnakMask(0)), 0)

    def test_full(self) -> None:
        self.assertEqual(self.KB.count(), 43)

    # -- masks --

    def test_snak_mask(self) -> None:
        self.assertEqual(self.KB.count(snak_mask=Filter.VALUE_SNAK), 40)
        self.assertEqual(self.KB.count(snak_mask=Filter.SOME_VALUE_SNAK), 1)
        self.assertEqual(self.KB.count(snak_mask=Filter.NO_VALUE_SNAK), 2)

    def test_subject_mask(self) -> None:
        self.assertEqual(self.KB.count(subject_mask=Filter.PROPERTY), 6)

    def test_property_mask(self) -> None:
        pass

    def test_value_mask(self) -> None:
        self.assertEqual(self.KB.count(value_mask=Filter.TEXT), 32)
        self.assertEqual(self.KB.count(
            value_mask=Filter.IRI,
            snak_mask=Filter.VALUE_SNAK), 0)

    def test_language(self) -> None:
        self.assertEqual(self.KB.count(
            value_mask=Filter.TEXT,
            language='pt',
            snak_mask=Filter.VALUE_SNAK), 2)

    # -- fingerprints --

    def test_value_fp_subject(self) -> None:
        self.assertEqual(self.KB.count(subject=wd.Brazil), 10)
        self.assertEqual(self.KB.count(subject=wd.InChIKey), 6)
        self.assertEqual(self.KB.count(subject=wd.L(46803)), 3)

    def test_value_fp_property(self) -> None:
        self.assertEqual(self.KB.count(
            subject=wd.Brazil, property=wd.label), 2)
        self.assertEqual(self.KB.count(
            subject=wd.benzene, property=wd.mass), 1)

    def test_value_fp_value_text(self) -> None:
        self.assertEqual(self.KB.count(
            value=Text('Brazil', 'en')), 1)

    def test_value_fp_value_quantity(self) -> None:
        self.assertEqual(self.KB.count(
            subject=wd.benzene,
            property=wd.mass,
            value=Quantity('78.046950192')), 1)
        self.assertEqual(self.KB.count(
            property=wd.mass,
            value=Quantity('78.046950192')), 1)
        self.assertEqual(self.KB.count(value=Quantity('78.046950192')), 1)
        self.assertEqual(self.KB.count(
            value=Quantity('78.046950192', wd.dalton)), 1)
        self.assertEqual(self.KB.count(
            value=Quantity('78.046950192', wd.kilogram)), 0)
        self.assertEqual(self.KB.count(
            property=wd.density,
            value=Quantity('.88', wd.gram_per_cubic_centimetre)), 1)
        self.assertEqual(self.KB.count(
            property=wd.density,
            value=Quantity('.88', wd.gram_per_cubic_centimetre, '.87')), 1)
        self.assertEqual(self.KB.count(
            property=wd.density,
            value=Quantity('.88', wd.gram_per_cubic_centimetre, '.88')), 0)
        self.assertEqual(self.KB.count(
            property=wd.density,
            value=Quantity(
                '.88', wd.gram_per_cubic_centimetre, None, '.89')), 1)
        self.assertEqual(self.KB.count(
            property=wd.density,
            value=Quantity(
                '.88', wd.gram_per_cubic_centimetre, '.87', '.89')), 1)

    def test_value_fp_value_time(self) -> None:
        self.assertEqual(self.KB.count(value=Time('1822-09-07')), 1)
        self.assertEqual(self.KB.count(value=Time('1822-09-08')), 0)
        self.assertEqual(self.KB.count(
            property=wd.inception, value=Time('1822-09-07')), 1)
        self.assertEqual(self.KB.count(
            value=Time('1822-09-07', Time.DAY)), 1)
        self.assertEqual(self.KB.count(
            value=Time('1822-09-07', Time.YEAR)), 0)
        self.assertEqual(self.KB.count(
            value=Time('1822-09-07', None, 0)), 1)
        self.assertEqual(self.KB.count(
            value=Time('1822-09-07', None, 9)), 0)
        self.assertEqual(self.KB.count(
            value=Time(
                '1822-09-07', None, None,
                wd.proleptic_Gregorian_calendar)), 1)
        self.assertEqual(self.KB.count(
            value=Time(
                '1822-09-07', None, None,
                wd.proleptic_Julian_calendar)), 0)
        self.assertEqual(self.KB.count(
            value=Time(
                '1822-09-07', Time.DAY, 0,
                wd.proleptic_Gregorian_calendar)), 1)

    def test_snak_fp_subject(self) -> None:
        self.assertEqual(self.KB.count(
            subject=wd.instance_of(wd.type_of_a_chemical_entity),
            property=wd.density), 1)

    def test_snak_fp_property(self) -> None:
        self.assertEqual(self.KB.count(
            subject=wd.benzene,
            property=wd.related_property(wd.InChI)), 1)

    def test_snak_fp_value(self) -> None:
        self.assertEqual(self.KB.count(
            subject=wd.Brazil,
            value=wd.demonym(Text('Latinoamericana', 'es'))), 1)

    def test_or_fp_subject_property(self) -> None:
        self.assertEqual(self.KB.count(
            subject=wd.Brazil | wd.benzene, property=wd.label | wd.mass), 4)


if __name__ == '__main__':
    Test.main()
