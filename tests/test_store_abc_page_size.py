# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import sys

from kif_lib import Items

from .tests import kif_EmptyStoreTestCase


class TestStoreABC_PageSize(kif_EmptyStoreTestCase):

    def test_page_size_defaults(self):
        kb = self.new_Store()
        self.assertEqual(kb.default_page_size, 100)
        self.assertEqual(kb.maximum_page_size, sys.maxsize)

    def test_page_size_init(self):
        kb = self.new_Store()
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb = self.new_Store(page_size=33)
        self.assertEqual(kb.page_size, 33)
        kb = self.new_Store(page_size=-1)
        self.assertEqual(kb.page_size, kb.default_page_size)

    def test_get_page_size(self):
        kb = self.new_Store()
        self.assertEqual(kb.get_page_size(), kb.default_page_size)
        self.assertEqual(kb.get_page_size(5), 5)
        kb = self.new_Store(page_size=0)
        self.assertEqual(kb.get_page_size(5), 0)
        kb = self.new_Store(page_size=-8)
        self.assertEqual(kb.get_page_size(5), 5)
        self.assertEqual(kb.get_page_size(), kb.default_page_size)
        kb = self.new_Store(page_size=33)
        self.assertEqual(kb.get_page_size(5), 33)

    def test_set_page_size(self):
        kb = self.new_Store()
        self.assert_raises_bad_argument(
            TypeError, 1, 'page_size', 'expected int, got str',
            kb.set_page_size, 'abc')
        self.assertEqual(kb.get_page_size(), kb.default_page_size)
        kb.page_size = 3
        self.assertEqual(kb.page_size, 3)
        kb.page_size = -1
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb.page_size = None
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb.set_page_size()
        self.assertEqual(kb.page_size, kb.default_page_size)
        kb.set_page_size(8)
        self.assertEqual(kb.page_size, 8)

    def test__batched(self):
        kb = self.new_Store()
        kb.page_size = 2
        it = kb._batched(Items('v', 'w', 'x', 'y', 'z'))
        self.assertEqual(next(it), tuple(Items('v', 'w')))
        self.assertEqual(next(it), tuple(Items('x', 'y')))
        self.assertEqual(next(it), tuple(Items('z')))
        self.assertRaises(StopIteration, next, it)


if __name__ == '__main__':
    TestStoreABC_PageSize.main()
