# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.context.options import Options
from kif_lib.typing import assert_type

from ..tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options
            assert_type(opts, Options)
            self.assertIsInstance(opts.model, Section)
            self.assertIsInstance(opts.store, Section)
            self.assertEqual(opts.language, opts.model.value.text.language)


if __name__ == '__main__':
    Test.main()
