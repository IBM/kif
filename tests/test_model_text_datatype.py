# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, Text, TextDatatype

from .tests import kif_TestCase, main


class TestModelTextDatatype(kif_TestCase):

    def test_sanity(self):
        self.assertIs(Datatype.text, Text.datatype)
        self.assertEqual(Datatype.text, TextDatatype())

    def test__from_rdflib(self):
        self.assert_text_datatype(
            TextDatatype._from_rdflib(NS.WIKIBASE.Monolingualtext))

    def test__to_rdflib(self):
        self.assertEqual(
            TextDatatype._to_rdflib(), NS.WIKIBASE.Monolingualtext)


if __name__ == '__main__':
    main()
