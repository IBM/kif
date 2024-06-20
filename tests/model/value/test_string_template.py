# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalIdTemplate,
    IRI,
    IRI_Variable,
    String,
    StringTemplate,
    StringVariable,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_object_class(self) -> None:
        assert_type(StringTemplate.object_class, type[String])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            StringTemplate, 0, StringTemplate.check)
        self.assert_raises_check_error(
            StringTemplate, {}, StringTemplate.check)
        self.assert_raises_check_error(
            StringTemplate, IRI('x'), StringTemplate.check)
        self.assert_raises_check_error(
            StringTemplate, StringTemplate('x'), StringTemplate.check)
        # success
        assert_type(
            StringTemplate.check(StringTemplate(Variable('x'))),
            StringTemplate)
        self.assertEqual(
            StringTemplate.check(StringTemplate(Variable('x'))),
            StringTemplate(Variable('x', String)))
        self.assertEqual(
            StringTemplate.check(ExternalIdTemplate(Variable('x'))),
            ExternalIdTemplate(Variable('x', String)))

    def test__init__(self) -> None:
        self.assert_raises_check_error(StringTemplate, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (StringTemplate, 'String'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into StringVariable",
            StringTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce StringTemplate into StringVariable",
            StringTemplate, StringTemplate(Variable('x')))
        # success
        assert_type(StringTemplate(Variable('x')), StringTemplate)
        self.assert_string_template(
            StringTemplate(Variable('x')), Variable('x', String))
        self.assert_string_template(
            ExternalIdTemplate(Variable('x')), Variable('x', String))
        x = Variable('x')
        self.assert_string_template(
            StringTemplate(x), StringVariable('x'))
        self.assert_string_template(String(x), Variable('x', String))
        self.assert_string(String('x'), 'x')


if __name__ == '__main__':
    Test.main()
