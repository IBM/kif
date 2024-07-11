# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    Property,
    Quantity,
    SomeValueSnak,
    String,
    Text,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_SnakTestCase


class Test(kif_SnakTestCase):

    def test_template_class(self) -> None:
        assert_type(NoValueSnak.template_class, type[NoValueSnakTemplate])
        self.assertIs(NoValueSnak.template_class, NoValueSnakTemplate)

    def test_variable_class(self) -> None:
        assert_type(NoValueSnak.variable_class, type[NoValueSnakVariable])
        self.assertIs(NoValueSnak.variable_class, NoValueSnakVariable)

    def test_check(self) -> None:
        assert_type(NoValueSnak.check(NoValueSnak('x')), NoValueSnak)
        self._test_check(
            NoValueSnak,
            success=[
                ('x', NoValueSnak(Property('x'))),
                (ExternalId('x'), NoValueSnak('x')),
                (IRI('x'), NoValueSnak('x')),
                (NoValueSnak('x'), NoValueSnak('x')),
                (Property('x', Item), NoValueSnak(Property('x', Item))),
                (String('x'), NoValueSnak('x')),
            ],
            failure=[
                0,
                Item('x'),
                ItemTemplate(Variable('x')),
                Quantity(0),
                SomeValueSnak(Property('x')),
                Text('x'),
                ValueSnak('x', 'y'),
                Variable('x', Text),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(NoValueSnak('x'), NoValueSnak)
        self._test__init__(
            NoValueSnak,
            self.assert_no_value_snak,
            success=[
                (['x'], NoValueSnak('x')),
                ([ExternalId('x')], NoValueSnak('x')),
                ([IRI('x')], NoValueSnak('x')),
                ([Property('x')], NoValueSnak('x')),
                ([String('x')], NoValueSnak('x')),
            ],
            failure=[
                [0],
                [Item('x')],
                [NoValueSnak('x')],
                [Quantity(0)],
                [SomeValueSnak('x')],
                [String(Variable('x'))],
                [Text('x')],
                [ValueSnak('x', 'y')],
                [Variable('x', Item)],
                [{}],
            ])


if __name__ == '__main__':
    Test.main()
