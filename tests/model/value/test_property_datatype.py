# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Property, PropertyDatatype
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_instance(self) -> None:
        assert_type(PropertyDatatype.instance, PropertyDatatype)
        self.assertIs(PropertyDatatype.instance, PropertyDatatype())

    def test_value_class(self) -> None:
        assert_type(PropertyDatatype.value_class, type[Property])

    def test_check(self) -> None:
        assert_type(PropertyDatatype.check(
            PropertyDatatype()), PropertyDatatype)
        self._test_check(PropertyDatatype)

    def test__init__(self) -> None:
        assert_type(PropertyDatatype(), PropertyDatatype)
        self._test__init__(PropertyDatatype, self.assert_property_datatype)


if __name__ == '__main__':
    Test.main()
