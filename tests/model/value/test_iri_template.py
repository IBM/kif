# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.model import IRI, IRI_Template, String, Variable
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_check(self) -> None:
        self.assert_raises_check_error(IRI_Template, 0)
        self.assert_raises_check_error(IRI_Template, {})
        self.assert_raises_check_error(IRI_Template, IRI('x'))
        self.assert_raises_check_error(IRI_Template, IRI_Template('x'))
        # success
        assert_type(
            IRI_Template.check(IRI_Template(Variable('x'))),
            IRI_Template)
        self.assertEqual(
            IRI_Template.check(IRI_Template(Variable('x'))),
            IRI_Template(Variable('x', String)))

    def test__init__(self) -> None:
        self.assert_raises_check_error(IRI_Template, Variable('x', IRI))
        # success
        assert_type(IRI_Template(Variable('x')), IRI_Template)
        self.assert_iri_template(
            IRI_Template(Variable('x')), Variable('x', String))


if __name__ == '__main__':
    Test.main()
