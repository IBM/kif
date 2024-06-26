# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    Property,
    Quantity,
    String,
    StringDatatype,
    Text,
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
)
from kif_lib.typing import assert_type

from ...tests import kif_DeepDataValueTestCase


class Test(kif_DeepDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Time.datatype_class, type[TimeDatatype])

    def test_datatype(self) -> None:
        assert_type(Time.datatype, TimeDatatype)
        self.assertIsInstance(String.datatype, StringDatatype)

    def test_template_class(self) -> None:
        assert_type(Time.template_class, type[TimeTemplate])

    def test_variable_class(self) -> None:
        assert_type(Time.variable_class, type[TimeVariable])

    def test_check(self) -> None:
        assert_type(Time.check(datetime.datetime(2024, 6, 26)), Time)
        self._test_check(
            Time,
            success=[
                ('2024-06-26', Time('2024-06-26')),
                (datetime.date(2024, 6, 26), Time('2024-06-26')),
                (datetime.datetime(2024, 6, 26,
                 tzinfo=datetime.timezone.utc), Time('2024-06-26')),
                (String('2024-06-26'), Time('2024-06-26')),
                (Time('2024-06-26'), Time('2024-06-26')),
            ],
            failure=[
                'x',
                ExternalId('x'),
                IRI('x'),
                Item('x'),
                Quantity(0),
                String('x'),
                Text('x'),
            ])

    def test__init__(self) -> None:
        assert_type(Time('2024-06-26'), Time)
        dt = datetime.datetime.fromisoformat('2024-06-26').replace(
            tzinfo=datetime.timezone.utc)
        self._test__init__(
            Time,
            self.assert_time,
            success=[
                ((dt, 0), Time('2024-06-26', 0)),
                ((dt, 11), Time(dt, Time.DAY)),
                ((dt, None, 0), Time(dt, None, 0)),
                ((dt, None, None, Item('x')),
                 Time('2024-06-26', None, None, Item('x'))),
                ((dt,), Time('2024-06-26')),
                ((Time(dt),), Time('2024-06-26')),
            ],
            failure=[
                (0,),
                (dt, -1),
                (dt, None, None, Property('x')),
                (dt, None, None, {}),
                (dt, None, Property('x'), {}),
                (dt, None, {}),
                ({},),
            ])

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
        self.assertEqual(
            Time('2023-09-04', 11, None, Item('x')).get_calendar(), Item('x'))
        self.assertEqual(
            Time('2023-09-04').get_calendar(Item('x')), Item('x'))
        self.assertIsNone(Time('2023-09-04').get_calendar())


if __name__ == '__main__':
    Test.main()
