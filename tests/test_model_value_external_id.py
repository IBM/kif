# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

from kif_lib import ExternalId, String

from .tests import kif_TestCase


class TestExternalId(kif_TestCase):

    def test__preprocess_arg_external_id(self):
        self.assertEqual(
            ExternalId('abc'),
            ExternalId._preprocess_arg_external_id('abc', 1))
        self.assertEqual(
            ExternalId('abc'),
            ExternalId._preprocess_arg_external_id(String('abc'), 1))
        self.assertEqual(
            ExternalId('abc'),
            ExternalId._preprocess_arg_external_id(ExternalId('abc'), 1))

    def test__preprocess_optional_arg_external_id(self):
        self.assertEqual(
            ExternalId('abc'),
            ExternalId._preprocess_optional_arg_external_id(
                None, 1, ExternalId('abc')))
        self.assertEqual(
            ExternalId('xyz'),
            ExternalId._preprocess_optional_arg_external_id(
                'xyz', 1, ExternalId('abc')))

    def test__init__(self):
        self.assertRaises(TypeError, ExternalId, 0)
        self.assert_external_id(ExternalId('abc'), 'abc')
        self.assert_external_id(ExternalId(String('abc')), 'abc')
        self.assert_external_id(ExternalId(ExternalId('abc')), 'abc')

    def test__from_rdflib(self):
        # bad argument: uri
        self.assertRaises(TypeError, ExternalId._from_rdflib, URIRef('x'))
        # good arguments
        self.assert_external_id(
            ExternalId._from_rdflib(Literal('abc')), 'abc')

    def test__to_rdflib(self):
        self.assertEqual(ExternalId('abc')._to_rdflib(), Literal('abc'))


if __name__ == '__main__':
    TestExternalId.main()
