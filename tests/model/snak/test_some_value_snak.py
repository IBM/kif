# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    NoValueSnakVariable,
    Property,
    PropertyVariable,
    Quantity,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    String,
    Term,
    Text,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import SnakTestCase


class Test(SnakTestCase):

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

    def test_variables(self) -> None:
        assert_type(SomeValueSnak('x').variables, Set[Variable])
        self._test_variables(SomeValueSnak, (SomeValueSnak('x'), set()))

    def test_instantiate(self) -> None:
        assert_type(SomeValueSnak('x').instantiate({}), Term)
        self._test_instantiate(
            SomeValueSnak,
            success=[
                (SomeValueSnak('x'),
                 SomeValueSnak('x'),
                 {Variable('x'): String('y')})
            ])

    def test_match(self) -> None:
        assert_type(
            SomeValueSnak('x').match(SomeValueSnak('x')), Optional[Theta])
        self._test_match(
            SomeValueSnak,
            success=[
                (SomeValueSnak('x'), SomeValueSnak('x'), {}),
                (SomeValueSnak('x'), SnakVariable('x'),
                 {SnakVariable('x'): SomeValueSnak('x')}),
                (SomeValueSnak('x'), SomeValueSnak(Variable('x')),
                 {PropertyVariable('x'): Property('x')}),
            ],
            failure=[
                (SomeValueSnak('x'), NoValueSnak('x')),
                (SomeValueSnak('x'), NoValueSnakVariable('x')),
            ])


if __name__ == '__main__':
    Test.main()
