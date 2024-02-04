# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, Lexeme, LexemeDatatype

from .tests import kif_TestCase, main


class TestModelLexemeDatatype(kif_TestCase):

    def test_sanity(self):
        self.assertIs(Datatype.lexeme, Lexeme.datatype)
        self.assertEqual(Datatype.lexeme, LexemeDatatype())

    def test__from_rdflib(self):
        self.assert_lexeme_datatype(
            LexemeDatatype._from_rdflib(NS.WIKIBASE.WikibaseLexeme))

    def test__to_rdflib(self):
        self.assertEqual(
            LexemeDatatype._to_rdflib(), NS.WIKIBASE.WikibaseLexeme)


if __name__ == '__main__':
    main()
