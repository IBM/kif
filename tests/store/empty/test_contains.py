# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        return cls.S('empty')

    def test_contains(self) -> None:
        c = self.store_contains_assertion(self.KB())
        c(False, wd.mass(wd.benzene, '78.11'))
        c(False, wd.mass(wd.benzene, '78.11').annotate())


if __name__ == '__main__':
    Test.main()
