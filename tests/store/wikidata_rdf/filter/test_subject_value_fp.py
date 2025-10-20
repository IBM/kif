# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store, Text
from kif_lib.vocabulary import wd

from ....tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from ..test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_item(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        s = wd.Brazil
        xf(F(subject=wd.Brazil, snak_mask=F.VALUE_SNAK, value_mask=F.ITEM),
           {wd.instance_of(s, wd.country_),
            wd.part_of(s, wd.Latin_America)})

    def test_property(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        s = wd.InChIKey
        xf(F(subject=s, property=wd.label),
           {wd.label(s, Text('InChIKey', 'en')),
            wd.label(s, Text('InChIKey', 'es'))})

    def test_lexeme(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        s = wd.L(46803)
        xf(F(subject=s),
           {wd.language(s, wd.Portuguese),
            wd.lexical_category(s, wd.verb),
            wd.lemma(s, Text('andar', 'pt'))})


if __name__ == '__main__':
    Test.main()
