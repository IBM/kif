# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

import kif.namespace as NS
from kif import String, Text

from .tests import kif_TestCase, main


class TestModelText(kif_TestCase):

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
            TypeError, Text._from_rdflib, Literal(
                '1.0', datatype=NS.XSD.decimal))
        # good arguments
        self.assert_text(
            Text._from_rdflib(Literal('abc', 'es')), 'abc', 'es')

    def test__to_rdflib(self):
        self.assertEqual(Text('abc')._to_rdflib(), Literal('abc', 'en'))
        self.assertEqual(
            Text('abc', 'es')._to_rdflib(), Literal('abc', 'es'))


if __name__ == '__main__':
    main()
