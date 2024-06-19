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

    def test_check(self) -> None:
        self.assert_raises_check_error(
            ExternalIdTemplate, 0, ExternalIdTemplate.check)
        self.assert_raises_check_error(
            ExternalIdTemplate, {}, ExternalIdTemplate.check)
        self.assert_raises_check_error(
            ExternalIdTemplate, IRI('x'), ExternalIdTemplate.check)
        self.assert_raises_check_error(
            ExternalIdTemplate, ExternalIdTemplate('x'))
        self.assert_raises_check_error(
            ExternalIdTemplate, StringTemplate(Variable('x')))
        # success
        assert_type(
            ExternalIdTemplate.check(ExternalIdTemplate(Variable('x'))),
            ExternalIdTemplate)
        self.assertEqual(
            ExternalIdTemplate.check(ExternalIdTemplate(Variable('x'))),
            ExternalIdTemplate(Variable('x', String)))

    def test__init__(self) -> None:
        self.assert_raises_check_error(ExternalIdTemplate, Variable('x', IRI))
        # success
        assert_type(ExternalIdTemplate(Variable('x')), ExternalIdTemplate)
        self.assert_string_template(
            ExternalIdTemplate(Variable('x')), Variable('x', String))


if __name__ == '__main__':
    Test.main()
