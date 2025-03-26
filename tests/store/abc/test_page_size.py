# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Items, Store
from kif_lib.typing import Final

from ...tests import TestCase


class Test(TestCase):

    KB: Final[Store] = Store('empty')

    def test_default_page_size(self) -> None:
        kb = Store('empty')
        self.assertEqual(
            kb.default_page_size,
            kb.context.options.store.page_size)
        self.assertEqual(
            kb.max_page_size,
            kb.context.options.store.max_page_size)

    def test__init_page_size(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb = Store('empty', page_size=33)
        self.assertEqual(kb.page_size, 33)
        kb = Store('empty', page_size=-1)
        self.assertEqual(kb.page_size, 0)
        kb = Store('empty', page_size=None)
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb = Store('empty', page_size=kb.max_page_size + 10)
        self.assertEqual(kb.page_size, kb.max_page_size)

    def test_get_page_size(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.get_page_size(), kb.default_page_size)
        self.assertEqual(kb.get_page_size(5), 5)
        kb = Store('empty', page_size=0)
        self.assertEqual(kb.get_page_size(5), 0)
        kb = Store('empty', page_size=-8)
        self.assertEqual(kb.get_page_size(5), 0)
        kb = Store('empty', page_size=None)
        self.assertEqual(kb.get_page_size(), kb.default_page_size)
        kb = Store('empty', page_size=None)
        self.assertEqual(
            kb.get_page_size(kb.max_page_size + 10), kb.max_page_size)

    def test_set_page_size(self) -> None:
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1, 'page_size', 'cannot coerce dict into Quantity',
            kb.set_page_size, {})
        self.assert_raises_bad_argument(
            ValueError, 1, 'page_size', 'cannot coerce str into Quantity',
            kb.set_page_size, 'abc')
        self.assertEqual(kb.get_page_size(), kb.default_page_size)
        kb.page_size = 3
        self.assertEqual(kb.page_size, 3)
        kb.page_size = '33'     # type: ignore
        self.assertEqual(kb.page_size, 33)
        kb.page_size = 33.5     # type: ignore
        self.assertEqual(kb.page_size, 33)
        kb.page_size = -1
        self.assertEqual(kb.page_size, 0)
        kb.page_size = None     # type: ignore
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb.set_page_size()
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb.set_page_size(8)
        self.assertEqual(kb.page_size, 8)
        kb.set_page_size(kb.max_page_size + 10)
        self.assertEqual(kb.page_size, kb.max_page_size)

    def test__batched(self) -> None:
        kb = Store('empty')
        kb.page_size = 2
        it = kb._batched(Items('v', 'w', 'x', 'y', 'z'))
        self.assertEqual(next(it), tuple(Items('v', 'w')))
        self.assertEqual(next(it), tuple(Items('x', 'y')))
        self.assertEqual(next(it), tuple(Items('z')))
        self.assertRaises(StopIteration, next, it)


if __name__ == '__main__':
    Test.main()
