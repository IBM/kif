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
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    String,
    Text,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_SnakTestCase


class Test(kif_SnakTestCase):

    def test_template_class(self) -> None:
        assert_type(SomeValueSnak.template_class, type[SomeValueSnakTemplate])
        self.assertIs(SomeValueSnak.template_class, SomeValueSnakTemplate)

    def test_variable_class(self) -> None:
        assert_type(SomeValueSnak.variable_class, type[SomeValueSnakVariable])
        self.assertIs(SomeValueSnak.variable_class, SomeValueSnakVariable)

    def test_check(self) -> None:
        assert_type(SomeValueSnak.check(SomeValueSnak('x')), SomeValueSnak)
        self._test_check(
            SomeValueSnak,
            success=[
                ('x', SomeValueSnak(Property('x'))),
                (ExternalId('x'), SomeValueSnak('x')),
                (IRI('x'), SomeValueSnak('x')),
                (SomeValueSnak('x'), SomeValueSnak('x')),
                (Property('x', Item), SomeValueSnak(Property('x', Item))),
                (String('x'), SomeValueSnak('x')),
            ],
            failure=[
                0,
                Item('x'),
                ItemTemplate(Variable('x')),
                NoValueSnak('x'),
                Quantity(0),
                Text('x'),
                ValueSnak(Property('x'), 'x'),
                Variable('x', Text),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(SomeValueSnak('x'), SomeValueSnak)
        self._test__init__(
            SomeValueSnak,
            self.assert_some_value_snak,
            success=[
                (['x'], SomeValueSnak('x')),
                ([ExternalId('x')], SomeValueSnak('x')),
                ([IRI('x')], SomeValueSnak('x')),
                ([Property('x')], SomeValueSnak('x')),
                ([String('x')], SomeValueSnak('x')),
            ],
            failure=[
                [0],
                [Item('x')],
                [NoValueSnak('x')],
                [Quantity(0)],
                [SomeValueSnak('x')],
                [String(Variable('x'))],
                [Text('x')],
                [ValueSnak('x', 'x')],
                [Variable('x', Item)],
                [{}],
            ])


if __name__ == '__main__':
    Test.main()
