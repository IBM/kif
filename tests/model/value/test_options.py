# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.context import Context, Section
from kif_lib.model.value.options import ValueOptions
from kif_lib.typing import assert_type

from ...tests import TestCase


class Test(TestCase):

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options.model.value
            assert_type(opts, ValueOptions)
            self.assertIsInstance(opts.text, Section)


if __name__ == '__main__':
    Test.main()
