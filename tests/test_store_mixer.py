# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Statement, Store
from kif_lib.store.mixer import MixerStore
from kif_lib.typing import cast

from .data import ADAM_TTL, BENZENE_TTL, BRAZIL_TTL
from .tests import StoreTestCase


class TestStoreMixer(StoreTestCase):

    def mk_empty_mixer(self) -> MixerStore:
        return cast(MixerStore, Store('mixer'))

    def mk_benzene_mixer(self) -> MixerStore:
        return cast(MixerStore, Store('mixer', [Store('rdf', BENZENE_TTL)]))

    def mk_adam_benzene_brazil_mixer(self) -> MixerStore:
        return cast(MixerStore, Store(
            'mixer',
            [Store('rdf', ADAM_TTL),
             Store('rdf', BENZENE_TTL),
             Store('rdf', BRAZIL_TTL)]))

    def test_sanity(self) -> None:
        self.store_sanity_checks(self.mk_empty_mixer())
        self.store_sanity_checks(self.mk_benzene_mixer())
        self.store_sanity_checks(self.mk_adam_benzene_brazil_mixer())

    def test_get_sources(self) -> None:
        kb = self.mk_empty_mixer()
        self.assertEqual(len(kb.sources), 0)
        kb = self.mk_benzene_mixer()
        self.assertEqual(len(kb.sources), 1)
        kb = self.mk_adam_benzene_brazil_mixer()
        self.assertEqual(len(kb.sources), 3)

    def test__iter__(self) -> None:
        kb = self.mk_adam_benzene_brazil_mixer()
        stmt = next(iter(kb))
        self.assertIsInstance(stmt, Statement)
        it = iter(Store('mixer', kb.sources, page_size=1))
        for _ in range(3):
            self.assertIsInstance(next(it), Statement)

    def test__len__(self) -> None:
        kb = self.mk_adam_benzene_brazil_mixer()
        self.assertEqual(len(kb), 15)

    def test_contains(self) -> None:
        from .test_store_rdf import TestStoreRDF
        test = TestStoreRDF()
        test._test_contains(self.mk_adam_benzene_brazil_mixer())

    def test_contains_any_rank(self) -> None:
        from .test_store_rdf import TestStoreRDF
        test = TestStoreRDF()
        test._test_contains_any_rank(self.mk_adam_benzene_brazil_mixer())

    def test_count(self) -> None:
        from .test_store_rdf import TestStoreRDF
        test = TestStoreRDF()
        test._test_count(self.mk_adam_benzene_brazil_mixer())

    def test_count_any_rank(self) -> None:
        from .test_store_rdf import TestStoreRDF
        test = TestStoreRDF()
        test._test_count_any_rank(self.mk_adam_benzene_brazil_mixer())

    def test_filter(self) -> None:
        from .test_store_rdf import TestStoreRDF
        test = TestStoreRDF()
        test._test_filter_tail(self.mk_adam_benzene_brazil_mixer())

    def test_filter_any_rank(self) -> None:
        from .test_store_rdf import TestStoreRDF
        test = TestStoreRDF()
        test._test_filter_any_rank(self.mk_adam_benzene_brazil_mixer())

    def test_get_annotations(self) -> None:
        from .test_store_rdf import TestStoreRDF
        test = TestStoreRDF()
        test._test_get_annotations(self.mk_adam_benzene_brazil_mixer())


if __name__ == '__main__':
    TestStoreMixer.main()
