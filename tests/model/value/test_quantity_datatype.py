# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Quantity, QuantityDatatype
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_instance(self) -> None:
        assert_type(QuantityDatatype.instance, QuantityDatatype)
        self.assertIs(QuantityDatatype.instance, QuantityDatatype())

    def test_value_class(self) -> None:
        assert_type(QuantityDatatype.value_class, type[Quantity])

    def test_check(self) -> None:
        assert_type(
            QuantityDatatype.check(QuantityDatatype()), QuantityDatatype)
        self._test_check(QuantityDatatype)

    def test__init__(self) -> None:
        assert_type(QuantityDatatype(), QuantityDatatype)
        self._test__init__(QuantityDatatype, self.assert_quantity_datatype)


if __name__ == '__main__':
    Test.main()
