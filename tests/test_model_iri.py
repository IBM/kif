# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

import kif_lib.namespace as NS
from kif_lib import IRI

from .tests import kif_TestCase, main


class TestModel_IRI(kif_TestCase):

    def test__preprocess_arg_iri(self):
        self.assertEqual(
            IRI('abc'), IRI._preprocess_arg_iri('abc', 1))
        self.assertEqual(
            IRI('abc'), IRI._preprocess_arg_iri(IRI('abc'), 1))

    def test__preprocess_optional_arg_iri(self):
        self.assertEqual(
            IRI('abc'),
            IRI._preprocess_optional_arg_iri(None, 1, IRI('abc')))
        self.assertEqual(
            IRI('xyz'),
            IRI._preprocess_optional_arg_iri(IRI('xyz'), 1, IRI('abc')))

    def test__init__(self):
        self.assertRaises(TypeError, IRI, 0)
        self.assert_iri(
            IRI(NS.XSD.decimal), 'http://www.w3.org/2001/XMLSchema#decimal')
        self.assert_iri(IRI('abc'), 'abc')
        self.assert_iri(IRI(IRI(IRI('abc'))), 'abc')

    def test__from_rdflib(self):
        # bad argument: literal
        self.assertRaises(TypeError, IRI._from_rdflib, Literal('x'))
        # bad argument: result is an item
        self.assertRaises(TypeError, IRI._from_rdflib, URIRef(NS.WD.Q155))
        # bad argument: result is a property
        self.assertRaises(TypeError, IRI._from_rdflib, URIRef(NS.WD.P31))
        # good arguments
        self.assert_iri(
            IRI._from_rdflib(URIRef('http://www.abc.org/')),
            'http://www.abc.org/')
        self.assert_iri(IRI._from_rdflib(URIRef('abc')), 'abc')

    def test__to_rdflib(self):
        self.assertEqual(IRI('abc')._to_rdflib(), URIRef('abc'))


if __name__ == '__main__':
    main()
