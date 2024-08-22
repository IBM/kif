# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.cache import Cache
from kif_lib.typing import assert_type

from .tests import TestCase


class Test(TestCase):

    def test__init__(self) -> None:
        c = Cache()
        self.assertIsInstance(c, Cache)
        assert_type(c, Cache)
        self.assertTrue(c.enabled)
        self.assertEqual(c.size, 0)
        c = Cache(False)
        self.assertIsInstance(c, Cache)
        self.assertFalse(c.enabled)
        self.assertEqual(c.size, 0)

    def test_enable(self) -> None:
        c = Cache(False)
        self.assertFalse(c.enabled)
        self.assertFalse(c.is_enabled())
        self.assertTrue(c.disabled)
        self.assertTrue(c.is_disabled())
        c.enable()
        self.assertTrue(c.enabled)
        self.assertTrue(c.is_enabled())
        self.assertFalse(c.disabled)
        self.assertFalse(c.is_disabled())

    def test_disable(self) -> None:
        c = Cache(True)
        self.assertTrue(c.enabled)
        self.assertTrue(c.is_enabled())
        self.assertFalse(c.disabled)
        self.assertFalse(c.is_disabled())
        c.disable()
        self.assertFalse(c.enabled)
        self.assertFalse(c.is_enabled())
        self.assertTrue(c.disabled)
        self.assertTrue(c.is_disabled())

    def test_clear(self) -> None:
        c = Cache()
        c.set(0, 'x', 1)
        self.assertEqual(c.size, 1)
        c.clear()
        self.assertEqual(c.size, 0)

    def test_get(self) -> None:
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

    def test_set(self) -> None:
        c = Cache()
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

    def test_unset(self) -> None:
        c = Cache()
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
    Test.main()
