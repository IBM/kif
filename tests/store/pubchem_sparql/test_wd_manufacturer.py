# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import pc, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_ask(self) -> None:
        a, F = self.store_ask_assertion(self.KB())
        a(True, F(pc.CID(23986), wd.manufacturer))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(37, F(pc.CID(23986), wd.manufacturer))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(pc.CID(23986), wd.manufacturer),
           set(map(lambda x: wd.manufacturer(pc.CID(23986), pc.source(x)), [
               'AAA_Chemistry',
               'AKos_Consulting___Solutions',
               'Ambinter',
               'ID1052',
               'ID1088',
               'ID1096',
               'ID11764',
               'ID11831',
               'ID14207',
               'ID14207',
               'ID15224',
               'ID15394',
               'ID15467',
               'ID15494',
               'ID15699',
               'ID15747',
               'ID18825',
               'ID21014',
               'ID23514',
               'ID23562',
               'ID23904',
               'ID23983',
               'ID24221',
               'ID24343',
               'ID24449',
               'ID24554',
               'ID24800',
               'ID25432',
               'ID26464',
               'ID26515',
               'ID708',
               'ID731',
               'IS_Chemical_Technology',
               'Kingston_Chemistry',
               'MP_Biomedicals',
               'NovoSeek',
               'Sigma_Aldrich',
               'Tractus',
           ])))


if __name__ == '__main__':
    Test.main()
