# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, Lexeme, LexemeDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueLexemeDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_lexeme_datatype(
            LexemeDatatype._from_rdflib(WIKIBASE.WikibaseLexeme))

    def test__to_rdflib(self):
        self.assertEqual(LexemeDatatype._to_rdflib(), WIKIBASE.WikibaseLexeme)

    def test_from_value_class(self):
        self.assert_lexeme_datatype(Datatype.from_value_class(Lexeme))

    def test_to_value_class(self):
        self.assertIs(LexemeDatatype().to_value_class(), Lexeme)


if __name__ == '__main__':
    TestModelValueLexemeDatatype.main()
