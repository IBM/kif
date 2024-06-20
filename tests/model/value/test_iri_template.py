# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    IRI_Template,
    IRI_Variable,
    String,
    StringTemplate,
    StringVariable,
    Variable,
)
from kif_lib.typing import assert_type, cast

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_object_class(self) -> None:
        assert_type(IRI_Template.object_class, type[IRI])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            IRI_Template, 0, IRI_Template.check)
        self.assert_raises_check_error(
            IRI_Template, {}, IRI_Template.check)
        self.assert_raises_check_error(
            IRI_Template, IRI('x'), IRI_Template.check)
        self.assert_raises_check_error(
            IRI_Template, IRI_Template('x'), IRI_Template.check)
        # success
        assert_type(
            IRI_Template.check(IRI_Template(Variable('x'))),
            IRI_Template)
        self.assertEqual(
            IRI_Template.check(IRI_Template(Variable('x'))),
            IRI_Template(Variable('x', String)))

    def test__init__(self) -> None:
        self.assert_raises_check_error(IRI_Template, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into String',
            (IRI_Template, 'IRI'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into StringVariable",
            IRI_Template, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce StringTemplate into StringVariable',
            IRI_Template, StringTemplate(Variable('x')))
        # success
        assert_type(IRI_Template(Variable('x')), IRI_Template)
        self.assert_iri_template(
            IRI_Template(Variable('x')), Variable('x', String))
        x = Variable('x')
        self.assert_iri_template(IRI_Template(x), StringVariable('x'))
        self.assert_iri_template(
            cast(IRI_Template, IRI(x)), Variable('x', String))
        self.assert_iri(IRI(String('x')), 'x')


if __name__ == '__main__':
    Test.main()
