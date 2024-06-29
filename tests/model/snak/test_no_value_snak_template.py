# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DatatypeVariable,
    Item,
    KIF_Object,
    NoValueSnak,
    NoValueSnakTemplate,
    Property,
    PropertyVariable,
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
        self._test_check(NoValueSnakTemplate)

    def test__init__(self) -> None:
        assert_type(NoValueSnakTemplate(Variable('x')), NoValueSnakTemplate)
        self._test__init__(
            NoValueSnakTemplate, self.assert_no_value_snak_template)

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
