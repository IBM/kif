# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Store

from .tests import kif_StoreTestCase, main


class TestStoreFlags(kif_StoreTestCase):

    def test_flags_init(self):
        kb = Store('empty')
        self.assertEqual(kb.flags, kb.DEFAULT)
        kb = Store('empty', flags=0)
        self.assertEqual(kb.flags, kb.Flags(0))

    def test_get_flags(self):
        kb = Store('empty')
        self.assertEqual(kb.flags, kb.DEFAULT)
        self.assertEqual(kb.get_flags(), kb.flags)
        kb = Store('empty', flags=0)
        self.assertEqual(kb.flags, kb.Flags(0))
        self.assertEqual(kb.get_flags(), kb.flags)

    def test_set_flags(self):
        kb = Store('empty', flags=Store.Flags(0))
        self.assertEqual(kb.flags, kb.Flags(0))
        kb.set_flags(kb.CACHE)
        self.assertEqual(kb.flags, kb.CACHE)
        kb.flags |= kb.BEST_RANK
        self.assertEqual(kb.flags, kb.CACHE | kb.BEST_RANK)

    def test_has_flags(self):
        kb = Store('empty', flags=Store.Flags(0))
        self.assertEqual(kb.flags, kb.Flags(0))
        self.assertFalse(kb.has_flags(kb.CACHE))
        kb.set_flags(kb.CACHE | kb.BEST_RANK)
        self.assertTrue(kb.has_flags(kb.CACHE | kb.BEST_RANK))
        self.assertTrue(kb.has_flags(kb.CACHE))
        self.assertTrue(kb.has_flags(kb.BEST_RANK))

    def test_unset_flags(self):
        kb = Store('empty', flags=Store.Flags(0))
        self.assertEqual(kb.flags, kb.Flags(0))
        kb.unset_flags(kb.Flags(kb.BEST_RANK))
        self.assertEqual(kb.flags, kb.Flags(0))
        kb.flags |= kb.ALL
        kb.unset_flags(kb.BEST_RANK)
        self.assertTrue(kb.has_flags(kb.ALL & ~kb.BEST_RANK))


if __name__ == '__main__':
    main()
