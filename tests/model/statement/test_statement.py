# Copyright (C) 2024 IBM Corp.
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
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    Text,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_StatementTestCase


class Test(kif_StatementTestCase):

    def test_template_class(self) -> None:
        assert_type(Statement.template_class, type[StatementTemplate])
        self.assertIs(Statement.template_class, StatementTemplate)

    def test_variable_class(self) -> None:
        assert_type(Statement.variable_class, type[StatementVariable])
        self.assertIs(Statement.variable_class, StatementVariable)

    def test_check(self) -> None:
        assert_type(Statement.check((Item('x'), 'y', 'z')), Statement)
        self._test_check(
            Statement,
            success=[
                ((Item('x'), 'y', 'z'),
                 Statement(Item('x'), ValueSnak(Property('y'), String('z')))),
                ((Item('x'), ('y', 'z')),
                 Statement(Item('x'), ValueSnak(Property('y'), String('z')))),
                ((Item('x'), NoValueSnak('y')),
                 Statement(Item('x'), NoValueSnak(Property('y')))),
                (Property('y')(Property('x'), ExternalId('z')),
                 (Statement(Property('x'), Property('y')(ExternalId('z'))))),
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
                Statement(Variable('x'), Variable('y')),
                Text('x'),
                ValueSnak('x', 'y'),
                Variable('x', Text),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(Statement(Item('x'), NoValueSnak('y')), Statement)
        self._test__init__(
            Statement,
            self.assert_statement,
            success=[
                ([Item('x'), ValueSnak('y', 'z')],
                 Statement(Item('x'), ValueSnak('y', 'z'))),
                ([Property('x'), NoValueSnak('y')],
                 Statement(Property('x'), NoValueSnak('y'))),
            ],
            failure=[
                [0, 'x'],
                [IRI('x'), NoValueSnak('x')],
                [Item('x'), Property('x')],
                [NoValueSnak('x'), NoValueSnak('y')],
                [SomeValueSnak('x'), SomeValueSnak('y')],
                [String(Variable('x')), Property('y')],
                [Text('x'), 'x'],
                [ValueSnak('x', 'x'), 'y'],
                [Variable('x', IRI), Variable('y')],
                [{}, 'y'],
            ])


if __name__ == '__main__':
    Test.main()
