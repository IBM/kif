# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        return cls.S('empty')

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(0, F())


if __name__ == '__main__':
    Test.main()
