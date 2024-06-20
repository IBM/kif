# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    ExternalId,
    ExternalIdDatatype,
    Item,
    ItemDatatype,
    String,
    StringDatatype,
    Value,
)
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_value_class(self) -> None:
        assert_type(StringDatatype.value_class, type[String])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            StringDatatype, 0, StringDatatype.check)
        self.assert_raises_check_error(
            StringDatatype, {}, StringDatatype.check)
        self.assert_raises_check_error(
            StringDatatype, String('x'), StringDatatype.check)
        self.assert_raises_check_error(
            StringDatatype, ItemDatatype(), StringDatatype.check)
        self.assert_raises_check_error(
            StringDatatype, Item, StringDatatype.check)
        self.assert_raises_check_error(
            StringDatatype, Value, StringDatatype.check)
        # success
        assert_type(StringDatatype.check(StringDatatype()), StringDatatype)
        self.assertEqual(
            StringDatatype.check(StringDatatype()),
            String.datatype)
        self.assertEqual(
            StringDatatype.check(ExternalIdDatatype()),
            ExternalId.datatype)
        self.assertEqual(
            StringDatatype.check(Datatype(StringDatatype)),
            String.datatype)
        self.assertEqual(
            StringDatatype.check(Datatype(ExternalIdDatatype)),
            ExternalId.datatype)
        self.assertEqual(
            StringDatatype.check(Datatype(String)),
            String.datatype)
        self.assertEqual(
            StringDatatype.check(Datatype(ExternalId)),
            ExternalId.datatype)
        self.assertEqual(
            StringDatatype.check(String),
            String.datatype)

    def test__init__(self) -> None:
        self.assert_raises_check_error(StringDatatype, 0)
        # success
        assert_type(StringDatatype(), StringDatatype)
        self.assert_string_datatype(StringDatatype())
        self.assert_string_datatype(Datatype(StringDatatype))
        self.assert_string_datatype(Datatype(String))


if __name__ == '__main__':
    Test.main()
