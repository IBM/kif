# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        return cls.S(
            'pubchem-rdf',
            'tests/data/benzene-pubchem.ttl',
        )

    def test_empty(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(0, F(snak_mask=F.SnakMask(0)))

    def test_full(self) -> None:
        c, F = self.count_assertion(self.KB())
        c(3, F())


if __name__ == '__main__':
    Test.main()
