# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, Lexeme, Property, Store

from .tests import kif_StoreTestCase, main


class TestStoreDescriptors(kif_StoreTestCase):

    item = Item('Q')

    property = Property('P')

    lexeme = Lexeme('L')

    def test_get_item_descriptor(self):
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1, 'items', 'expected Item or Iterable, got int',
            kb.get_item_descriptor, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'language', 'expected str, got int',
            kb.get_item_descriptor, self.item, 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'descriptor_mask',
            'expected PlainDescriptor.AttributeMask or int, got str',
            kb.get_item_descriptor, self.item, 'pt', 'abc')

    def test_get_property_descriptor(self):
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1,
            'properties', 'expected Iterable or Property, got int',
            kb.get_property_descriptor, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'language', 'expected str, got int',
            kb.get_property_descriptor, self.property, 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'descriptor_mask',
            'expected PlainDescriptor.AttributeMask or int, got str',
            kb.get_property_descriptor, self.property, 'pt', 'abc')

    def test_get_lexeme_descriptor(self):
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1,
            'lexemes', 'expected Iterable or Lexeme, got int',
            kb.get_lexeme_descriptor, 0)


if __name__ == '__main__':
    main()
