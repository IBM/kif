# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

from kif_lib import Time
from kif_lib.model import Datetime, UTC
from kif_lib.namespace import XSD
from kif_lib.vocabulary import wd

from .tests import kif_TestCase


class TestModelValueTime(kif_TestCase):

    def test__check_arg_precision(self):
        self.assertRaises(TypeError, Time._check_arg_precision, 'abc')
        self.assertRaises(ValueError, Time._check_arg_precision, 99)
        self.assertEqual(
            Time.Precision.DAY,
            Time._check_arg_precision(Time.Precision.DAY))

    def test__preprocess_arg_precision(self):
        self.assertEqual(
            Time.Precision.DAY,
            Time._preprocess_arg_precision(Time.Precision.DAY, 1))
        self.assertEqual(
            Time.Precision.DAY,
            Time._preprocess_arg_precision(11, 1))

    def test__preprocess_optional_arg_precision(self):
        self.assertEqual(
            Time.Precision.DAY,
            Time._preprocess_optional_arg_precision(
                None, 1, Time.Precision.DAY))
        self.assertEqual(
            Time.Precision.YEAR,
            Time._preprocess_optional_arg_precision(
                Time.Precision.YEAR, 1, Time.Precision.DAY))

    def test_precision_aliases(self):
        self.assertIs(
            Time.Precision.BILLION_YEARS,
            Time.BILLION_YEARS)
        self.assertIs(
            Time.Precision.HUNDRED_MILLION_YEARS,
            Time.HUNDRED_MILLION_YEARS)
        self.assertIs(
            Time.Precision.TEN_MILLION_YEARS,
            Time.TEN_MILLION_YEARS)
        self.assertIs(
            Time.Precision.MILLION_YEARS,
            Time.MILLION_YEARS)
        self.assertIs(
            Time.Precision.HUNDRED_THOUSAND_YEARS,
            Time.HUNDRED_THOUSAND_YEARS)
        self.assertIs(
            Time.Precision.TEN_THOUSAND_YEARS,
            Time.TEN_THOUSAND_YEARS)
        self.assertIs(
            Time.Precision.MILLENNIA,
            Time.MILLENNIA)
        self.assertIs(
            Time.Precision.CENTURY,
            Time.CENTURY)
        self.assertIs(
            Time.Precision.DECADE,
            Time.DECADE)
        self.assertIs(
            Time.Precision.YEAR,
            Time.YEAR)
        self.assertIs(
            Time.Precision.MONTH,
            Time.MONTH)
        self.assertIs(
            Time.Precision.DAY,
            Time.DAY)
        self.assertIs(
            Time.Precision.HOUR,
            Time.HOUR)
        self.assertIs(
            Time.Precision.MINUTE,
            Time.MINUTE)
        self.assertIs(
            Time.Precision.SECOND,
            Time.SECOND)

    def test__init__(self):
        self.assertRaises(TypeError, Time, [])
        self.assertRaises(ValueError, Time, 'abc')
        self.assertRaises(TypeError, Time, '2023-09-04', 'abc')
        self.assertRaises(ValueError, Time, '2023-09-04', -1)
        self.assertRaises(TypeError, Time, '2023-09-04', 1, 'abc')
        self.assertRaises(TypeError, Time, '2023-09-04', 1, 1, 0)
        self.assert_time(
            Time('2023-09-04'), Datetime(2023, 9, 4, tzinfo=UTC))
        self.assert_time(
            Time(Datetime(2023, 9, 4)), Datetime(2023, 9, 4))
        self.assert_time(
            Time('2023-09-04', 11),
            Datetime(2023, 9, 4, tzinfo=UTC), Time.Precision(11))
        self.assert_time(
            Time('2023-09-04', None, 44),
            Datetime(2023, 9, 4, tzinfo=UTC), None, 44)
        self.assert_time(
            Time('2023-09-04', None, None, wd.proleptic_Gregorian_calendar),
            Datetime(2023, 9, 4, tzinfo=UTC),
            None, None, wd.proleptic_Gregorian_calendar)

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
        self.assertRaises(TypeError, Time._from_rdflib, Literal('x'))
        # bad argument: ill-typed literal
        self.assertRaises(
            TypeError, Time._from_rdflib, Literal(
                '1.0', datatype=XSD.decimal))
        # good arguments
        t = Literal('2023-10-03T00:00:00', datatype=XSD.dateTime)
        self.assert_time(
            Time._from_rdflib(t), Datetime(2023, 10, 3, tzinfo=UTC))
        t = Literal('2023-10-03', datatype=XSD.date)
        self.assert_time(
            Time._from_rdflib(t), Datetime(2023, 10, 3, tzinfo=UTC))
        t = Literal('2023-10-03T11:11:11', datatype=XSD.dateTime)
        self.assert_time(
            Time._from_rdflib(t),
            Datetime(2023, 10, 3, 11, 11, 11, tzinfo=UTC))

    def test__to_rdflib(self):
        self.assertEqual(
            Time('2023-10-03')._to_rdflib(),
            Literal('2023-10-03T00:00:00+00:00', datatype=XSD.dateTime))


if __name__ == '__main__':
    TestModelValueTime.main()
