# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import ExternalId, IRI, String
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_check(self) -> None:
        self.assert_raises_check_error(String, 0)
        self.assert_raises_check_error(String, {})
        self.assert_raises_check_error(String, IRI('x'))
        # success
        assert_type(String.check(String('x')), String)
        self.assertEqual(String.check(String('x')), String('x'))
        self.assertEqual(String.check(String('x')), String('x'))
        self.assertEqual(String.check(ExternalId('x')), ExternalId('x'))
        self.assertEqual(String.check(URIRef('x')), String('x'))
        self.assertEqual(String.check(Literal('x')), String('x'))
        self.assertEqual(String.check('x'), String('x'))

    def test__init__(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int', String, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got dict', String, {})
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got IRI', String, IRI('x'))
        # success
        assert_type(String('x'), String)
        self.assert_string(String(String('x')), 'x')
        self.assert_string(String(String('x')), 'x')
        self.assert_string(String('x'), 'x')
        self.assert_string(ExternalId('x'), 'x')
        self.assert_string(String(URIRef('x')), 'x')
        self.assert_string(String(Literal('x')), 'x')
        self.assert_string(String('x'), 'x')


if __name__ == '__main__':
    Test.main()
