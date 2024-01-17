# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

from kif_lib import String

from .tests import kif_TestCase, main


class TestModelString(kif_TestCase):

    def test__preprocess_arg_string(self):
        self.assertEqual(
            String('abc'), String._preprocess_arg_string('abc', 1))
        self.assertEqual(
            String('abc'), String._preprocess_arg_string(String('abc'), 1))

    def test__preprocess_optional_arg_string(self):
        self.assertEqual(
            String('abc'),
            String._preprocess_optional_arg_string(None, 1, String('abc')))
        self.assertEqual(
            String('xyz'),
            String._preprocess_optional_arg_string('xyz', 1, String('abc')))

    def test__init__(self):
        self.assertRaises(TypeError, String, 0)
        self.assert_string(String('abc'), 'abc')
        self.assert_string(String(String('abc')), 'abc')

    def test__from_rdflib(self):
        # bad argument: uri
        self.assertRaises(TypeError, String._from_rdflib, URIRef('x'))
        # good arguments
        self.assert_string(String._from_rdflib(Literal('abc')), 'abc')

    def test__to_rdflib(self):
        self.assertEqual(String('abc')._to_rdflib(), Literal('abc'))


if __name__ == '__main__':
    main()
