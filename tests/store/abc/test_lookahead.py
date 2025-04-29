# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.typing import Final

from ...tests import TestCase


class Test(TestCase):

    KB: Final[Store] = Store('empty')

    def test_default_lookahead(self) -> None:
        kb = Store('empty')
        self.assertEqual(
            kb.default_lookahead,
            kb.context.options.store.lookahead)

    def test__init__lookahead(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.lookahead, kb.default_lookahead)
        kb = Store('empty', lookahead=33)
        self.assertEqual(kb.lookahead, 33)
        kb = Store('empty', lookahead=-1)
        self.assertEqual(kb.lookahead, 1)
        kb = Store('empty', lookahead=0)
        self.assertEqual(kb.lookahead, 1)
        kb = Store('empty', lookahead=None)
        self.assertEqual(kb.lookahead, kb.default_lookahead)

    def test_get_lookahead(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.get_lookahead(), kb.default_lookahead)
        self.assertEqual(kb.get_lookahead(5), 5)
        kb = Store('empty', lookahead=0)
        self.assertEqual(kb.get_lookahead(5), 1)
        kb = Store('empty', lookahead=-8)
        self.assertEqual(kb.get_lookahead(5), 1)
        kb = Store('empty', lookahead=None)
        self.assertEqual(kb.get_lookahead(), kb.default_lookahead)

    def test_set_lookahead(self) -> None:
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1, 'lookahead', 'cannot coerce dict into Quantity',
            kb.set_lookahead, {})
        self.assert_raises_bad_argument(
            ValueError, 1, 'lookahead', 'cannot coerce str into Quantity',
            kb.set_lookahead, 'abc')
        self.assertEqual(kb.get_lookahead(), kb.default_lookahead)
        kb.lookahead = 3
        self.assertEqual(kb.lookahead, 3)
        kb.lookahead = '33'     # type: ignore
        self.assertEqual(kb.lookahead, 33)
        kb.lookahead = 33.5     # type: ignore
        self.assertEqual(kb.lookahead, 33)
        kb.lookahead = -1
        self.assertEqual(kb.lookahead, 1)
        kb.lookahead = None     # type: ignore
        self.assertEqual(kb.lookahead, kb.default_lookahead)
        kb.set_lookahead()
        self.assertEqual(kb.lookahead, kb.default_lookahead)
        kb.set_lookahead(8)
        self.assertEqual(kb.lookahead, 8)


if __name__ == '__main__':
    Test.main()
