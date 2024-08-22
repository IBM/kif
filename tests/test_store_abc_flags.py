# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Store

from .tests import EmptyStoreTestCase


class TestStoreABC_Flags(EmptyStoreTestCase):

    def test_flags_default(self) -> None:
        kb = self.new_Store()
        self.assertEqual(
            kb.default_flags,
            kb.Flags.ALL & ~(kb.DEBUG | kb.ORDER))

    def test_flags_init(self) -> None:
        kb = self.new_Store()
        self.assertEqual(kb.flags, kb.default_flags)
        kb = self.new_Store(flags=0)
        self.assertEqual(kb.flags, kb.Flags(0))

    def test_get_flags(self) -> None:
        kb = self.new_Store()
        self.assertEqual(kb.flags, kb.default_flags)
        self.assertEqual(kb.get_flags(), kb.flags)
        kb = self.new_Store(flags=0)
        self.assertEqual(kb.flags, kb.Flags(0))
        self.assertEqual(kb.get_flags(), kb.flags)

    def test_set_flags(self) -> None:
        kb = self.new_Store(flags=Store.Flags(0))
        self.assertEqual(kb.flags, kb.Flags(0))
        kb.set_flags(kb.CACHE)
        self.assertEqual(kb.flags, kb.CACHE)
        kb.flags |= kb.BEST_RANK
        self.assertEqual(kb.flags, kb.CACHE | kb.BEST_RANK)

    def test_has_flags(self) -> None:
        kb = self.new_Store(flags=Store.Flags(0))
        self.assertEqual(kb.flags, kb.Flags(0))
        self.assertFalse(kb.has_flags(kb.CACHE))
        kb.set_flags(kb.CACHE | kb.BEST_RANK)
        self.assertTrue(kb.has_flags(kb.CACHE | kb.BEST_RANK))
        self.assertTrue(kb.has_flags(kb.CACHE))
        self.assertTrue(kb.has_flags(kb.BEST_RANK))

    def test_unset_flags(self) -> None:
        kb = self.new_Store(flags=Store.Flags(0))
        self.assertEqual(kb.flags, kb.Flags(0))
        kb.unset_flags(kb.Flags(kb.BEST_RANK))
        self.assertEqual(kb.flags, kb.Flags(0))
        kb.flags |= kb.Flags.ALL
        kb.unset_flags(kb.BEST_RANK)
        self.assertTrue(kb.has_flags(kb.Flags.ALL & ~kb.BEST_RANK))


if __name__ == '__main__':
    TestStoreABC_Flags.main()
