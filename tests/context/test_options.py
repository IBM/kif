# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.context import Context, Section
from kif_lib.context.options import Options
from kif_lib.typing import assert_type

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options
            assert_type(opts, Options)
            self.assertIsInstance(opts.model, Section)
            self.assertIsInstance(opts.store, Section)
            self.assertEqual(
                opts.default_language,
                opts.model.value.text.default_language)


if __name__ == '__main__':
    Test.main()
