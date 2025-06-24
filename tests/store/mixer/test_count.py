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

    def test_empty(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(0, F(snak_mask=F.SnakMask(0)))

    def test_full(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(25, F())

    # -- masks --

    def test_snak_mask(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(2, F(snak_mask=F.SOME_VALUE_SNAK))
        c(3, F(snak_mask=F.NO_VALUE_SNAK))

    def test_subject_mask(self) -> None:
        raise self.TODO()

    def test_property_mask(self) -> None:
        raise self.TODO()

    def test_value_mask(self) -> None:
        raise self.TODO()

    def test_language(self) -> None:
        c, F = self.store_count_assertion(self.KB())
        c(4, F(property=wd.alias, language='es'))

    # -- value fp --

    def test_value_fp_subject(self) -> None:
        raise self.TODO()

    def test_value_fp_property(self) -> None:
        raise self.TODO()

    def test_value_fp_iri(self) -> None:
        raise self.TODO()

    def test_value_fp_text(self) -> None:
        raise self.TODO()

    def test_value_fp_string(self) -> None:
        raise self.TODO()

    def test_value_fp_external_id(self) -> None:
        raise self.TODO()

    def test_value_fp_quantity(self) -> None:
        raise self.TODO()

    def test_value_fp_time(self):
        raise self.TODO()

    # -- snak fp --

    def test_snak_fp_subject(self) -> None:
        raise self.TODO()

    def test_snak_fp_property(self) -> None:
        raise self.TODO()

    def test_snak_fp_value(self) -> None:
        raise self.TODO()

    def test_or_fp_subject_property(self) -> None:
        raise self.TODO()

    def test_and_fp_subject(self) -> None:
        raise self.TODO()

    def test_and_fp_property(self) -> None:
        raise self.TODO()

    def test_and_fp_value(self) -> None:
        raise self.TODO()

    def test_or_fp_subject(self) -> None:
        raise self.TODO()

    def test_or_fp_property(self) -> None:
        raise self.TODO()

    def test_or_fp_value(self) -> None:
        raise self.TODO()


if __name__ == '__main__':
    Test.main()
