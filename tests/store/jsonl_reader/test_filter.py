# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store

from ...tests import StoreTestCase


class Test(StoreTestCase):

    def test(self) -> None:
        kb = Store('jsonl-reader', 'tests/data/benzene.jsonl')
        xf, F = self.store_xfilter_assertion(kb)
        xf(F(), set(Store(
            'rdf', 'tests/data/benzene.ttl').filter(annotated=True)))


if __name__ == '__main__':
    Test.main()
