# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.model import (
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

    def test_check(self) -> None:
        self.assert_raises_check_error(
            ExternalIdDatatype, 0, ExternalIdDatatype.check)
        self.assert_raises_check_error(
            ExternalIdDatatype, {}, ExternalIdDatatype.check)
        self.assert_raises_check_error(
            ExternalIdDatatype, ExternalId('x'), ExternalIdDatatype.check)
        self.assert_raises_check_error(
            ExternalIdDatatype, ItemDatatype(), ExternalIdDatatype.check)
        self.assert_raises_check_error(
            ExternalIdDatatype, Item, ExternalIdDatatype.check)
        self.assert_raises_check_error(
            ExternalIdDatatype, StringDatatype(), ExternalIdDatatype.check)
        self.assert_raises_check_error(
            ExternalIdDatatype, String, ExternalIdDatatype.check)
        self.assert_raises_check_error(
            ExternalIdDatatype, Value, ExternalIdDatatype.check)
        # success
        assert_type(
            ExternalIdDatatype.check(ExternalIdDatatype()),
            ExternalIdDatatype)
        self.assertEqual(
            ExternalIdDatatype.check(ExternalIdDatatype()),
            ExternalId.datatype)
        self.assertEqual(
            ExternalIdDatatype.check(Datatype(ExternalIdDatatype)),
            ExternalId.datatype)
        self.assertEqual(
            ExternalIdDatatype.check(Datatype(ExternalId)),
            ExternalId.datatype)
        self.assertEqual(
            ExternalIdDatatype.check(ExternalId),
            ExternalId.datatype)

    def test__init__(self) -> None:
        self.assert_raises_check_error(ExternalIdDatatype, 0)
        # success
        assert_type(ExternalIdDatatype(), ExternalIdDatatype)
        self.assert_string_datatype(ExternalIdDatatype())
        self.assert_string_datatype(Datatype(ExternalIdDatatype))
        self.assert_string_datatype(Datatype(ExternalId))


if __name__ == '__main__':
    Test.main()
