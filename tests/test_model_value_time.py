# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime

from kif_lib import Item, Time
from kif_lib.namespace import XSD
from kif_lib.rdflib import Literal, URIRef
from kif_lib.vocabulary import wd

from .tests import kif_TestCase


class TestModelValueTime(kif_TestCase):

    def test__init__(self):
        dt = datetime.datetime(2023, 9, 4, tzinfo=datetime.timezone.utc)
        self.assertRaises(TypeError, Time, [])
        self.assertRaises(ValueError, Time, 'abc')
        self.assertRaises(TypeError, Time, '2023-09-04', 'abc')
        self.assertRaises(TypeError, Time, '2023-09-04', -1)
        self.assertRaises(ValueError, Time, '2023-09-04', 1, 'abc')
        self.assertRaises(TypeError, Time, '2023-09-04', 1, 1, 0)
        self.assert_time(Time('2023-09-04'), dt)
        self.assert_time(
            Time(datetime.datetime(2023, 9, 4)),
            datetime.datetime(2023, 9, 4))
        self.assert_time(
            Time('2023-09-04', 11), dt, Time.Precision(11))
        self.assert_time(
            Time('2023-09-04', None, 44), dt, None, 44)
        self.assert_time(
            Time('2023-09-04', None, None, Item('x')),
            dt, None, None, Item('x'))

    def test_get_precision(self):
        self.assertEqual(
            Time('2023-09-04', 11).get_precision(), Time.Precision.DAY)
        self.assertEqual(
            Time('2023-09-04').get_precision(Time.Precision.DAY),
            Time.Precision.DAY)
        self.assertIsNone(Time('2023-09-04').get_precision())

    def test_get_timezone(self):
        self.assertEqual(Time('2023-09-04', None, 1).get_timezone(), 1)
        self.assertEqual(Time('2023-09-04').get_timezone(1), 1)
        self.assertIsNone(Time('2023-09-04').get_timezone())

    def test_get_calendar(self):
        self.assertEqual(Time(
            '2023-09-04', 11, None,
            wd.proleptic_Gregorian_calendar).get_calendar(),
            wd.proleptic_Gregorian_calendar)
        self.assertIsNone(Time('2023-09-04').get_calendar())

    def test__from_rdflib(self):
        # bad argument: uri
        self.assertRaises(TypeError, Time._from_rdflib, URIRef('x'))
        # bad argument: untyped literal
        self.assertRaises(ValueError, Time._from_rdflib, Literal('x'))
        # bad argument: ill-typed literal
        self.assertRaises(
            TypeError, Time._from_rdflib, Literal(
                '1.0', datatype=XSD.decimal))
        # good arguments
        t = Literal('2023-10-03T00:00:00', datatype=XSD.dateTime)
        dt = datetime.datetime(2023, 10, 3, tzinfo=datetime.timezone.utc)
        self.assert_time(Time._from_rdflib(t), dt)
        t = Literal('2023-10-03', datatype=XSD.date)
        self.assert_time(Time._from_rdflib(t), dt)
        t = Literal('2023-10-03T11:11:11', datatype=XSD.dateTime)
        self.assert_time(
            Time._from_rdflib(t),
            datetime.datetime(
                2023, 10, 3, 11, 11, 11,
                tzinfo=datetime.timezone.utc))

    def test__to_rdflib(self):
        self.assertEqual(
            Time('2023-10-03')._to_rdflib(),
            Literal('2023-10-03T00:00:00+00:00', datatype=XSD.dateTime))


if __name__ == '__main__':
    TestModelValueTime.main()
