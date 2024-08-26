# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import os

from kif_lib import Context, Store
from kif_lib.store.options import StoreOptions
from kif_lib.typing import assert_type, Optional

from ..tests import TestCase


class Test(TestCase):

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            assert_type(opts, StoreOptions)
            # flags
            assert_type(opts.flags, Store.Flags)
            self.assertEqual(opts.flags, opts._v_flags[1])
            # page_size
            assert_type(opts.page_size, int)
            self.assertEqual(opts.page_size, opts._v_page_size[1])
            # timeout
            assert_type(opts.timeout, Optional[int])
            self.assertEqual(opts.timeout, opts._v_timeout[1])

    def test_flags(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_flags[0]] = str(Store.Flags.ALL.value)
            opts = StoreOptions()
            self.assertEqual(opts.flags, Store.Flags.ALL)
            del os.environ[opts._v_flags[0]]
        with Context() as ctx:
            opts = ctx.options.store
            opts.flags = Store.Flags.ALL
            self.assertEqual(opts.flags, Store.Flags.ALL)
            opts.flags = 0  # type: ignore
            self.assertEqual(opts.flags, Store.Flags(0))
            self.assertRaises(ValueError, setattr, opts, 'flags', {})

    def test_page_size(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_page_size[0]] = '33'
            opts = StoreOptions()
            self.assertEqual(opts.page_size, 33)
            del os.environ[opts._v_page_size[0]]
        with Context() as ctx:
            opts = ctx.options.store
            opts.page_size = 44
            self.assertEqual(opts.page_size, 44)
            opts.page_size = 0
            self.assertEqual(opts.page_size, 0)
            opts.page_size = -8
            self.assertEqual(opts.page_size, 0)
            self.assert_raises_bad_argument(
                TypeError, 1, 'page_size',
                'cannot coerce dict into Quantity',
                opts.set_page_size, {})


if __name__ == '__main__':
    Test.main()
