# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os

from kif_lib import (
    Context,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
    Store,
)
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
            # flags
            assert_type(opts.flags, Store.Flags)
            self.assertEqual(opts.flags, opts._v_flags[1])
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
            self.assert_raises_bad_argument(
                TypeError, 1, 'extra_references',
                'cannot coerce str into Snak',
                opts.set_extra_references, 'abc')
            refs = ReferenceRecordSet(ReferenceRecord(
                Property('p').no_value()))
            opts.extra_references = refs
            self.assertEqual(opts.extra_references, refs)
            opts.extra_references = ReferenceRecordSet()
            self.assertEqual(opts.extra_references, ReferenceRecordSet())
            opts.extra_references = [
                ReferenceRecord(Property('p').no_value())]  # type: ignore
            self.assertEqual(opts.extra_references, refs)

    def test_flags(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_flags[0]] = str(Store.Flags.ALL.value)
            opts = StoreOptions()
            self.assertEqual(opts.flags, Store.Flags.ALL)
            del os.environ[opts._v_flags[0]]
        with Context() as ctx:
            opts = ctx.options.store
            self.assert_raises_bad_argument(
                TypeError, 1, 'flags', 'cannot coerce dict into Store.Flags',
                opts.set_flags, {})
            opts.flags = Store.Flags.ALL
            self.assertEqual(opts.flags, Store.Flags.ALL)
            opts.flags = 0  # type: ignore
            self.assertEqual(opts.flags, Store.Flags(0))

    def test_max_page_size(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_max_page_size[0]] = '33'
            opts = StoreOptions()
            self.assertEqual(opts.max_page_size, 33)
            del os.environ[opts._v_max_page_size[0]]
        with Context() as ctx:
            opts = ctx.options.store
            self.assert_raises_bad_argument(
                TypeError, 1, 'max_page_size',
                'cannot coerce dict into Quantity',
                opts.set_max_page_size, {})
            self.assert_raises_bad_argument(
                ValueError, 1, 'max_page_size',
                'cannot coerce str into Quantity',
                opts.set_max_page_size, 'abc')
            opts.max_page_size = 44
            self.assertEqual(opts.max_page_size, 44)
            opts.max_page_size = 0
            self.assertEqual(opts.max_page_size, 0)
            opts.max_page_size = -8
            self.assertEqual(opts.max_page_size, 0)

    def test_page_size(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_page_size[0]] = '33'
            opts = StoreOptions()
            self.assertEqual(opts.page_size, 33)
            del os.environ[opts._v_page_size[0]]
        with Context() as ctx:
            opts = ctx.options.store
            self.assert_raises_bad_argument(
                TypeError, 1, 'page_size', 'cannot coerce dict into Quantity',
                opts.set_page_size, {})
            self.assert_raises_bad_argument(
                ValueError, 1, 'page_size', 'cannot coerce str into Quantity',
                opts.set_page_size, 'abc')
            opts.page_size = 44
            self.assertEqual(opts.page_size, 44)
            opts.page_size = 0
            self.assertEqual(opts.page_size, 0)
            opts.page_size = -8
            self.assertEqual(opts.page_size, 0)

    def test_max_timeout(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_max_timeout[0]] = '1000'
            opts = StoreOptions()
            self.assertEqual(opts.max_timeout, 1000.)
            del os.environ[opts._v_max_timeout[0]]
        with Context() as ctx:
            opts = ctx.options.store
            self.assert_raises_bad_argument(
                TypeError, 1, 'max_timeout',
                'cannot coerce dict into Quantity',
                opts.set_max_timeout, {})
            self.assert_raises_bad_argument(
                ValueError, 1, 'max_timeout',
                'cannot coerce str into Quantity',
                opts.set_max_timeout, 'abc')
            opts.max_timeout = 44.
            self.assertEqual(opts.max_timeout, 44.)
            opts.max_timeout = 0.
            self.assertEqual(opts.max_timeout, 0.)
            opts.max_timeout = -8.
            self.assertEqual(opts.max_timeout, 0.)

    def test_timeout(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_timeout[0]] = '33'
            opts = StoreOptions()
            self.assertEqual(opts.timeout, 33.)
            del os.environ[opts._v_timeout[0]]
        with Context() as ctx:
            opts = ctx.options.store
            self.assert_raises_bad_argument(
                TypeError, 1, 'timeout', 'cannot coerce dict into Quantity',
                opts.set_timeout, {})
            self.assert_raises_bad_argument(
                ValueError, 1, 'timeout', 'cannot coerce str into Quantity',
                opts.set_timeout, 'abc')
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
