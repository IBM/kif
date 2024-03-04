# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    DeepDataValue,
    Entity,
    ExternalId,
    IRI,
    Item,
    Lexeme,
    Property,
    Quantity,
    ShallowDataValue,
    String,
    Text,
    Time,
    Value,
)

from .tests import kif_TestCase


class TestValue(kif_TestCase):

    def test__preprocess_arg_value_mask(self):
        self.assertRaises(
            TypeError, Value._preprocess_arg_value_mask, 'abc', 1)
        self.assertEqual(
            Value.ITEM,
            Value._preprocess_arg_value_mask(Value.ITEM, 1))
        self.assertEqual(
            Value.Mask(0),
            Value._preprocess_arg_value_mask(0, 1))

    def test__check_optional_arg_value_mask(self):
        self.assertRaises(
            TypeError,
            Value._check_optional_arg_value_mask, 'abc')
        self.assertIsNone(Value._check_optional_arg_value_mask(None))
        self.assertEqual(
            Value.ITEM,
            Value._check_optional_arg_value_mask(None, Value.ITEM))
        self.assertEqual(
            Value.Mask(0),
            Value._check_optional_arg_value_mask(Value.Mask(0), Value.ITEM))

    def test__preprocess_optional_arg_value_mask(self):
        self.assertRaises(
            TypeError,
            Value._preprocess_optional_arg_value_mask, 'abc', 1)
        self.assertIsNone(
            Value._preprocess_optional_arg_value_mask(None, 1))
        self.assertEqual(
            Value.ENTITY | Value.TEXT,
            Value._preprocess_optional_arg_value_mask(
                None, 1, Value.TEXT | Value.ENTITY))
        self.assertEqual(
            Value.ALL,
            Value._preprocess_optional_arg_value_mask(Value.ALL, 1, None))
        self.assertEqual(
            Value.Mask(0),
            Value._preprocess_optional_arg_value_mask(0, 1))

    def test__preprocess_arg_value(self):
        self.assertRaises(TypeError, Value._preprocess_arg_value, dict(), 1)
        self.assertEqual(Value._preprocess_arg_value(5, 1), Quantity(5))
        self.assertEqual(Value._preprocess_arg_value('abc', 1), String('abc'))
        self.assertEqual(Value._preprocess_arg_value(Item('x'), 1), Item('x'))

    def test_get_mask(self):
        self.assertEqual(Item.get_mask(), Value.ITEM)
        self.assertEqual(Property.get_mask(), Value.PROPERTY)
        self.assertEqual(Lexeme.get_mask(), Value.LEXEME)
        self.assertEqual(IRI.get_mask(), Value.IRI)
        self.assertEqual(Text.get_mask(), Value.TEXT)
        self.assertEqual(String.get_mask(), Value.STRING)
        self.assertEqual(ExternalId.get_mask(), Value.EXTERNAL_ID)
        self.assertEqual(Quantity.get_mask(), Value.QUANTITY)
        self.assertEqual(Time.get_mask(), Value.TIME)
        self.assertEqual(Entity.get_mask(), Value.ENTITY)
        self.assertEqual(ShallowDataValue.get_mask(), Value.SHALLOW_DATA_VALUE)
        self.assertEqual(DeepDataValue.get_mask(), Value.DEEP_DATA_VALUE)
        self.assertEqual(DataValue.get_mask(), Value.DATA_VALUE)
        self.assertEqual(Value.get_mask(), Value.ALL)


if __name__ == '__main__':
    TestValue.main()
