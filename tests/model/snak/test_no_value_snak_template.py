# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DatatypeVariable,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemVariable,
    NoValueSnak,
    NoValueSnakTemplate,
    Property,
    PropertyTemplate,
    PropertyVariable,
    SomeValueSnakTemplate,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, cast

from ...tests import kif_SnakTemplateTestCase


class Test(kif_SnakTemplateTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(NoValueSnakTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            NoValueSnakTemplate,
            success=[
                (NoValueSnakTemplate(Variable('x')),
                 NoValueSnak('y'),
                 {PropertyVariable('x'): Property('y')}),
                (NoValueSnakTemplate(Property('x', Variable('y'))),
                 NoValueSnak(Property('x', Item.datatype)),
                 {DatatypeVariable('y'): Item.datatype}),
            ],
            failure=[
                (NoValueSnakTemplate(Variable('x')),
                 {PropertyVariable('x'): Item('y')}),
            ])


if __name__ == '__main__':
    Test.main()
