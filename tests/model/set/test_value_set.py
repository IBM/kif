# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import decimal

from kif_lib import (
    Item,
    ItemTemplate,
    NoValueSnak,
    Property,
    Quantity,
    String,
    Text,
    TextSet,
    Time,
    Value,
    ValueSet,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import ClosedTermSetTestCase


class Test(ClosedTermSetTestCase):

    def test_children_class(self) -> None:
        assert_type(ValueSet.children_class, type[Value])
        self.assertIs(ValueSet.children_class, Value)

    def test_check(self) -> None:
        assert_type(ValueSet.check('x'), ValueSet)
        super()._test_check(
            ValueSet,
            success=[
                ([], ValueSet()),
                (('x', 'y', 0),
                 ValueSet(String('x'), String('y'), Quantity(0))),
                (['x', 'y', 0],
                 ValueSet(String('x'), String('y'), Quantity(0))),
                ({'x', 'y', 0},
                 ValueSet(String('x'), String('y'), Quantity(0))),
                (TextSet('x', 'y', 'z'),
                 TextSet(Text('x'), Text('y'), Text('z'))),
                (list(ValueSnak('x', 'y')),
                 ValueSet(Property('x', String), String('y'))),
                ('xyz',
                 ValueSet('x', 'y', 'z')),
                ({'x': 0, 'y': 1, 'z': 2},
                 ValueSet('x', 'y', 'z')),
            ],
            failure=[
                0,
                [Item(Variable('x'))],
                [Variable('x')],
            ])

    def test__init__(self) -> None:
        assert_type(ValueSet('x'), ValueSet)
        self._test__init__(
            ValueSet,
            self.assert_value_set,
            success=[
                ([Item('x'), 'y'], ValueSet(Item('x'), String('y'))),
                ([datetime.datetime(2024, 7, 2, tzinfo=datetime.timezone.utc),
                  decimal.Decimal('.77')],
                 ValueSet(Time('2024-07-02'), Quantity('.77'))),
            ],
            failure=[
                [ItemTemplate(Variable('x'))],
                [Variable('x', Text)],
                [Item('x'), NoValueSnak('x')],
            ])

    def test__contains__(self) -> None:
        self.assertNotIn(0, ValueSet())
        self.assertIn(Text('p'), ValueSet(Text('p')))
        self.assertNotIn(Text('p', 'pt'), ValueSet(Text('p')))

    def test_union(self) -> None:
        assert_type(ValueSet().union(), ValueSet)
        self.assert_value_set(ValueSet().union(ValueSet(), ValueSet()))
        self.assert_value_set(
            ValueSet('x').union(ValueSet('x', 'y'), ValueSet('z')),
            String('x'), String('y'), String('z'))
        s1 = ValueSet(Text('p'), Property('q'))
        s2 = ValueSet(Text('p'))
        s3 = ValueSet()
        s4 = ValueSet(Text('r'), Text('s'))
        self.assertEqual(
            s1.union(s2, s3, s4),
            ValueSet(Text('p'), Property('q'), Text('r'), Text('s')))


if __name__ == '__main__':
    Test.main()
