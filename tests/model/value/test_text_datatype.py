# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.model import (
    Datatype,
    Item,
    ItemDatatype,
    String,
    Text,
    TextDatatype,
    Value,
)
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_value_class(self) -> None:
        assert_type(TextDatatype.value_class, type[Text])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            TextDatatype, 0, TextDatatype.check)
        self.assert_raises_check_error(
            TextDatatype, {}, TextDatatype.check)
        self.assert_raises_check_error(
            TextDatatype, Text('x'), TextDatatype.check)
        self.assert_raises_check_error(
            TextDatatype, ItemDatatype(), TextDatatype.check)
        self.assert_raises_check_error(
            TextDatatype, Item, TextDatatype.check)
        self.assert_raises_check_error(
            TextDatatype, String, TextDatatype.check)
        self.assert_raises_check_error(
            TextDatatype, Value, TextDatatype.check)
        # success
        assert_type(TextDatatype.check(TextDatatype()), TextDatatype)
        self.assertEqual(
            TextDatatype.check(TextDatatype()), Text.datatype)
        self.assertEqual(
            TextDatatype.check(Datatype(TextDatatype)), Text.datatype)
        self.assertEqual(
            TextDatatype.check(Datatype(Text)), Text.datatype)
        self.assertEqual(
            TextDatatype.check(Text), Text.datatype)

    def test__init__(self) -> None:
        self.assert_raises_check_error(TextDatatype, 0)
        # success
        assert_type(TextDatatype(), TextDatatype)
        self.assert_text_datatype(TextDatatype())
        self.assert_text_datatype(Datatype(TextDatatype))
        self.assert_text_datatype(Datatype(Text))


if __name__ == '__main__':
    Test.main()
