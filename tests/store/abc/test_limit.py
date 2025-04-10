# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store

from ...tests import TestCase


class Test(TestCase):

    def test_default_limit(self) -> None:
        kb = Store('empty')
        self.assertEqual(
            kb.default_limit,
            kb.context.options.store.limit)
        self.assertEqual(
            kb.max_limit,
            kb.context.options.store.max_limit)

    def test__init__limit(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.limit, kb.default_limit)
        kb = Store('empty', limit=33)
        self.assertEqual(kb.limit, 33)
        kb = Store('empty', limit=-1)
        self.assertEqual(kb.limit, 0)
        kb = Store('empty', limit=None)
        self.assertEqual(kb.limit, kb.default_limit)
        kb = Store('empty', limit=kb.max_limit + 10)
        self.assertEqual(kb.limit, kb.max_limit)

    def test_get_limit(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.get_limit(), kb.default_limit)
        self.assertEqual(kb.get_limit(5), 5)
        kb = Store('empty', limit=0)
        self.assertEqual(kb.get_limit(5), 0)
        kb = Store('empty', limit=-8)
        self.assertEqual(kb.get_limit(5), 0)
        kb = Store('empty', limit=None)
        self.assertEqual(kb.get_limit(), kb.default_limit)
        kb = Store('empty', limit=None)
        self.assertEqual(
            kb.get_limit(kb.max_limit + 10), kb.max_limit)

    def test_set_limit(self) -> None:
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1, 'limit', 'cannot coerce dict into Quantity',
            kb.set_limit, {})
        self.assert_raises_bad_argument(
            ValueError, 1, 'limit', 'cannot coerce str into Quantity',
            kb.set_limit, 'abc')
        self.assertEqual(kb.get_limit(), kb.default_limit)
        kb.limit = 3
        self.assertEqual(kb.limit, 3)
        kb.limit = '33'     # type: ignore
        self.assertEqual(kb.limit, 33)
        kb.limit = 33.5     # type: ignore
        self.assertEqual(kb.limit, 33)
        kb.limit = -1
        self.assertEqual(kb.limit, 0)
        kb.limit = None     # type: ignore
        self.assertEqual(kb.limit, kb.default_limit)
        kb.set_limit()
        self.assertEqual(kb.limit, kb.default_limit)
        kb.set_limit(8)
        self.assertEqual(kb.limit, 8)
        kb.set_limit(kb.max_limit + 10)
        self.assertEqual(kb.limit, kb.max_limit)


if __name__ == '__main__':
    Test.main()
