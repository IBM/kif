# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Store
from kif_lib.error import MustBeImplementedInSubclass, ShouldNotGetHere

from .tests import kif_StoreTestCase


class TestStoreError(kif_StoreTestCase):

    def test__error(self):
        err = Store._error('hello')
        self.assertIsInstance(err, Store.Error)
        self.assertEqual(err.args, ('hello',))

    def test__must_be_implemented_in_subclass(self):
        err = Store._must_be_implemented_in_subclass()
        self.assertIsInstance(err, MustBeImplementedInSubclass)
        self.assertEqual(err.args, ())
        err = Store._must_be_implemented_in_subclass('hello')
        self.assertIsInstance(err, MustBeImplementedInSubclass)
        self.assertEqual(err.args, ('hello',))

    def test__should_not_get_here(self):
        err = Store._should_not_get_here()
        self.assertIsInstance(err, ShouldNotGetHere)
        self.assertEqual(err.args, ())
        err = Store._should_not_get_here('hello')
        self.assertIsInstance(err, ShouldNotGetHere)
        self.assertEqual(err.args, ('hello',))


if __name__ == '__main__':
    TestStoreError.main()
