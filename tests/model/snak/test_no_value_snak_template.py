# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DatatypeVariable,
    IRI,
    IRI_Template,
    Item,
    ItemVariable,
    KIF_Object,
    NoValueSnak,
    NoValueSnakTemplate,
    Property,
    PropertyVariable,
    SomeValueSnakTemplate,
    Variable,
)
from kif_lib.typing import assert_type

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

    def test_instantiate(self) -> None:
        assert_type(
            NoValueSnakTemplate(Variable('x')).instantiate({}), KIF_Object)
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
