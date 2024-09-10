# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DatatypeVariable,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemVariable,
    NoValueSnak,
    NoValueSnakTemplate,
    Property,
    PropertyTemplate,
    PropertyVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    Term,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, cast, Optional, Set

from ...tests import SnakTemplateTestCase


class Test(SnakTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(NoValueSnakTemplate.object_class, type[NoValueSnak])
        self.assertIs(NoValueSnakTemplate.object_class, NoValueSnak)

    def test_check(self) -> None:
        assert_type(
            NoValueSnakTemplate.check(NoValueSnakTemplate(Variable('x'))),
            NoValueSnakTemplate)
        self._test_check(
            NoValueSnakTemplate,
            success=[
                (NoValueSnakTemplate(Variable('x')),
                 NoValueSnakTemplate(PropertyVariable('x'))),
            ],
            failure=[
                SomeValueSnakTemplate(Variable('x')),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(NoValueSnakTemplate(Variable('x')), NoValueSnakTemplate)
        self._test__init__(
            NoValueSnakTemplate,
            self.assert_no_value_snak_template,
            success=[
                ([Variable('x')], NoValueSnak(PropertyVariable('x'))),
                ([Property(Variable('x'))],
                 NoValueSnak(Property(Variable('x', IRI)))),
            ],
            failure=[
                [IRI_Template(Variable('x'))],
                [ItemVariable('x')],
            ],
            normalize=[
                ['x'],
                [IRI('x')],
                [Property('x')],
            ])

        # extra
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            (NoValueSnakTemplate, 'NoValueSnak'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into PropertyVariable",
            NoValueSnakTemplate, IRI_Variable('x'))
        self.assert_no_value_snak_template(
            NoValueSnakTemplate(x), PropertyVariable('x'))
        self.assert_no_value_snak_template(
            NoValueSnakTemplate(Property(x)),
            PropertyTemplate(IRI_Variable('x')))
        self.assert_no_value_snak_template(
            NoValueSnak(x), PropertyVariable('x'))
        self.assert_no_value_snak_template(
            NoValueSnak(Property(x)),
            Property(Variable('x', IRI)))
        self.assert_no_value_snak(
            cast(NoValueSnak, NoValueSnakTemplate(Property('x'))),
            Property('x'))

    def test_variables(self) -> None:
        assert_type(
            NoValueSnakTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(
            NoValueSnakTemplate,
            (NoValueSnak(Variable('x')), {PropertyVariable('x')}))

    def test_instantiate(self) -> None:
        assert_type(NoValueSnakTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            NoValueSnakTemplate,
            success=[
                (NoValueSnakTemplate(Variable('x')),
                 NoValueSnak('y'),
                 {PropertyVariable('x'): Property('y')}),
                (NoValueSnakTemplate(Property('x', Variable('y'))),
                 NoValueSnak(Property('x', ItemDatatype())),
                 {DatatypeVariable('y'): ItemDatatype()}),
            ],
            failure=[
                (NoValueSnakTemplate(Variable('x')),
                 {PropertyVariable('x'): Item('y')}),
            ])

    def test_match(self) -> None:
        assert_type(
            NoValueSnakTemplate(Variable('x')).match(
                Variable('x')), Optional[Theta])
        self._test_match(
            NoValueSnakTemplate,
            success=[
                (NoValueSnak(Variable('x')), NoValueSnak('x'),
                 {PropertyVariable('x'): Property('x')}),
                (NoValueSnak(Property(Variable('x'), Variable('y'))),
                 NoValueSnak(Property(Variable('z'), Item)),
                 {IRI_Variable('x'): IRI_Variable('z'),
                  DatatypeVariable('y'): ItemDatatype()}),
            ], failure=[
                (NoValueSnak(Variable('x')), SomeValueSnak('x')),
                (NoValueSnak(Variable('x')), ValueSnak('x', 'y')),
            ])


if __name__ == '__main__':
    Test.main()
