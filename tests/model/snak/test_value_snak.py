# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    Property,
    Quantity,
    SomeValueSnak,
    String,
    Text,
    Time,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_SnakTestCase


class Test(kif_SnakTestCase):

    def test_template_class(self) -> None:
        assert_type(ValueSnak.template_class, type[ValueSnakTemplate])
        self.assertIs(ValueSnak.template_class, ValueSnakTemplate)

    def test_variable_class(self) -> None:
        assert_type(ValueSnak.variable_class, type[ValueSnakVariable])
        self.assertIs(ValueSnak.variable_class, ValueSnakVariable)

    def test_check(self) -> None:
        assert_type(ValueSnak.check(ValueSnak('x', 'y')), ValueSnak)
        self._test_check(
            ValueSnak,
            success=[
                (('x', 'y'), ValueSnak(Property('x'), String('y'))),
                (('x', ExternalId('y')), ValueSnak('x', ExternalId('y'))),
                ((IRI('x'), IRI('y')), ValueSnak('x', IRI('y'))),
                (ValueSnak('x', 'y'), ValueSnak('x', 'y')),
                ((Property('x', Quantity), Quantity(0)),
                 ValueSnak(Property('x', Quantity), Quantity(0))),
                ((String('x'), Time('2024-06-30')),
                 ValueSnak('x', Time('2024-06-30'))),
            ],
            failure=[
                (0, 'x'),
                (Item('x'), 'x'),
                0,
                Item('x'),
                ItemTemplate(Variable('x')),
                NoValueSnak('x'),
                Quantity(0),
                SomeValueSnak(Property('x')),
                Text('x'),
                Variable('x', Text),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(ValueSnak('x', 'y'), ValueSnak)
        self._test__init__(
            ValueSnak,
            self.assert_value_snak,
            success=[
                (['x', 'y'], ValueSnak('x', 'y')),
                (['x', 0], ValueSnak('x', Quantity(0))),
                (['x', ExternalId('y')], ValueSnak('x', ExternalId('y'))),
                (['x', Property('y')], ValueSnak('x', Property('y'))),
                ([IRI('x'), IRI('y')], ValueSnak('x', IRI('y'))),
                ([Property('x', Quantity), 0],
                 ValueSnak(Property('x', Quantity), Quantity(0))),
                ([Property('x', Quantity), Quantity(0)],
                 ValueSnak('x', Quantity(0))),
                ([String('x'), Time('2024-06-30')],
                 ValueSnak('x', Time('2024-06-30'))),
            ],
            failure=[
                [0, 'x'],
                [0, 0],
                [Item('x'), 'x'],
                [NoValueSnak('x'), NoValueSnak('y')],
                [Quantity(0), Property('x')],
                [SomeValueSnak('x'), SomeValueSnak('y')],
                [String(Variable('x')), Property('y')],
                [Text('x'), 'x'],
                [ValueSnak('x', 'x'), 'y'],
                [Variable('x', Item), Variable('y')],
                [{}, 'y'],
            ],
            failure_value_error=[
                [Property('x', ExternalId), String('y')],
                [Property('x', IRI), Item('x')],
                [Property('x', Item), Quantity(0)],
                [Property('x', Property), IRI('x')],
                [Property('x', String), ExternalId('y')],
            ])


if __name__ == '__main__':
    Test.main()
