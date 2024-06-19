# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

from kif_lib import String
from kif_lib.typing import cast

from .tests import kif_TestCase


class TestModelValueString(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, String, 0)
        self.assert_string(String('abc'), 'abc')
        self.assert_string(String(String('abc')), 'abc')

    def test__from_rdflib(self):
        # bad argument: uri
        self.assertRaises(TypeError, String._from_rdflib, URIRef('x'))
        # good arguments
        self.assert_string(
            cast(String, String._from_rdflib(Literal('abc'))), 'abc')

    def test__to_rdflib(self):
        self.assertEqual(String('abc')._to_rdflib(), Literal('abc'))


if __name__ == '__main__':
    TestModelValueString.main()
