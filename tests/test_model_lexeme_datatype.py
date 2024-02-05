# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Lexeme, LexemeDatatype

from .tests import kif_TestCase, main


class TestModelLexemeDatatype(kif_TestCase):

    def test_value_class(self):
        self.assert_datatype_value_class(LexemeDatatype, Lexeme, 'lexeme')

    def test__from_rdflib(self):
        self.assert_lexeme_datatype(
            LexemeDatatype._from_rdflib(NS.WIKIBASE.WikibaseLexeme))

    def test__to_rdflib(self):
        self.assertEqual(
            LexemeDatatype._to_rdflib(), NS.WIKIBASE.WikibaseLexeme)


if __name__ == '__main__':
    main()
