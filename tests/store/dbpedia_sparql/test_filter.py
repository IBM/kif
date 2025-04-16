# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.vocabulary import db

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls):
        import os
        dbpedia = os.getenv('DBPEDIA')
        if not dbpedia:
            raise cls.SKIP('DBPEDIA is not set')
        else:
            return cls.S('dbpedia-sparql', dbpedia)

    def test(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(db.r('Alan_Turing'), db.op('birthPlace')),
           {db.op('birthPlace')(db.r('Alan_Turing'), db.r('Maida_Vale'))})


if __name__ == '__main__':
    Test.main()
