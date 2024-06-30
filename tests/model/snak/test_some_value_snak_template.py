# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DatatypeVariable,
    IRI,
    IRI_Template,
    Item,
    ItemVariable,
    KIF_Object,
    Property,
    PropertyVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_SnakTemplateTestCase


class Test(kif_SnakTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(SomeValueSnakTemplate.object_class, type[SomeValueSnak])
        self.assertIs(SomeValueSnakTemplate.object_class, SomeValueSnak)

    def test_check(self) -> None:
        assert_type(
            SomeValueSnakTemplate.check(SomeValueSnakTemplate(Variable('x'))),
            SomeValueSnakTemplate)
        self._test_check(SomeValueSnakTemplate)

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

    def test_instantiate(self) -> None:
        assert_type(
            SomeValueSnakTemplate(Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(
            SomeValueSnakTemplate,
            success=[
                (SomeValueSnakTemplate(Variable('x')),
                 SomeValueSnak('y'),
                 {PropertyVariable('x'): Property('y')}),
                (SomeValueSnakTemplate(Property('x', Variable('y'))),
                 SomeValueSnak(Property('x', Item.datatype)),
                 {DatatypeVariable('y'): Item.datatype}),
            ],
            failure=[
                (SomeValueSnakTemplate(Variable('x')),
                 {PropertyVariable('x'): Item('y')}),
            ])


if __name__ == '__main__':
    Test.main()
