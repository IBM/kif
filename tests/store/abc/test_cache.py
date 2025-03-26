# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Item, Items, Property, Store

from ...tests import TestCase


class Test(TestCase):

    def test__init_cache(self) -> None:
        kb = Store('empty')
        self.assertTrue(kb._cache.enabled)
        kb = Store('empty', flags=0)
        self.assertFalse(kb._cache.enabled)
        self.assertEqual(kb._cache.size, 0)

    def test__cache_get_presence(self) -> None:
        kb = Store('empty')
        self.assertIsNone(kb._cache_get_presence(Item('x')))

    def test__cache_set_presence(self) -> None:
        kb = Store('empty')
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
    Test.main()
