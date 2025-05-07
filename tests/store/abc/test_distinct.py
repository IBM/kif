# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.typing import Final

from ...tests import TestCase


class Test(TestCase):

    KB: Final[Store] = Store('empty')

    def test_default_distinct(self) -> None:
        kb = Store('empty')
        self.assertEqual(
            kb.default_distinct,
            kb.context.options.store.distinct)

    def test__init__distinct(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.distinct, kb.default_distinct)
        kb = Store('empty', distinct=False)
        self.assertEqual(kb.distinct, False)
        kb = Store('empty', distinct=True)
        self.assertEqual(kb.distinct, True)

    def test_get_distinct(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.get_distinct(), kb.default_distinct)
        kb = Store('empty', distinct=True)
        self.assertEqual(kb.get_distinct(), True)
        kb = Store('empty', distinct=False)
        self.assertEqual(kb.get_distinct(), False)
        kb = Store('empty', distinct=None)
        self.assertEqual(kb.get_distinct(), kb.default_distinct)

    def test_set_distinct(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.get_distinct(), kb.default_distinct)
        kb = Store('empty', distinct=0)  # type: ignore
        self.assertEqual(kb.get_distinct(), False)
        kb = Store('empty', distinct=1)  # type: ignore
        self.assertEqual(kb.get_distinct(), True)
        kb = Store('empty')
        kb.distinct = False
        self.assertEqual(kb.distinct, False)
        kb.distinct = True
        self.assertEqual(kb.distinct, True)
        kb.distinct = False
        self.assertEqual(kb.distinct, False)
        kb.distinct = None      # type: ignore
        self.assertEqual(kb.distinct, kb.default_distinct)


if __name__ == '__main__':
    Test.main()
