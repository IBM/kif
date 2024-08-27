# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.error import ShouldNotGetHere

from .tests import StoreTestCase


class TestStoreABC_Error(StoreTestCase):

    def test__error(self) -> None:
        err = Store._error('hello')
        self.assertIsInstance(err, Store.Error)
        self.assertEqual(err.args, ('hello',))

    def test__should_not_get_here(self) -> None:
        err = Store._should_not_get_here()
        self.assertIsInstance(err, ShouldNotGetHere)
        self.assertEqual(err.args, ())
        err = Store._should_not_get_here('hello')
        self.assertIsInstance(err, ShouldNotGetHere)
        self.assertEqual(err.args, ('hello',))


if __name__ == '__main__':
    TestStoreABC_Error.main()
