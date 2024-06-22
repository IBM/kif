# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    ShallowDataValue,
    String,
    StringTemplate,
    StringVariable,
    Text,
    TextTemplate,
    TextVariable,
    Variable,
    Variables,
)
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_object_class(self) -> None:
        assert_type(TextTemplate.object_class, type[Text])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            TextTemplate, 0, TextTemplate.check)
        self.assert_raises_check_error(
            TextTemplate, {}, TextTemplate.check)
        self.assert_raises_check_error(
            TextTemplate, Text('x'), TextTemplate.check)
        self.assert_raises_check_error(
            TextTemplate, TextTemplate('x'), TextTemplate.check)
        # success
        assert_type(
            TextTemplate.check(TextTemplate(Variable('x'))),
            TextTemplate)
        self.assertEqual(
            TextTemplate.check(TextTemplate(Variable('x'))),
            TextTemplate(Variable('x', String)))
        self.assertEqual(
            TextTemplate.check(TextTemplate(Variable('x'), Variable('y'))),
            TextTemplate(Variable('x', String), Variable('y', String)))

    def test__init__(self) -> None:
        self.assert_raises_check_error(TextTemplate, Variable('x', Text))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce TextVariable into StringVariable',
            TextTemplate, 'x', Variable('y', Text))
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into String',
            (TextTemplate, 'Text'), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce int into String',
            (TextTemplate, 'Text'), 'x', 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce TextVariable into StringVariable",
            TextTemplate, TextVariable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce StringTemplate into StringVariable',
            TextTemplate, StringTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce TextVariable into StringVariable",
            TextTemplate, 'x', TextVariable('y'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce StringTemplate into StringVariable',
            TextTemplate, 'x', StringTemplate(Variable('y')))
        # success
        assert_type(TextTemplate(Variable('x')), TextTemplate)
        self.assert_text_template(
            TextTemplate(Variable('x')),
            Variable('x', String), Text.default_language)
        self.assert_text_template(
            TextTemplate(Text('x'), Variable('y')),
            'x', Variable('y', String))
        x, y = Variables('x', 'y')
        self.assert_text_template(
            TextTemplate(x, y),
            StringVariable('x'), StringVariable('y'))
        self.assert_text_template(
            TextTemplate('x', y), 'x', StringVariable('y'))
        self.assert_text_template(
            TextTemplate(x, 'y'),
            StringVariable('x'), 'y')
        self.assert_text_template(
            TextTemplate(x), StringVariable('x'),
            Text.default_language)
        self.assert_text_template(
            Text(x, y), Variable('x', String), StringVariable('y'))
        self.assert_text(Text(String('x'), String('y')), 'x', 'y')
        # normalization
        x = Variable('x')
        self.assert_text_template(
            TextTemplate(x, x), StringVariable('x'), StringVariable('x'))
        self.assert_text_template(
            TextTemplate(
                Variable('x', ShallowDataValue),
                Variable('x', DataValue)),
            StringVariable('x'), StringVariable('x'))
        self.assert_text_template(
            TextTemplate(StringVariable('x'), StringVariable('x')),
            StringVariable('x'), StringVariable('x'))


if __name__ == '__main__':
    Test.main()
