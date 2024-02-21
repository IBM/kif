# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Items, Lexemes, Properties, Store

from .tests import kif_StoreTestCase, main


class TestEmptyStoreDescriptors(kif_StoreTestCase):

    item = list(Items('Q1', 'Q2', 'Q3'))

    property = list(Properties('P1', 'P2', 'P3'))

    lexeme = list(Lexemes('L1', 'L2', 'L3'))

    def test_get_item_descriptor(self):
        kb = Store('empty')
        desc = dict(kb.get_item_descriptor([]))
        self.assertEqual(desc, dict())
        desc = dict(kb.get_item_descriptor(self.item[0]))
        self.assertEqual(desc, {self.item[0]: None})
        desc = dict(kb.get_item_descriptor(self.item, 'pt'))
        self.assertEqual(desc, {
            self.item[0]: None,
            self.item[1]: None,
            self.item[2]: None,
        })
        desc = dict(kb.get_item_descriptor(self.item[1:], descriptor_mask=0))
        self.assertEqual(desc, {
            self.item[1]: None,
            self.item[2]: None,
        })

    def test_get_property_descriptor(self):
        kb = Store('empty')
        desc = dict(kb.get_property_descriptor([]))
        self.assertEqual(desc, dict())
        desc = dict(kb.get_property_descriptor(self.property[0]))
        self.assertEqual(desc, {self.property[0]: None})
        desc = dict(kb.get_property_descriptor(self.property, 'pt'))
        self.assertEqual(desc, {
            self.property[0]: None,
            self.property[1]: None,
            self.property[2]: None,
        })
        desc = dict(kb.get_property_descriptor(
            self.property[1:], descriptor_mask=0))
        self.assertEqual(desc, {
            self.property[1]: None,
            self.property[2]: None,
        })

    def test_get_lexeme_descriptor(self):
        kb = Store('empty')
        desc = dict(kb.get_lexeme_descriptor([]))
        self.assertEqual(desc, dict())
        desc = dict(kb.get_lexeme_descriptor(self.lexeme[0]))
        self.assertEqual(desc, {self.lexeme[0]: None})
        desc = dict(kb.get_lexeme_descriptor(self.lexeme))
        self.assertEqual(desc, {
            self.lexeme[0]: None,
            self.lexeme[1]: None,
            self.lexeme[2]: None,
        })
        desc = dict(kb.get_lexeme_descriptor(self.lexeme[1:]))
        self.assertEqual(desc, {
            self.lexeme[1]: None,
            self.lexeme[2]: None,
        })


if __name__ == '__main__':
    main()
