# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os

from kif_lib.context import Context
from kif_lib.model.value.text import TextOptions
from kif_lib.typing import assert_type

from ...tests import TestCase


class Test(TestCase):

    def test_options(self) -> None:
        with Context() as ctx:
            opts = ctx.options.model.value.text
            assert_type(opts, TextOptions)
            assert_type(opts.language, str)
            self.assertEqual(opts.language, opts._v_language[1])

    def test_language(self) -> None:
        with Context() as ctx:
            opts = ctx.options.model.value.text
            os.environ[opts._v_language[0]] = 'pt'
            opts = TextOptions()
            self.assertEqual(opts.language, 'pt')
            del os.environ[opts._v_language[0]]
        with Context() as ctx:
            opts = ctx.options.model.value.text
            opts.language = 'abc'
            self.assertEqual(opts.language, 'abc')
            self.assert_raises_bad_argument(
                TypeError, 1, 'language', 'cannot coerce int into String',
                (lambda x: setattr(opts, 'language', x),
                 'language'), 0)


if __name__ == '__main__':
    Test.main()
