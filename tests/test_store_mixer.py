# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import Statement, Store
from kif.store import MixerStore

from .data import ADAM_TTL, BENZENE_TTL, BRAZIL_TTL
from .tests import kif_TestCase, main


class TestMixerStore(kif_TestCase):

    def mk_empty_mixer(self):
        return Store('mixer')

    def mk_benzene_mixer(self):
        return Store('mixer', [Store('rdf', BENZENE_TTL)])

    def mk_adam_benzene_brazil_mixer(self):
        return Store(
            'mixer',
            [Store('rdf', ADAM_TTL),
             Store('rdf', BENZENE_TTL),
             Store('rdf', BRAZIL_TTL)])

    def test_sanity(self):
        self.store_sanity_checks(self.mk_empty_mixer())
        self.store_sanity_checks(self.mk_benzene_mixer())
        self.store_sanity_checks(self.mk_adam_benzene_brazil_mixer())

    def test__init__(self):
        # bad argument
        self.assertRaises(TypeError, Store, 'mixer', 0)
        self.assertRaises(
            TypeError, Store, 'mixer', Store('rdf', BENZENE_TTL))
        # good arguments
        kb = Store('mixer')
        self.assertIsInstance(kb, MixerStore)
        self.assertEqual(kb._flags, Store.ALL)

    def test_get_sources(self):
        kb = self.mk_empty_mixer()
        self.assertEqual(len(kb.sources), 0)
        kb = self.mk_benzene_mixer()
        self.assertEqual(len(kb.sources), 1)
        kb = self.mk_adam_benzene_brazil_mixer()
        self.assertEqual(len(kb.sources), 3)

    # -- Set interface -----------------------------------------------------

    def test__iter__(self):
        kb = self.mk_adam_benzene_brazil_mixer()
        stmt = next(iter(kb))
        self.assertIsInstance(stmt, Statement)
        it = iter(Store('mixer', kb.sources, page_size=1))
        for i in range(3):
            self.assertIsInstance(next(it), Statement)

    def test__len__(self):
        kb = self.mk_adam_benzene_brazil_mixer()
        self.assertEqual(len(kb), 15)

    # -- Queries -----------------------------------------------------------

    def test_contains(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_contains(self.mk_adam_benzene_brazil_mixer())

    def test_contains_any_rank(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_contains_any_rank(self.mk_adam_benzene_brazil_mixer())

    def test_count(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_count(self.mk_adam_benzene_brazil_mixer())

    def test_count_any_rank(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_count_any_rank(self.mk_adam_benzene_brazil_mixer())

    def test_filter(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_filter(self.mk_adam_benzene_brazil_mixer())

    def test_filter_any_rank(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_filter_any_rank(self.mk_adam_benzene_brazil_mixer())

    # -- Annotations -------------------------------------------------------

    def test_get_annotations(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_get_annotations(self.mk_adam_benzene_brazil_mixer())

    # -- Descriptor --------------------------------------------------------

    def test_get_descriptor(self):
        from .test_store_rdf import TestRDF_Store
        test = TestRDF_Store()
        test._test_get_descriptor(self.mk_adam_benzene_brazil_mixer())


if __name__ == '__main__':
    main()
