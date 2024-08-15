# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.context import Context, Section
from kif_lib.model.options import ModelOptions
from kif_lib.typing import assert_type

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options.model
            assert_type(opts, ModelOptions)
            self.assertIsInstance(opts.value, Section)


if __name__ == '__main__':
    Test.main()
