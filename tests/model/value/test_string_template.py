# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.model import (
    ExternalIdTemplate,
    IRI,
    String,
    StringTemplate,
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
        # success
        assert_type(StringTemplate(Variable('x')), StringTemplate)
        self.assert_string_template(
            StringTemplate(Variable('x')), Variable('x', String))
        self.assert_string_template(
            ExternalIdTemplate(Variable('x')), Variable('x', String))


if __name__ == '__main__':
    Test.main()
