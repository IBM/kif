# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

import kif_lib.namespace as NS
from kif_lib import Entity, IRI, Item, Items

from .tests import kif_TestCase, main


class TestItem(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, Item, 0)
        self.assert_item(Item('abc'), IRI('abc'))
        self.assert_item(Item(IRI('abc')), IRI('abc'))

    def test_Items(self):
        a, b, c = Items('a', IRI('b'), 'c')
        self.assert_item(a, IRI('a'))
        self.assert_item(b, IRI('b'))
        self.assert_item(c, IRI('c'))

    def test__from_rdflib(self):
        # bad argument: literal
        self.assertRaises(TypeError, Item._from_rdflib, Literal('x'))
        # bad argument: result is a IRI
        self.assertRaises(TypeError, Item._from_rdflib, URIRef('x'))
        # bad argument: result is a property
        self.assertRaises(TypeError, Item._from_rdflib, NS.WD.P31)
        # good arguments
        self.assert_item(Item._from_rdflib(NS.WD.Q5), IRI(NS.WD.Q5))
        self.assert_item(
            Item._from_rdflib(NS.WDT.Q5, [NS.WDT]), IRI(NS.WD.Q5))
        self.assert_item(
            Entity._from_rdflib(NS.WDT.Q5, [NS.WDT]), IRI(NS.WD.Q5))

    def test__to_rdflib(self):
        self.assertEqual(Item(NS.WD.Q5)._to_rdflib(), NS.WD.Q5)


if __name__ == '__main__':
    main()
