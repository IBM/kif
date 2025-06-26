# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    def test(self) -> None:
        rdf = Store('rdf', 'tests/data/benzene.ttl')
        f, F = self.store_filter_assertion(
            Store('csv-reader', 'tests/data/benzene.csv'))
        f(F(), set(rdf.filter()))
        f(F(subject_mask=F.PROPERTY), set(rdf.filter(subject=wd.InChIKey)))


if __name__ == '__main__':
    Test.main()
