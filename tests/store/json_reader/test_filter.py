# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store

from ...tests import StoreTestCase


class Test(StoreTestCase):

    def test(self) -> None:
        rdf = Store('rdf', 'tests/data/benzene.ttl')
        f, F = self.store_filter_assertion(
            Store('json-reader', 'tests/data/benzene.json'))
        f(F(), set(rdf.filter()))
        f(F(value_mask=F.STRING), set(rdf.filter(value_mask=F.STRING)))


if __name__ == '__main__':
    Test.main()
