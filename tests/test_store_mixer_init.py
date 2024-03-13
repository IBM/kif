# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Store
from kif_lib.store.mixer import MixerStore

from .tests import kif_StoreTestCase


class TestStoreMixer_Init(kif_StoreTestCase):

    def test__init__(self):
        # bad argument: sources
        self.assert_raises_bad_argument(
            TypeError, 2, 'sources', 'expected Iterable, got int',
            MixerStore, 'mixer', 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'sources', 'expected Iterable[Store]',
            MixerStore, 'mixer', [0])
        # success
        kb = Store('mixer')
        self.assertEqual(kb.sources, [])
        sources = (Store('empty'), Store('empty'))
        kb = Store('mixer', sources)
        self.assertEqual(kb.sources, list(sources))


if __name__ == '__main__':
    TestStoreMixer_Init.main()
