# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.model import IRI, IRI_Template, String, Variable

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_check(self):
        self.assert_raises_check_error(IRI_Template, 0)
        self.assert_raises_check_error(IRI_Template, {})
        self.assert_raises_check_error(IRI_Template, IRI('x'))
        self.assert_raises_check_error(IRI_Template, IRI_Template('x'))
        self.assertEqual(
            IRI_Template.check(IRI_Template(Variable('x'))),
            IRI_Template(Variable('x', String)))

    def test__init__(self):
        self.assert_raises_check_error(IRI_Template, Variable('x', IRI))
        self.assertEqual(
            IRI_Template(Variable('x')),
            IRI_Template(Variable('x', String)))


if __name__ == '__main__':
    Test.main()
