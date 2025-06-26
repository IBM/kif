# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    def test(self) -> None:
        rdf = Store('rdf', 'tests/data/benzene.ttl')
        xf, F = self.store_xfilter_assertion(
            Store('jsonl-reader', 'tests/data/benzene.jsonl'))
        xf(F(), set(rdf.filter(annotated=True)))
        xf(F(property=wd.mass),
           set(rdf.filter(property=wd.mass, annotated=True)))


if __name__ == '__main__':
    Test.main()
