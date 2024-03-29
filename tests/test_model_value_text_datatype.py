# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, Text, TextDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueTextDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_text_datatype(
            TextDatatype._from_rdflib(WIKIBASE.Monolingualtext))

    def test__to_rdflib(self):
        self.assertEqual(TextDatatype._to_rdflib(), WIKIBASE.Monolingualtext)

    def test_from_value_class(self):
        self.assert_text_datatype(Datatype.from_value_class(Text))

    def test_to_value_class(self):
        self.assertIs(TextDatatype().to_value_class(), Text)


if __name__ == '__main__':
    TestModelValueTextDatatype.main()
