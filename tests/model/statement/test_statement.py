# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    EntityVariable,
    ExternalId,
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    Property,
    Quantity,
    SnakVariable,
    SomeValueSnak,
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    Term,
    Text,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import StatementTestCase


class Test(StatementTestCase):

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

    def test_variables(self) -> None:
        assert_type(
            Statement(Item('x'), SomeValueSnak('y')).variables,
            Set[Variable])
        self._test_variables(
            Statement, (Statement(Item('x'), SomeValueSnak('y')), set()))

    def test_instantiate(self) -> None:
        assert_type(
            Statement(Item('x'), NoValueSnak('y')).instantiate({}), Term)
        self._test_instantiate(
            Statement, success=[
                (Statement(Item('x'), ValueSnak('y', 'z')),
                 Statement(Item('x'), ValueSnak('y', 'z')),
                 {Variable('x'): String('y')})
            ])

    def test_match(self) -> None:
        assert_type(
            Statement(Item('x'), ValueSnak('y', 'z')).match(
                Statement(Item('x'), ValueSnak('y', 'z'))), Optional[Theta])
        self._test_match(
            Statement, success=[
                (Statement(Item('x'), ValueSnak('y', 'z')),
                 Statement(Item('x'), ValueSnak('y', 'z')), {}),
                (Statement(Item('x'), SomeValueSnak('y')),
                 StatementVariable('x'),
                 {StatementVariable('x'):
                  Statement(Item('x'), SomeValueSnak('y'))}),
                (Statement(Property('x'), NoValueSnak('y')),
                 Statement(Variable('x'), Variable('y')),
                 {EntityVariable('x'): Property('x'),
                  SnakVariable('y'): NoValueSnak('y')}),
            ],
            failure=[
                (Statement(Item('x'), NoValueSnak('y')),
                 Statement(Property('x'), NoValueSnak('y'))),
                (Statement(Item('x'), ValueSnak('y', 'z')),
                 ValueSnak('y', 'z')),
            ])


if __name__ == '__main__':
    Test.main()
