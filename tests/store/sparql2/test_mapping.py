# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.compiler.sparql.mapping.pubchem import PubChemMapping
from kif_lib.compiler.sparql.mapping.wikidata import WikidataMapping

from ...tests import SPARQL_Store2TestCase


class Test(SPARQL_Store2TestCase):

    def test_default_mapping(self) -> None:
        kb = self.new_Store()
        self.assertIsInstance(kb.default_mapping, WikidataMapping)

    def test__init_mapping(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'mapping', 'expected SPARQL_Mapping, got int',
            (self.new_Store, 'SPARQL_Store2'), mapping=0)
        kb = self.new_Store()
        self.assertIsInstance(kb.mapping, WikidataMapping)
        mapping = PubChemMapping()
        kb = self.new_Store(mapping=mapping)
        self.assertEqual(kb.mapping, mapping)

    def test_get_mapping(self) -> None:
        mapping = PubChemMapping()
        kb = self.new_Store(mapping=mapping)
        self.assertEqual(kb.get_mapping(), mapping)
        self.assertEqual(kb.mapping, mapping)

if __name__ == '__main__':
    Test.main()
