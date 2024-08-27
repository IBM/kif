# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Context
from kif_lib.context.options import Options
from kif_lib.typing import assert_type

from ..tests import TestCase


class Test(TestCase):

    def test__init__(self) -> None:
        ctx = Context()
        assert_type(ctx, Context)
        self.assertIsInstance(ctx, Context)

    def test__enter__(self) -> None:
        ctx0 = Context.top()
        with Context() as ctx1:
            self.assertEqual(Context.top(), ctx1)
            with Context() as ctx2:
                self.assertEqual(Context.top(), ctx2)
            self.assertEqual(Context.top(), ctx1)
        self.assertEqual(Context.top(), ctx0)

    def test_top(self) -> None:
        assert_type(Context.top(), Context)
        self.assertIsInstance(Context.top(), Context)
        ctx = Context()
        self.assertEqual(ctx, Context.top(ctx))
        self.assertNotEqual(ctx, Context.top())

    def test_get_options(self) -> None:
        assert_type(Context.top().options, Options)


if __name__ == '__main__':
    Test.main()
