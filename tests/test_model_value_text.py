# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

from kif_lib import String, Text
from kif_lib.namespace import XSD

from .tests import kif_TestCase


class TestText(kif_TestCase):

    def test__check_arg_text(self):
        self.assertRaises(TypeError, Text._check_arg_text, 55)
        self.assertEqual(Text._check_arg_text('abc'), Text('abc'))
        self.assertEqual(
            Text._check_arg_text(Text('abc', 'pt')), Text('abc', 'pt'))

    def test__init__(self):
        self.assertRaises(TypeError, Text, 0)
        self.assert_text(Text('abc'), 'abc', 'en')
        self.assert_text(Text(String('abc')), 'abc', 'en')
        self.assert_text(Text(Text('abc')), 'abc', 'en')
        self.assert_text(Text('abc', 'pt'), 'abc', 'pt')

    def test__from_rdflib(self):
        # bad argument: uri
        self.assertRaises(TypeError, Text._from_rdflib, URIRef('x'))
        # bad argument: no language tag
        self.assertRaises(TypeError, Text._from_rdflib, Literal('x'))
        # bad argument: typed literal
        self.assertRaises(
            TypeError, Text._from_rdflib, Literal('1.0', datatype=XSD.decimal))
        # good arguments
        self.assert_text(
            Text._from_rdflib(Literal('abc', 'es')), 'abc', 'es')

    def test__to_rdflib(self):
        self.assertEqual(Text('abc')._to_rdflib(), Literal('abc', 'en'))
        self.assertEqual(
            Text('abc', 'es')._to_rdflib(), Literal('abc', 'es'))


if __name__ == '__main__':
    TestText.main()
