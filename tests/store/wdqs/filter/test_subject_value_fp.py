# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import wd

from ....tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from ..test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_item(self) -> None:
        kb = self.KB()
        kb.page_size = 2
        xf, F = self.store_xfilter_assertion(kb)
        s = wd.Ginga
        xf(F(subject=s, snak_mask=F.VALUE_SNAK, value_mask=F.ITEM),
           {wd.copyright_license(s, wd.GNU_General_Public_License),
            wd.copyright_status(s, wd.copyrighted),
            wd.country_of_origin(s, wd.Brazil),
            wd.different_from(s, wd.ginga),
            wd.instance_of(s, wd.system_software),
            wd.named_after(s, wd.ginga),
            wd.subclass_of(s, wd.middleware)})

    def test_property(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        s = wd.PubChem_CID
        xf(F(subject=s, property=wd.instance_of),
           {wd.instance_of(s, wd.Wikidata_property_for_an_identifier),
            wd.instance_of(s, wd.Wikidata_property_related_to_biology),
            wd.instance_of(s, wd.Wikidata_property_related_to_chemistry),
            wd.instance_of(s, wd.Wikidata_property_to_identify_substances)})

    def test_lexeme(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        s = wd.L(33)
        xf(F(subject=s, property=wd.homograph_lexeme),
           {wd.homograph_lexeme(s, wd.L(1259))})


if __name__ == '__main__':
    Test.main()
