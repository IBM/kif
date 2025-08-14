# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Store
from kif_lib.vocabulary import wd

from ...tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls) -> Store:
        from .test_filter import Test as TestFilter
        return TestFilter.KB()

    def test_ask(self) -> None:
        a, F = self.store_ask_assertion(self.KB())
        a(True, F(wd.Brazil, wd.type, wd.state))

    def test_count(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(4, F(wd.Brazil, wd.instance_of))
        c(68, F(wd.Brazil, wd.type))

    def test_filter_subject_is_item(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(wd.Brazil, wd.type, wd.subtype(wd.state)),
           {wd.type(wd.Brazil, wd.seculararchy),
            wd.type(wd.Brazil, wd.sovereign_state)})

    def test_filter_subject_is_property(self) -> None:
        xf, F = self.store_xfilter_assertion(self.KB())
        xf(F(None, wd.type, wd.Wikidata_property_for_ontology_mapping),
           set(map(lambda s: wd.a(
               s, wd.Wikidata_property_for_ontology_mapping), (
                   wd.equivalent_class,
                   wd.exact_match,
                   wd.GeoNames_feature_code,
                   wd.mapping_relation_type,
                   wd.narrower_external_class))))

    def test_filter_subject_is_lexeme(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
