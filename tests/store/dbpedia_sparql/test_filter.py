# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        import os
        dbpedia = os.getenv('DBPEDIA')
        if not dbpedia:
            raise cls.SKIP('DBPEDIA is not set')
        else:
            return cls.S('dbpedia-sparql', dbpedia)


if __name__ == '__main__':
    Test.main()
