# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.cache import Cache

from .tests import kif_TestCase, main


class TestCache(kif_TestCase):

    def test__init__(self):
        c = Cache()
        self.assertIsInstance(c, Cache)
        self.assertTrue(c.enabled)
        self.assertEqual(c.size, 0)
        c = Cache(False)
        self.assertIsInstance(c, Cache)
        self.assertFalse(c.enabled)
        self.assertEqual(c.size, 0)

    def test_enable(self):
        c = Cache(False)
        self.assertFalse(c.enabled)
        c.enable()
        self.assertTrue(c.enabled)

    def test_disable(self):
        c = Cache(True)
        self.assertTrue(c.enabled)
        c.disable()
        self.assertFalse(c.enabled)

    def test_clear(self):
        c = Cache()
        c.set(0, 'x', 1)
        self.assertEqual(c.size, 1)
        c.clear()
        self.assertEqual(c.size, 0)

    def test_get(self):
        c = Cache()
        self.assertIsNone(c.get(0, 'x'))
        c.set(0, 'x', 1)
        self.assertEqual(c.get(0, 'x'), 1)
        c.set(0, 'x', 2)
        self.assertEqual(c.get(0, 'x'), 2)
        c.set(0, 'y', 1)
        self.assertEqual(c.get(0, 'y'), 1)
        self.assertIsNone(c.get(0, 'z'))
        self.assertIsNone(c.get(1, 'x'))
        c.set(1, 'x', 1)
        self.assertEqual(c.get(1, 'x'), 1)
        self.assertEqual(c.size, 2)
        c.disable()
        self.assertIsNone(c.get(1, 'x'))
        c.enable()
        self.assertEqual(c.get(1, 'x'), 1)
        self.assertEqual(c.size, 2)
        c.clear()
        self.assertEqual(c.size, 0)

    def test_set(self):
        c = Cache(self)
        self.assertEqual(c.set(0, 'x', 1), 1)
        self.assertEqual(c.size, 1)
        self.assertEqual(c.set(0, 'x', None), None)
        self.assertEqual(c.size, 1)
        self.assertEqual(c.get(0, 'x'), None)
        self.assertEqual(c.set(0, 'x', 1), 1)
        self.assertEqual(c.size, 1)
        self.assertEqual(c.get(0, 'x'), 1)
        c.disable()
        self.assertEqual(c.set(0, 'x', 2), 2)
        c.enable()
        self.assertEqual(c.get(0, 'x'), 1)
        self.assertEqual(c.set(0, 'x', 2), 2)
        self.assertEqual(c.size, 1)

    def test_unset(self):
        c = Cache(self)
        c.set(0, 'x', 1)
        c.set(1, 'y', 1)
        self.assertEqual(c.get(0, 'x'), 1)
        self.assertEqual(c.size, 2)
        self.assertEqual(c.unset(0, 'x'), 1)
        self.assertIsNone(c.get(0, 'x'))
        self.assertEqual(c.size, 1)
        self.assertIsNone(c.unset(3, 'x'))
        self.assertIsNone(c.unset(1, 'z'))
        self.assertIsNone(c.unset(0, 'x'))
        self.assertEqual(c.unset(1, 'y'), 1)
        self.assertEqual(c.size, 0)
        c.set(0, 'x', 1)
        self.assertEqual(c.size, 1)
        c.disable()
        self.assertIsNone(c.unset(0, 'x'))
        self.assertEqual(c.size, 1)
        c.enable()
        self.assertEqual(c.unset(0, 'x'), 1)
        self.assertEqual(c.size, 0)
        c.set(0, 'x', 1)
        c.set(0, 'y', 2)
        c.set(1, 'x', 1)
        self.assertEqual(c.size, 2)
        self.assertEqual(c.unset(0), {'x': 1, 'y': 2})
        self.assertEqual(c.size, 1)


if __name__ == '__main__':
    main()
