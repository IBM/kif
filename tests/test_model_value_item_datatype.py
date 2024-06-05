# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import ItemDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueItemDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_item_datatype(
            ItemDatatype._from_rdflib(WIKIBASE.WikibaseItem))

    def test__to_rdflib(self):
        self.assertEqual(ItemDatatype._to_rdflib(), WIKIBASE.WikibaseItem)


if __name__ == '__main__':
    TestModelValueItemDatatype.main()
