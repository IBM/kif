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
        a(True, F(pc.CID(241), wd.instance_of))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(2, F(pc.isotope_atom_count | pc.CID(241), wd.instance_of))

    def test_filter(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(
            pc.CID(241)
            | pc.isotope_atom_count
            | pc.IUPAC_name
            | pc.patent('AR-033431-A1')
            | pc.source('ID25790'),
            wd.instance_of),
           {wd.instance_of(pc.CID(241), wd.type_of_a_chemical_entity),
            wd.instance_of(
                pc.isotope_atom_count,
                wd.Wikidata_property_related_to_chemistry),
            wd.instance_of(
                pc.IUPAC_name,
                wd.Wikidata_property_related_to_chemistry),
            wd.instance_of(pc.patent('AR-033431-A1'), wd.patent),
            wd.instance_of(pc.source('ID25790'), wd.vendor)})


if __name__ == '__main__':
    Test.main()
