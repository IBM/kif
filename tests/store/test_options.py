# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import os

from kif_lib import Context, Store
from kif_lib.store.options import StoreOptions
from kif_lib.typing import assert_type

from ..tests import TestCase


class Test(TestCase):

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            assert_type(opts, StoreOptions)
            assert_type(opts.default_flags, Store.Flags)
            self.assertEqual(opts.default_flags, opts._v_default_flags[1])

    def test_default_flags(self) -> None:
        with Context() as ctx:
            opts = ctx.options.store
            os.environ[opts._v_default_flags[0]] = str(Store.Flags.ALL.value)
            opts = StoreOptions()
            self.assertEqual(opts.default_flags, Store.Flags.ALL)
            del os.environ[opts._v_default_flags[0]]
        with Context() as ctx:
            opts = ctx.options.store
            opts.default_flags = Store.Flags.ALL
            self.assertEqual(opts.default_flags, Store.Flags.ALL)
            opts.default_flags = 0  # type: ignore
            self.assertEqual(opts.default_flags, Store.Flags(0))
            self.assertRaises(ValueError, setattr, opts, 'default_flags', {})


if __name__ == '__main__':
    Test.main()
