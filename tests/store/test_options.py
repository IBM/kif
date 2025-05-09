# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os

from kif_lib import Context, Property, ReferenceRecord, ReferenceRecordSet
from kif_lib.store.options import StoreOptions
from kif_lib.typing import assert_type, Optional

from ..tests import TestCase


class Test(TestCase):

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            assert_type(opts, StoreOptions)
            # extra_references
            assert_type(opts.extra_references, ReferenceRecordSet)
            self.assertEqual(opts.extra_references, ReferenceRecordSet())
            # max_page_size
            assert_type(opts.max_page_size, int)
            self.assertEqual(opts.max_page_size, opts._v_max_page_size[1])
            # page_size
            assert_type(opts.page_size, int)
            self.assertEqual(opts.page_size, opts._v_page_size[1])
            # max_timeout
            assert_type(opts.max_timeout, float)
            self.assertEqual(opts.max_timeout, opts._v_max_timeout[1])
            # timeout
            assert_type(opts.timeout, Optional[float])
            self.assertEqual(opts.timeout, opts._v_timeout[1])

    def test_extra_references(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            self.assertRaises(TypeError, opts.set_extra_references, 'abc')
            refs = ReferenceRecordSet(ReferenceRecord(
                Property('p').no_value()))
            opts.extra_references = refs
            self.assertEqual(opts.extra_references, refs)
            opts.extra_references = ReferenceRecordSet()
            self.assertEqual(opts.extra_references, ReferenceRecordSet())
            opts.extra_references = [
                ReferenceRecord(Property('p').no_value())]  # type: ignore
            self.assertEqual(opts.extra_references, refs)

    def test_max_page_size(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ['KIF_STORE_MAX_PAGE_SIZE'] = '33'
            opts = StoreOptions()
            self.assertEqual(opts.max_page_size, 33)
            del os.environ['KIF_STORE_MAX_PAGE_SIZE']
        with Context() as ctx:
            opts = ctx.options.store
            self.assertRaises(TypeError, opts.set_max_page_size, {})
            self.assertRaises(ValueError, opts.set_max_page_size, 'abc')
            opts.max_page_size = 44
            self.assertEqual(opts.max_page_size, 44)
            opts.max_page_size = 0
            self.assertEqual(opts.max_page_size, 0)
            opts.max_page_size = -8
            self.assertEqual(opts.max_page_size, 0)

    def test_page_size(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ['KIF_STORE_PAGE_SIZE'] = '33'
            opts = StoreOptions()
            self.assertEqual(opts.page_size, 33)
            del os.environ['KIF_STORE_PAGE_SIZE']
        with Context() as ctx:
            opts = ctx.options.store
            self.assertRaises(TypeError, opts.set_page_size, {})
            self.assertRaises(ValueError, opts.set_page_size, 'abc')
            opts.page_size = 44
            self.assertEqual(opts.page_size, 44)
            opts.page_size = 0
            self.assertEqual(opts.page_size, 0)
            opts.page_size = -8
            self.assertEqual(opts.page_size, 0)

    def test_max_timeout(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ['KIF_STORE_MAX_TIMEOUT'] = '1000'
            opts = StoreOptions()
            self.assertEqual(opts.max_timeout, 1000.)
            del os.environ['KIF_STORE_MAX_TIMEOUT']
        with Context() as ctx:
            opts = ctx.options.store
            self.assertRaises(TypeError, opts.set_max_timeout, {})
            self.assertRaises(ValueError, opts.set_max_timeout, 'abc')
            opts.max_timeout = 44.
            self.assertEqual(opts.max_timeout, 44.)
            opts.max_timeout = 0.
            self.assertEqual(opts.max_timeout, 0.)
            opts.max_timeout = -8.
            self.assertEqual(opts.max_timeout, 0.)

    def test_timeout(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ['KIF_STORE_TIMEOUT'] = '33'
            opts = StoreOptions()
            self.assertEqual(opts.timeout, 33.)
            del os.environ['KIF_STORE_TIMEOUT']
        with Context() as ctx:
            opts = ctx.options.store
            self.assertRaises(TypeError, opts.set_timeout, {})
            self.assertRaises(ValueError, opts.set_timeout, 'abc')
            opts.timeout = 44.
            self.assertEqual(opts.timeout, 44.)
            opts.timeout = 0.
            self.assertEqual(opts.timeout, 0)
            opts.timeout = -8.
            self.assertEqual(opts.timeout, 0.)
            opts.timeout = None
            self.assertIsNone(opts.timeout)


if __name__ == '__main__':
    Test.main()
