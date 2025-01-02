# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    Property,
    Quantity,
    String,
    StringVariable,
    Term,
    Text,
    Theta,
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import DeepDataValueTestCase


class Test(DeepDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Time.datatype_class, type[TimeDatatype])
        self.assertIs(Time.datatype_class, TimeDatatype)

    def test_datatype(self) -> None:
        assert_type(Time.datatype, TimeDatatype)
        self.assert_time_datatype(Time.datatype)

    def test_template_class(self) -> None:
        assert_type(Time.template_class, type[TimeTemplate])
        self.assertIs(Time.template_class, TimeTemplate)

    def test_variable_class(self) -> None:
        assert_type(Time.variable_class, type[TimeVariable])
        self.assertIs(Time.variable_class, TimeVariable)

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
                ('2024-06-26T00:00:00+10:00',
                 Time(datetime.datetime(
                     2024, 6, 26, 0, 0, 0,
                     tzinfo=datetime.timezone(
                         datetime.timedelta(seconds=36000))))),
            ],
            failure=[
                IRI('x'),
                Item('x'),
                Quantity(0),
                Text('x'),
            ],
            failure_value_error=[
                'x',
                ExternalId('x'),
                String('x'),
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

    def test_get_precision(self) -> None:
        assert_type(Time('2024-08-22').precision, Optional[Time.Precision])
        assert_type(
            Time('2024-08-22').get_precision(), Optional[Time.Precision])
        self.assertEqual(
            Time('2023-09-04', 11).get_precision(), Time.Precision.DAY)
        self.assertEqual(
            Time('2023-09-04').get_precision(Time.Precision.DAY),
            Time.Precision.DAY)
        self.assertIsNone(Time('2023-09-04').get_precision())

    def test_get_timezone(self) -> None:
        assert_type(Time('2024-08-22').timezone, Optional[int])
        assert_type(Time('2024-08-22').get_timezone(), Optional[int])
        self.assertEqual(Time('2023-09-04', None, 1).get_timezone(), 1)
        self.assertEqual(Time('2023-09-04').get_timezone(1), 1)
        self.assertIsNone(Time('2023-09-04').get_timezone())

    def test_get_calendar(self) -> None:
        assert_type(Time('2024-08-22').calendar, Optional[Item])
        assert_type(Time('2024-08-22').get_calendar(), Optional[Item])
        self.assertEqual(
            Time('2023-09-04', 11, None, Item('x')).get_calendar(), Item('x'))
        self.assertEqual(
            Time('2023-09-04').get_calendar(Item('x')), Item('x'))
        self.assertIsNone(Time('2023-09-04').get_calendar())

    def test_variables(self) -> None:
        assert_type(Time('2024-09-05').variables, Set[Variable])
        self._test_variables(
            Time,
            (Time('2024-09-05'), set()),
            (Time('2024-09-05', 0), set()),
            (Time('2024-09-05', 0, 0), set()),
            (Time('2024-09-05', 0, 0, 'x'), set()))

    def test_instantiate(self) -> None:
        assert_type(Time('2024-09-05').instantiate({}), Term)
        self._test_instantiate(
            Time,
            success=[
                (Time('2024-09-05'), Time('2024-09-05'),
                 {Variable('x'): String('y')}),
            ])

    def test_match(self) -> None:
        assert_type(Time('2024-09-10').match(Variable('x')), Optional[Theta])
        self._test_match(
            Time,
            success=[
                (Time('2024-09-10'), Time('2024-09-10'), {}),
                (Time('2024-09-10'), TimeVariable('x'),
                 {TimeVariable('x'): Time('2024-09-10')}),
                (Time('2024-09-10'), Time(Variable('x')),
                 {TimeVariable('x'): Time('2024-09-10')}),
            ],
            failure=[
                (Time('2024-09-10'), StringVariable('y')),
                (Time('2024-09-10'), Time(Variable('x'), 0)),
                (Time('2024-09-10', 0, 0), Time(Variable('x'), 0, 1)),
            ])


if __name__ == '__main__':
    Test.main()
