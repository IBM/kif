# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Item, ItemDatatype
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_instance(self) -> None:
        assert_type(ItemDatatype.instance, ItemDatatype)
        self.assertIs(ItemDatatype.instance, ItemDatatype())

    def test_value_class(self) -> None:
        assert_type(ItemDatatype.value_class, type[Item])

    def test_check(self) -> None:
        assert_type(ItemDatatype.check(ItemDatatype()), ItemDatatype)
        self._test_check(ItemDatatype)

    def test__init__(self) -> None:
        assert_type(ItemDatatype(), ItemDatatype)
        self._test__init__(ItemDatatype, self.assert_item_datatype)


if __name__ == '__main__':
    Test.main()
