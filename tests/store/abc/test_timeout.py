# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.typing import Final

from ...tests import TestCase


class Test(TestCase):

    KB: Final[Store] = Store('empty')

    def test_default_timeout(self) -> None:
        self.assertEqual(
            self.KB.default_timeout,
            self.KB.context.options.store.timeout)
        self.assertEqual(
            self.KB.max_timeout,
            self.KB.context.options.store.max_timeout)

    def test__init_timeout(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb = Store('empty', timeout=33)
        self.assertEqual(kb.timeout, 33)
        kb = Store('empty', timeout=0)
        self.assertEqual(kb.timeout, 0.)
        kb = Store('empty', timeout=-1)
        self.assertEqual(kb.timeout, 0.)
        kb = Store('empty', timeout=None)
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb = Store('empty', timeout=kb.max_timeout + 10)
        self.assertEqual(kb.timeout, kb.max_timeout)

    def test_get_timeout(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.get_timeout(), kb.default_timeout)
        self.assertEqual(kb.get_timeout(44.), 44.)
        kb = Store('empty', timeout=0)
        self.assertEqual(kb.get_timeout(44), 0)
        kb = Store('empty', timeout=-8)
        self.assertEqual(kb.get_timeout(5), 0.0)
        kb = Store('empty', timeout=None)
        self.assertEqual(kb.get_timeout(), kb.default_timeout)
        kb = Store('empty', timeout=33.)
        self.assertEqual(kb.get_timeout(5), 33.)
        kb = Store('empty', timeout=None)
        self.assertEqual(kb.get_timeout(kb.max_timeout + 10), kb.max_timeout)

    def test_set_timeout(self) -> None:
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1, 'timeout', 'cannot coerce dict into Quantity',
            kb.set_timeout, {})
        self.assert_raises_bad_argument(
            ValueError, 1, 'timeout', 'cannot coerce str into Quantity',
            kb.set_timeout, 'abc')
        self.assertEqual(kb.get_timeout(), kb.default_timeout)
        kb.timeout = 3
        self.assertEqual(kb.timeout, 3)
        kb.timeout = -1
        self.assertEqual(kb.timeout, 0.0)
        kb.timeout = '33'     # type: ignore
        self.assertEqual(kb.timeout, 33)
        kb.timeout = 33.5
        self.assertEqual(kb.timeout, 33.5)
        kb.timeout = -1
        self.assertEqual(kb.timeout, 0)
        kb.timeout = None
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb.set_timeout()
        self.assertEqual(kb.timeout, kb.default_timeout)
        kb.set_timeout(8)
        self.assertEqual(kb.timeout, 8.)
        kb.set_timeout(kb.max_timeout + 10)
        self.assertEqual(kb.timeout, kb.max_timeout)


if __name__ == '__main__':
    Test.main()
