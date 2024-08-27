# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.store.mixer import MixerStore
from kif_lib.typing import cast

from .tests import StoreTestCase


class TestStoreMixer_Init(StoreTestCase):

    def test__init__(self) -> None:
        # bad argument: sources
        self.assert_raises_bad_argument(
            TypeError, 2, 'sources', 'expected Iterable, got int',
            MixerStore, 'mixer', 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'sources', 'expected Iterable[Store]',
            MixerStore, 'mixer', [0])
        # success
        kb = cast(MixerStore, Store('mixer'))
        self.assertEqual(kb.sources, [])
        sources = (Store('empty'), Store('empty'))
        kb = cast(MixerStore, Store('mixer', sources))
        self.assertEqual(kb.sources, list(sources))


if __name__ == '__main__':
    TestStoreMixer_Init.main()
