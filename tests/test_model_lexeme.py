# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

import kif_lib.namespace as NS
from kif_lib import Entity, IRI, Lexeme, Lexemes

from .tests import kif_TestCase, main


class TestModelItem(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, Lexeme, 0)
        self.assert_lexeme(Lexeme('abc'), IRI('abc'))
        self.assert_lexeme(Lexeme(IRI('abc')), IRI('abc'))

    def test_Lexemes(self):
        a, b, c = Lexemes('a', IRI('b'), 'c')
        self.assert_lexeme(a, IRI('a'))
        self.assert_lexeme(b, IRI('b'))
        self.assert_lexeme(c, IRI('c'))

    def test__from_rdflib(self):
        # bad argument: literal
        self.assertRaises(TypeError, Lexeme._from_rdflib, Literal('x'))
        # bad argument: result is a IRI
        self.assertRaises(TypeError, Lexeme._from_rdflib, URIRef('x'))
        # bad argument: result is an item
        self.assertRaises(TypeError, Lexeme._from_rdflib, NS.WD.Q5)
        # bad argument: result is a property
        self.assertRaises(TypeError, Lexeme._from_rdflib, NS.WD.P31)
        # good arguments
        self.assert_lexeme(Lexeme._from_rdflib(NS.WD.L3873), IRI(NS.WD.L3873))
        self.assert_lexeme(
            Lexeme._from_rdflib(NS.WDT.L3873, lexeme_prefixes=[NS.WDT]),
            IRI(NS.WD.L3873))
        self.assert_lexeme(
            Entity._from_rdflib(NS.WDT.L3873, lexeme_prefixes=[NS.WDT]),
            IRI(NS.WD.L3873))

    def test__to_rdflib(self):
        self.assertEqual(Lexeme(NS.WD.L3873)._to_rdflib(), NS.WD.L3873)


if __name__ == '__main__':
    main()
