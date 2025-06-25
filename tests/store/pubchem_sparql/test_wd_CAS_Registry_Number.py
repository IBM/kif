# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.typing import Any
from kif_lib.vocabulary import pc, wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls, **kwargs: Any) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB(**kwargs)

    def test_ask(self) -> None:
        a, F = self.store_ask_assertion(self.KB())
        a(True, F(pc.CID(241), wd.CAS_Registry_Number))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(7, F(pc.CID(241), wd.CAS_Registry_Number))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(pc.CID(241), wd.CAS_Registry_Number),
           {wd.CAS_Registry_Number(pc.CID(241), '2396-01-2'),
            wd.CAS_Registry_Number(pc.CID(241), '25053-22-9'),
            wd.CAS_Registry_Number(pc.CID(241), '26181-88-4'),
            wd.CAS_Registry_Number(pc.CID(241), '3355-34-8'),
            wd.CAS_Registry_Number(pc.CID(241), '54682-86-9'),
            wd.CAS_Registry_Number(pc.CID(241), '62485-97-6'),
            wd.CAS_Registry_Number(pc.CID(241), '71-43-2')})
        # Now without normalizing CAS nos.
        xf, F = self.store_xfilter_assertion(self.KB(normalize_casrn=False))
        xf(F(pc.CID(241), wd.CAS_Registry_Number),
           {wd.CAS_Registry_Number(pc.CID(241), '2396-01-2'),
            wd.CAS_Registry_Number(pc.CID(241), '25053-22-9'),
            wd.CAS_Registry_Number(pc.CID(241), '26181-88-4'),
            wd.CAS_Registry_Number(pc.CID(241), '3355-34-8'),
            wd.CAS_Registry_Number(pc.CID(241), '54682-86-9'),
            wd.CAS_Registry_Number(pc.CID(241), '62485-97-6'),
            wd.CAS_Registry_Number(pc.CID(241), '71-43-2'),
            wd.CAS_Registry_Number(pc.CID(241), 'cas-71-43-2')})


if __name__ == '__main__':
    Test.main()
