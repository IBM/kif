# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Context,
    DataValue,
    ExternalId,
    Item,
    ShallowDataValue,
    String,
    StringTemplate,
    StringVariable,
    Term,
    Text,
    TextTemplate,
    TextVariable,
    Variable,
    Variables,
)
from kif_lib.typing import assert_type

from ...tests import ShallowDataValueTemplateTestCase


class Test(ShallowDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(TextTemplate.object_class, type[Text])
        self.assertIs(TextTemplate.object_class, Text)

    def test_check(self) -> None:
        assert_type(
            TextTemplate.check(TextTemplate(Variable('x'))), TextTemplate)
        self._test_check(TextTemplate)
        self.assertEqual(
            TextTemplate.check(TextTemplate(Variable('x'), Variable('y'))),
            TextTemplate(Variable('x', String), Variable('y', String)))

    def test__init__(self) -> None:
        assert_type(TextTemplate(Variable('x')), TextTemplate)
        self._test__init__(
            TextTemplate,
            self.assert_text_template,
            success=[
                (['x', Variable('y', String)],
                 Text('x', Variable('y', String))),
                ([StringVariable('x'), 'y'],
                 Text(Variable('x', String), 'y')),
                ([StringVariable('x'), StringVariable('y')],
                 Text(Variable('x', String), Variable('y', String))),
                ([Variable('x', String),
                  Context.top().options.default_language],
                 Text(Variable('x', String)))
            ],
            normalize=[
                [Variable('x'), Variable('x')],
                [Variable('x', ShallowDataValue), Variable('x', DataValue)],
            ],
            failure=[
                [Variable('x'), 0],
                [Variable('x'), {}],
                [Variable('x'), StringTemplate(Variable('y'))],
                [Variable('x'), TextVariable('y')],
                [Variable('x'), Variable('y', Text)],
            ])
        x, y = Variables('x', 'y')
        self.assert_text_template(
            Text(x, y), Variable('x', String), StringVariable('y'))
        self.assert_text(Text(String('x'), String('y')), 'x', 'y')
        self.assert_text_template(
            TextTemplate(
                Variable('x', ShallowDataValue),
                Variable('x', DataValue)),
            StringVariable('x'), StringVariable('x'))

    def test_instantiate(self) -> None:
        assert_type(
            TextTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            TextTemplate,
            success=[
                (TextTemplate(Variable('x'), Variable('x')),
                 Text('x', 'x'),
                 {StringVariable('x'): ExternalId('x')}),
                (TextTemplate('x', Variable('y')),
                 Text('x', 'y'),
                 {StringVariable('y'): String('y')}),
                (TextTemplate('x', Variable('y')),
                 TextTemplate('x', Variable('z')),
                 {StringVariable('y'): StringVariable('z')}),
                (TextTemplate('x', Variable('y')),
                 TextTemplate('x'),
                 {StringVariable('y'): None}),
            ],
            failure=[
                (TextTemplate(Variable('x'), Variable('x')),
                 {StringVariable('x'): Item('x')}),
            ])


if __name__ == '__main__':
    Test.main()
