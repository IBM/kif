# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from kif_lib import (
    DataValue,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    Quantity,
    QuantityTemplate,
    QuantityVariable,
    String,
    Term,
    Time,
    TimeTemplate,
    TimeVariable,
    Variable,
)
from kif_lib.typing import assert_type, cast

from ...tests import DeepDataValueTemplateTestCase


class Test(DeepDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(TimeTemplate.object_class, type[Time])
        self.assertIs(TimeTemplate.object_class, Time)

    def test_check(self) -> None:
        assert_type(
            TimeTemplate.check(TimeTemplate(Variable('x'))),
            TimeTemplate)
        self._test_check(TimeTemplate, failure=[Time('2024-06-26')])

    def test__init__(self) -> None:
        assert_type(TimeTemplate(Variable('x')), TimeTemplate)
        dt = datetime.datetime(2024, 6, 26).replace(
            tzinfo=datetime.timezone.utc)
        self._test__init__(
            TimeTemplate,
            self.assert_time_template,
            success=[
                ([Variable('x')], TimeTemplate(TimeVariable('x'))),
                (['2024-06-26', Variable('y')],
                 Time('2024-06-26', QuantityVariable('y'))),
                ([dt, None, None, Item(Variable('y'))],
                 Time(dt, None, None, ItemTemplate(Variable('y', IRI)))),
                ([dt, None, None, Item(IRI(Variable('y')))],
                 Time(dt, None, None, ItemTemplate(
                     IRI(Variable('y', String))))),
                ([dt, None, Variable('x')],
                 Time(dt, None, QuantityVariable('x'))),
                ([dt, None, Quantity(1, Item('x')), Variable('x')],
                 Time(dt, None, 1, ItemVariable('x'))),
                ([Variable('x'), Variable('y'), Variable('z'), Variable('w')],
                 Time(
                     TimeVariable('x'),
                     QuantityVariable('y'),
                     QuantityVariable('z'),
                     ItemVariable('w'))),
                ([Variable('x', Time), None, None, None],
                 Time(Variable('x'))),
                ([Variable('x'), decimal.Decimal('1'),
                  0, Item(Variable('y', IRI))],
                 Time(Variable('x'), 1, 0, Item(Variable('y')))),
            ],
            failure=[
                [dt, None, None, Time(Variable('x'))],
                [dt, None, Time(Variable('x'))],
                [ItemVariable('x')],
                [None, None, ItemVariable('x')],
                [None, None, None, Item(IRI(Variable('x')))],
                [None, Variable('x', IRI)],
                [Time('2024-06-26', Variable('x'))],
                [Time(Variable('x'))],
            ],
            normalize=[
                ['2024-06-26', None, 1, Item('x')],
                [dt, None, 1],
                [dt, None, None, Item('x')],
                [dt, None, None, Item('x')],
                [dt, None, None, None],
                [dt],
            ])

        # extra
        x = Variable('x')
        self.assert_raises_bad_argument(
            ValueError, 1, None, 'cannot coerce str into Time',
            (TimeTemplate, 'Time'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce str into Time.Precision',
            (TimeTemplate, 'Time'), '2024-05-06', 'x')
        self.assert_raises_bad_argument(
            ValueError, 3, None,
            'cannot coerce str into Quantity',
            (TimeTemplate, 'Time'), '2024-05-06', None, 'x')
        self.assert_raises_bad_argument(
            TypeError, 4, None, 'cannot coerce int into IRI',
            (TimeTemplate, 'Time'), '2024-05-06', None, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into TimeVariable",
            TimeTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce TimeTemplate into Time',
            TimeTemplate, TimeTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            TimeTemplate, '2024-05-06', IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce QuantityTemplate into Quantity',
            TimeTemplate, Variable('t', Time),
            QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            TimeTemplate, '2024-05-06', None, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'cannot coerce QuantityTemplate into Quantity',
            TimeTemplate, Variable('t', Time), None,
            QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            "cannot coerce IRI_Variable into ItemVariable",
            TimeTemplate, '2024-05-06', None, None, IRI_Variable('x'))
        self.assert_time_template(
            TimeTemplate(x),
            TimeVariable('x'),
            None, None, None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', Variable('x')),
            Time('2024-05-06').time,
            QuantityVariable('x'), None, None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', None, Variable('x')),
            Time('2024-05-06').time,
            None, QuantityVariable('x'), None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', None, None, x),
            Time('2024-05-06').time,
            None, None, ItemVariable('x'))
        self.assert_time_template(
            TimeTemplate(
                Variable('x'),
                Variable('y'),
                Variable('z'),
                Variable('w')),
            TimeVariable('x'),
            QuantityVariable('y'),
            QuantityVariable('z'),
            ItemVariable('w'))
        self.assert_time_template(
            Time(x), Variable('x', Time), None, None, None)
        self.assert_time_template(
            Time('2024-05-06', x),
            Time('2024-05-06').time,
            Variable('x', Quantity), None, None)
        self.assert_time_template(
            Time('2024-05-06', None, x),
            Time('2024-05-06').time,
            None, Variable('x', Quantity), None)
        self.assert_time_template(
            Time('2024-05-06', None, None, x),
            Time('2024-05-06').time,
            None, None, Variable('x', Item))
        self.assert_time_template(
            Time('2024-05-06', None, None, Item(IRI(x))),
            Time('2024-05-06').time, None, None,
            Item(IRI(Variable('x'))))
        self.assert_time(
            cast(Time, TimeTemplate('2024-05-06', None, None, None)),
            Time('2024-05-06').time, None, None, None)
        self.assertRaises(TypeError, TimeTemplate, x, x)
        self.assertRaises(
            TypeError, Time, '2024-05-06', x, x, x)
        self.assert_time_template(
            TimeTemplate('2024-05-06', x, x),
            Time('2024-05-06').time,
            QuantityVariable('x'), QuantityVariable('x'), None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', x, Variable('x', DataValue)),
            Time('2024-05-06').time,
            QuantityVariable('x'), QuantityVariable('x'), None)

    def test_instantiate(self) -> None:
        assert_type(
            TimeTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            TimeTemplate,
            success=[
                (TimeTemplate(Variable('x')),
                 Time('2024-06-26'),
                 {TimeVariable('x'): Time('2024-06-26')}),
                (Time('2024-06-26', None, 1, Variable('x')),
                 Time('2024-06-26', None, 1, Item(Variable('x', IRI))),
                 {ItemVariable('x'): Item(Variable('x'))}),
                (Time('2024-06-26', None, Variable('x')),
                 Time('2024-06-26', None, 8),
                 {QuantityVariable('x'): Quantity(8, Item('x'))}),
                (Time(Variable('x'), Variable('y'), Variable('y'), None),
                 Time(TimeVariable('z'), 8, 8),
                 {TimeVariable('x'): TimeVariable('z'),
                  QuantityVariable('y'): Quantity(8, Item('w'))}),
            ],
            failure=[
                (Time(Variable('x')),
                 {TimeVariable('x'): Item('y')}),
            ])


if __name__ == '__main__':
    Test.main()
