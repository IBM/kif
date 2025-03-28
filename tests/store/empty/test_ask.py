# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        return cls.S('empty')

    def test_ask(self) -> None:
        c, F = self.ask_assertion(self.KB())
        c(False, F())


if __name__ == '__main__':
    Test.main()
