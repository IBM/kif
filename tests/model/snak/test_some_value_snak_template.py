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
        assert_type(SomeValueSnakTemplate.object_class, type[SomeValueSnak])
        self.assertIs(SomeValueSnakTemplate.object_class, SomeValueSnak)

    def test_check(self) -> None:
        assert_type(
            SomeValueSnakTemplate.check(SomeValueSnakTemplate(Variable('x'))),
            SomeValueSnakTemplate)
        self._test_check(
            SomeValueSnakTemplate,
            success=[
                (SomeValueSnakTemplate(Variable('x')),
                 SomeValueSnakTemplate(PropertyVariable('x'))),
            ],
            failure=[
                NoValueSnakTemplate(Variable('x')),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(
            SomeValueSnakTemplate(Variable('x')), SomeValueSnakTemplate)
        self._test__init__(
            SomeValueSnakTemplate,
            self.assert_some_value_snak_template,
            success=[
                ([Variable('x')], SomeValueSnak(PropertyVariable('x'))),
                ([Property(Variable('x'))],
                 SomeValueSnak(Property(Variable('x', IRI)))),
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
            (SomeValueSnakTemplate, 'SomeValueSnak'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into PropertyVariable",
            SomeValueSnakTemplate, IRI_Variable('x'))
        self.assert_some_value_snak_template(
            SomeValueSnakTemplate(x),
            PropertyVariable('x'))
        self.assert_some_value_snak_template(
            SomeValueSnakTemplate(Property(x)),
            PropertyTemplate(IRI_Variable('x')))
        self.assert_some_value_snak_template(
            cast(SomeValueSnakTemplate, SomeValueSnak(x)),
            PropertyVariable('x'))
        self.assert_some_value_snak_template(
            SomeValueSnak(Property(x)),
            Property(Variable('x', IRI)))
        self.assert_some_value_snak(
            cast(SomeValueSnak, SomeValueSnakTemplate(Property('x'))),
            Property('x'))

    def test_variables(self) -> None:
        assert_type(
            SomeValueSnakTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(
            SomeValueSnakTemplate,
            (SomeValueSnak(Variable('x')), {PropertyVariable('x')}))

    def test_instantiate(self) -> None:
        assert_type(SomeValueSnakTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            SomeValueSnakTemplate,
            success=[
                (SomeValueSnakTemplate(Variable('x')),
                 SomeValueSnak('y'),
                 {PropertyVariable('x'): Property('y')}),
                (SomeValueSnakTemplate(Property('x', Variable('y'))),
                 SomeValueSnak(Property('x', ItemDatatype())),
                 {DatatypeVariable('y'): ItemDatatype()}),
            ],
            failure=[
                (SomeValueSnakTemplate(Variable('x')),
                 {PropertyVariable('x'): Item('y')}),
            ])

    def test_match(self) -> None:
        assert_type(SomeValueSnakTemplate(Variable('x')).match(
            Variable('x')), Optional[Theta])
        self._test_match(
            SomeValueSnakTemplate,
            success=[
                (SomeValueSnak(Variable('x')), SomeValueSnak('x'),
                 {PropertyVariable('x'): Property('x')}),
                (SomeValueSnak(Property(Variable('x'), Variable('y'))),
                 SomeValueSnak(Property(Variable('z'), Item)),
                 {IRI_Variable('x'): IRI_Variable('z'),
                  DatatypeVariable('y'): ItemDatatype()}),
            ], failure=[
                (SomeValueSnak(Variable('x')), NoValueSnak('x')),
                (SomeValueSnak(Variable('x')), ValueSnak('x', 'y')),
            ])


if __name__ == '__main__':
    Test.main()
