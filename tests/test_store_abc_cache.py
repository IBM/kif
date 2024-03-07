# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, Items, Property

from .tests import kif_EmptyStoreTestCase


class TestStoreABC_Cache(kif_EmptyStoreTestCase):

    def test__cache_init(self):
        kb = self.new_Store()
        self.assertTrue(kb._cache.enabled)
        kb = self.new_Store(flags=0)
        self.assertFalse(kb._cache.enabled)
        self.assertEqual(kb._cache.size, 0)

    def test__cache_get_presence(self):
        kb = self.new_Store()
        self.assertIsNone(kb._cache_get_presence(Item('x')))

    def test__cache_set_presence(self):
        kb = self.new_Store()
        x, y = Items('x', 'y')
        stmt = Property('p')(x, y)
        self.assertIsNone(kb._cache_get_presence(x))
        self.assertIs(kb._cache_set_presence(x, True), True)
        self.assertIs(kb._cache_get_presence(x), True)
        self.assertIs(kb._cache_set_presence(stmt, False), False)
        self.assertIs(kb._cache_get_presence(stmt), False)
        self.assertIs(kb._cache_set_presence(x, None), None)
        self.assertIsNone(kb._cache_get_presence(x))
        self.assertEqual(kb._cache.size, 1)


if __name__ == '__main__':
    TestStoreABC_Cache.main()
