# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Quantity, Text
from kif_lib.vocabulary import wd

from ...tests import WikidataStoreTestCase


class Test(WikidataStoreTestCase):

    def test_filter_subject_is_empty_fp(self) -> None:
        kb = self.new_Store()
        self.assert_it_empty(kb.filter(Quantity(0)))

    def test_filter_subject_is_value_fp(self) -> None:
        kb = self.new_Store()
        self.assert_it_contains(
            kb.filter(wd.Monte_Pascoal),
            wd.instance_of(wd.Monte_Pascoal, wd.mountain),
            wd.named_after(wd.Monte_Pascoal, wd.Easter),
            wd.continent(wd.Monte_Pascoal, wd.Americas),
            wd.elevation_above_sea_level(
                wd.Monte_Pascoal, Quantity(536, wd.metre)))

    def test_filter_subject_is_snak_fp(self) -> None:
        kb = self.new_Store()
        self.assert_it_contains(
            kb.filter(wd.instance_of(wd.mountain), wd.named_after, wd.Easter),
            wd.named_after(wd.Monte_Pascoal, wd.Easter))

    def test_filter_subject_is_converse_snak_fp(self) -> None:
        kb = self.new_Store()
        self.assert_it_contains(
            kb.filter(-(wd.instance_of(wd.Monte_Pascoal))),
            wd.has_part(wd.mountain, wd.summit))

    def test_filter_subject_is_and(self) -> None:
        kb = self.new_Store()
        self.assert_it_empty(
            kb.filter(wd.Monte_Pascoal & wd.Mount_Everest))
        self.assert_it_empty(
            kb.filter(wd.Monte_Pascoal & wd.instance_of(wd.human)))
        self.assert_it_equals(
            kb.filter(
                wd.instance_of(wd.mountain) & wd.country(wd.Brazil),
                wd.named_after,
                wd.Easter),
            wd.named_after(wd.Monte_Pascoal, wd.Easter))
        self.assert_it_contains(
            kb.filter(
                wd.instance_of(wd.mountain)
                & wd.parent_peak.no_value()
                & (wd.country(wd.Nepal) | wd.country(wd.Argentina)),
                wd.native_label),
            wd.native_label(wd.Mount_Everest, Text('सगरमाथा', 'ne')))

    def test_filter_subject_is_or(self) -> None:
        kb = self.new_Store()
        self.assert_it_contains(
            kb.filter(wd.Monte_Pascoal | wd.Mount_Everest, wd.country),
            wd.country(wd.Mount_Everest, wd.Nepal),
            wd.country(wd.Monte_Pascoal, wd.Brazil))
        self.assert_it_equals(
            kb.filter(
                wd.Monte_Pascoal
                | wd.El_Capitan
                | (wd.parent_peak.no_value() & wd.instance_of(wd.mountain)),
                wd.country, wd.Nepal),
            wd.country(wd.Mount_Everest, wd.Nepal))


if __name__ == '__main__':
    Test.main()
