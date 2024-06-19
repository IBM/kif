# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import ExternalId, IRI, String
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_check(self) -> None:
        self.assert_raises_check_error(IRI, 0, IRI.check)
        self.assert_raises_check_error(IRI, {}, IRI.check)
        # success
        assert_type(IRI.check(IRI('x')), IRI)
        self.assertEqual(IRI.check(IRI('x')), IRI('x'))
        self.assertEqual(IRI.check(String('x')), IRI('x'))
        self.assertEqual(IRI.check(ExternalId('x')), IRI('x'))
        self.assertEqual(IRI.check(URIRef('x')), IRI('x'))
        self.assertEqual(IRI.check(Literal('x')), IRI('x'))
        self.assertEqual(IRI.check('x'), IRI('x'))

    def test__init__(self) -> None:
        self.assert_raises_check_error(String, 0, IRI, None, 1)
        self.assert_raises_check_error(String, {}, IRI, None, 1)
        # success
        assert_type(IRI('x'), IRI)
        self.assert_iri(IRI(IRI('x')), 'x')
        self.assert_iri(IRI(String('x')), 'x')
        self.assert_iri(IRI(ExternalId('x')), 'x')
        self.assert_iri(IRI(URIRef('x')), 'x')
        self.assert_iri(IRI(Literal('x')), 'x')
        self.assert_iri(IRI('x'), 'x')


if __name__ == '__main__':
    Test.main()
