# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

from kif_lib import Entity, IRI, Item, Properties, Property, ValueSnak
from kif_lib.namespace import P, WD
from kif_lib.typing import cast

from .tests import kif_TestCase


class TestModelValueProperty(kif_TestCase):

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
        # bad argument: result is an IRI
        self.assertRaises(TypeError, Property._from_rdflib, URIRef('x'))
        # bad argument: result is an item
        self.assertRaises(TypeError, Property._from_rdflib, WD.Q5)
        # good arguments
        self.assert_property(
            cast(Property, Property._from_rdflib(WD.P31)), IRI(WD.P31))
        self.assert_property(
            cast(Property, Property._from_rdflib(
                P.P31, property_prefixes=[P])),
            IRI(WD.P31))
        self.assert_property(
            cast(Property, Entity._from_rdflib(
                P.P31, property_prefixes=[P])),
            IRI(WD.P31))

    def test__to_rdflib(self):
        self.assertEqual(Property(WD.P31)._to_rdflib(), WD.P31)


if __name__ == '__main__':
    TestModelValueProperty.main()
