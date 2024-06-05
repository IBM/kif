# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import sys

from .tests import kif_EmptyStoreTestCase


class TestStoreABC_Timeout(kif_EmptyStoreTestCase):

    def test_timeout_defaults(self):
        kb = self.new_Store()
        self.assertIsNone(kb.default_timeout)
        self.assertEqual(kb.maximum_page_size, sys.maxsize)

    def test_timeout_init(self):
        kb = self.new_Store()
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb = self.new_Store(timeout=33)
        self.assertEqual(kb.timeout, 33)
        kb = self.new_Store(timeout=0)
        self.assertEqual(kb.timeout, 0)
        kb = self.new_Store(timeout=-1)
        self.assertEqual(kb.timeout, kb.default_timeout)

    def test_get_timeout(self):
        kb = self.new_Store()
        self.assertEqual(kb.get_timeout(), kb.default_timeout)
        self.assertEqual(kb.get_timeout(44.), 44.)
        kb = self.new_Store(timeout=0)
        self.assertEqual(kb.get_timeout(44), 0)
        kb = self.new_Store(timeout=-8)
        self.assertEqual(kb.get_timeout(5), 5)
        self.assertEqual(kb.get_timeout(), kb.default_timeout)
        kb = self.new_Store(timeout=33.)
        self.assertEqual(kb.get_timeout(5), 33.)

    def test_set_timeout(self):
        kb = self.new_Store()
        self.assert_raises_bad_argument(
            TypeError, 1, 'timeout', 'expected float or int, got str',
            kb.set_timeout, 'abc')
        self.assertEqual(kb.get_timeout(), kb.default_timeout)
        kb.timeout = 3
        self.assertEqual(kb.timeout, 3)
        kb.timeout = -1
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb.timeout = None
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb.set_timeout()
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb.set_timeout(8)
        self.assertEqual(kb.timeout, 8)


if __name__ == '__main__':
    TestStoreABC_Timeout.main()
