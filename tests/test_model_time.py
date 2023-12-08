# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

import kif.namespace as NS
import kif.vocabulary as wd
from kif import Time
from kif.model import Datetime

from .tests import kif_TestCase, main


class TestModelTime(kif_TestCase):

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
        self.assertIs(Time.Precision.BILLION_YEARS, Time.BILLION_YEARS)
        self.assertIs(Time.HUNDRED_MILLION_YEARS, Time.HUNDRED_MILLION_YEARS)
        self.assertIs(Time.TEN_MILLION_YEARS, Time.TEN_MILLION_YEARS)
        self.assertIs(Time.MILLION_YEARS, Time.MILLION_YEARS)
        self.assertIs(
            Time.HUNDRED_THOUSAND_YEARS, Time.HUNDRED_THOUSAND_YEARS)
        self.assertIs(Time.TEN_THOUSAND_YEARS, Time.TEN_THOUSAND_YEARS)
        self.assertIs(Time.MILLENIA, Time.MILLENIA)
        self.assertIs(Time.CENTURY, Time.CENTURY)
        self.assertIs(Time.DECADE, Time.DECADE)
        self.assertIs(Time.YEAR, Time.YEAR)
        self.assertIs(Time.MONTH, Time.MONTH)
        self.assertIs(Time.DAY, Time.DAY)
        self.assertIs(Time.HOUR, Time.HOUR)
        self.assertIs(Time.MINUTE, Time.MINUTE)
        self.assertIs(Time.SECOND, Time.SECOND)

    def test__init__(self):
        self.assertRaises(TypeError, Time, [])
        self.assertRaises(ValueError, Time, 'abc')
        self.assertRaises(TypeError, Time, '2023-09-04', 'abc')
        self.assertRaises(ValueError, Time, '2023-09-04', -1)
        self.assertRaises(TypeError, Time, '2023-09-04', 1, 'abc')
        self.assertRaises(TypeError, Time, '2023-09-04', 1, 1, 0)
        self.assert_time(Time('2023-09-04'), Datetime(2023, 9, 4))
        self.assert_time(Time(Datetime(2023, 9, 4)), Datetime(2023, 9, 4))
        self.assert_time(
            Time('2023-09-04', 11), Datetime(2023, 9, 4), Time.Precision(11))
        self.assert_time(
            Time('2023-09-04', None, 44), Datetime(2023, 9, 4), None, 44)
        self.assert_time(
            Time('2023-09-04', None, None, wd.proleptic_Gregorian_calendar),
            Datetime(2023, 9, 4), None, None, wd.proleptic_Gregorian_calendar)

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

    def test_get_calendar_model(self):
        self.assertEqual(Time(
            '2023-09-04', 11, None,
            wd.proleptic_Gregorian_calendar).get_calendar_model(),
            wd.proleptic_Gregorian_calendar)
        self.assertIsNone(Time('2023-09-04').get_calendar_model())

    def test__from_rdflib(self):
        # bad argument: uri
        self.assertRaises(TypeError, Time._from_rdflib, URIRef('x'))
        # bad argument: untyped literal
        self.assertRaises(TypeError, Time._from_rdflib, Literal('x'))
        # bad argument: ill-typed literal
        self.assertRaises(
            TypeError, Time._from_rdflib, Literal(
                '1.0', datatype=NS.XSD.decimal))
        # good arguments
        t = Literal('2023-10-03T00:00:00', datatype=NS.XSD.dateTime)
        self.assert_time(
            Time._from_rdflib(t), Datetime(2023, 10, 3))
        t = Literal('2023-10-03', datatype=NS.XSD.date)
        self.assert_time(
            Time._from_rdflib(t), Datetime(2023, 10, 3))
        t = Literal('2023-10-03T11:11:11', datatype=NS.XSD.dateTime)
        self.assert_time(
            Time._from_rdflib(t), Datetime(2023, 10, 3, 11, 11, 11))

    def test__to_rdflib(self):
        self.assertEqual(
            Time('2023-10-03')._to_rdflib(),
            Literal('2023-10-03T00:00:00+00:00', datatype=NS.XSD.dateTime))


if __name__ == '__main__':
    main()
