# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, Items, Property, Store

from .tests import kif_StoreTestCase, main


class TestStoreCache(kif_StoreTestCase):

    def test__cache_init(self):
        kb = Store('empty')
        self.assertTrue(kb._cache.enabled)
        kb = Store('empty', flags=0)
        self.assertFalse(kb._cache.enabled)
        self.assertEqual(kb._cache.size, 0)

    def test__cache_get_occurrence(self):
        kb = Store('empty')
        self.assertIsNone(kb._cache_get_occurrence(Item('x')))

    def test__cache_set_occurrence(self):
        kb = Store('empty')
        x, y = Items('x', 'y')
        stmt = Property('p')(x, y)
        self.assertIsNone(kb._cache_get_occurrence(x))
        self.assertIs(kb._cache_set_occurrence(x, True), True)
        self.assertIs(kb._cache_get_occurrence(x), True)
        self.assertIs(kb._cache_set_occurrence(stmt, False), False)
        self.assertIs(kb._cache_get_occurrence(stmt), False)
        self.assertIs(kb._cache_set_occurrence(x, None), None)
        self.assertIsNone(kb._cache_get_occurrence(x))
        self.assertEqual(kb._cache.size, 1)


if __name__ == '__main__':
    main()
