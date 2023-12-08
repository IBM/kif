# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

import kif.namespace as NS
from kif import Entity, IRI, Item, Properties, Property, ValueSnak

from .tests import kif_TestCase, main


class TestModelProperty(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, Property, 0)
        self.assert_property(Property('abc'), IRI('abc'))
        self.assert_property(Property(IRI('abc')), IRI('abc'))

    def test_Properties(self):
        a, b, c = Properties('a', IRI('b'), 'c')
        self.assert_property(a, IRI('a'))
        self.assert_property(b, IRI('b'))
        self.assert_property(c, IRI('c'))

    def test__call__(self):
        p = Property('x')
        self.assert_property(p, IRI('x'))
        self.assert_value_snak(p(IRI('x')), p, IRI('x'))
        self.assert_statement(
            p(Item('u'), IRI('x')),
            Item('u'), ValueSnak(p, IRI('x')))
        self.assertRaises(TypeError, p, IRI('u'), IRI('x'))

    def test__from_rdflib(self):
        # bad argument: literal
        self.assertRaises(TypeError, Property._from_rdflib, Literal('x'))
        # bad argument: result is a IRI
        self.assertRaises(TypeError, Property._from_rdflib, URIRef('x'))
        # bad argument: result is an item
        self.assertRaises(TypeError, Property._from_rdflib, NS.WD.Q5)
        # good arguments
        self.assert_property(
            Property._from_rdflib(NS.WD.P31), IRI(NS.WD.P31))
        self.assert_property(
            Property._from_rdflib(NS.P.P31, property_prefixes=[NS.P]),
            IRI(NS.WD.P31))
        self.assert_property(
            Entity._from_rdflib(NS.P.P31, property_prefixes=[NS.P]),
            IRI(NS.WD.P31))

    def test__to_rdflib(self):
        self.assertEqual(Property(NS.WD.P31)._to_rdflib(), NS.WD.P31)


if __name__ == '__main__':
    main()
