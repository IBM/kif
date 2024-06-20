# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    ExternalIdTemplate,
    IRI,
    IRI_Template,
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
        assert_type(ExternalIdTemplate.object_class, type[ExternalId])

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
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (ExternalIdTemplate, 'ExternalId'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into StringVariable",
            ExternalIdTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI_Template into StringVariable',
            ExternalIdTemplate, IRI_Template(Variable('x')))
        # success
        assert_type(ExternalIdTemplate(Variable('x')), ExternalIdTemplate)
        self.assert_string_template(
            ExternalIdTemplate(Variable('x')), Variable('x', String))
        x = Variable('x')
        self.assert_external_id_template(
            ExternalIdTemplate(x), StringVariable('x'))
        self.assert_external_id_template(
            ExternalId(x), Variable('x', String))
        self.assert_external_id(ExternalId('x'), 'x')


if __name__ == '__main__':
    Test.main()
