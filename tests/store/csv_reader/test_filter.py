# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.model import DecoderError
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    def test(self) -> None:
        rdf = Store('rdf', 'tests/data/benzene.ttl')
        f, F = self.store_filter_assertion(
            Store('csv-reader', 'tests/data/benzene.csv'))
        f(F(), set(rdf.filter()))
        f(F(subject_mask=F.PROPERTY), set(rdf.filter(subject=wd.InChIKey)))

    def test_cell_is_not_evaluated(self) -> None:
        payload = '().__class__.__base__.__subclasses__().__len__()'
        csv = ('subject,property,value\n'
               f'"Item(IRI(\'x\'))","Property(IRI(\'p\'))","{payload}"\n')
        self.assertRaises(
            DecoderError, list, Store('csv-reader', data=csv).filter())


if __name__ == '__main__':
    Test.main()
