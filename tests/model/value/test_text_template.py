# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.model import String, Text, TextTemplate, Variable
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
        # success
        assert_type(TextTemplate(Variable('x')), TextTemplate)
        self.assert_text_template(
            TextTemplate(Variable('x')),
            Variable('x', String), Text.default_language)
        self.assert_text_template(
            TextTemplate(Text('x'), Variable('y')),
            'x', Variable('y', String))


if __name__ == '__main__':
    Test.main()
