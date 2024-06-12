# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

from kif_lib import Entity, IRI, Item, Items
from kif_lib.namespace import WD, WDT
from kif_lib.typing import cast

from .tests import kif_TestCase


class TestModelValueItem(kif_TestCase):

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
        # bad argument: result is an IRI
        self.assertRaises(TypeError, Item._from_rdflib, URIRef('x'))
        # bad argument: result is a property
        self.assertRaises(TypeError, Item._from_rdflib, WD.P31)
        # good arguments
        self.assert_item(cast(Item, Item._from_rdflib(WD.Q5)), IRI(WD.Q5))
        self.assert_item(
            cast(Item, Item._from_rdflib(WDT.Q5, [WDT])), IRI(WD.Q5))
        self.assert_item(
            cast(Item, Entity._from_rdflib(WDT.Q5, [WDT])), IRI(WD.Q5))

    def test__to_rdflib(self):
        self.assertEqual(Item(WD.Q5)._to_rdflib(), WD.Q5)


if __name__ == '__main__':
    TestModelValueItem.main()
