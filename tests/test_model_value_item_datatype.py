# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, Item, ItemDatatype

from .tests import kif_TestCase, main


class TestItemDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_item_datatype(
            ItemDatatype._from_rdflib(NS.WIKIBASE.WikibaseItem))

    def test__to_rdflib(self):
        self.assertEqual(
            ItemDatatype._to_rdflib(), NS.WIKIBASE.WikibaseItem)

    def test_from_value_class(self):
        self.assert_item_datatype(Datatype.from_value_class(Item))

    def test_to_value_class(self):
        self.assertIs(ItemDatatype().to_value_class(), Item)


if __name__ == '__main__':
    main()
