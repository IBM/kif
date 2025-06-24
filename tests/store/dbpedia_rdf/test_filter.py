# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import db, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        return cls.S(
            'dbpedia-rdf',
            'tests/data/benzene-dbpedia.ttl')

    def test_empty(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(snak_mask=F.SnakMask(0)), ())

    def test_full(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(),
           {wd.label(db.r('Benzene'), 'Benzene')})


if __name__ == '__main__':
    Test.main()
