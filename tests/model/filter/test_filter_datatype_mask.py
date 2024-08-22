# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    DataValue,
    DeepDataValue,
    Entity,
    ExternalId,
    Filter,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    Lexeme,
    LexemeDatatype,
    Property,
    PropertyDatatype,
    Quantity,
    QuantityDatatype,
    ShallowDataValue,
    String,
    Text,
    Time,
    Value,
)
from kif_lib.typing import assert_type

from ...tests import ObjectTestCase


class Test(ObjectTestCase):

    def test_check(self) -> None:
        assert_type(
            Filter.DatatypeMask.check(Quantity), Filter.DatatypeMask)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Filter.DatatypeMask.check, {})
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Filter.DatatypeMask.check, 999)
        self.assertEqual(Filter.DatatypeMask.check('x'), Filter.STRING)
        self.assertEqual(Filter.DatatypeMask.check(0), Filter.DatatypeMask(0))
        self.assertEqual(
            Filter.DatatypeMask.check(Datatype),
            Filter.DatatypeMask.ALL)
        self.assertEqual(
            Filter.DatatypeMask.check(Value),
            Filter.VALUE)
        self.assertEqual(
            Filter.DatatypeMask.check(Entity),
            Filter.ENTITY)
        self.assertEqual(
            Filter.DatatypeMask.check(ItemDatatype()), Filter.ITEM)
        self.assertEqual(
            Filter.DatatypeMask.check(ItemDatatype), Filter.ITEM)
        self.assertEqual(Filter.DatatypeMask.check(Item), Filter.ITEM)
        self.assertEqual(
            Filter.DatatypeMask.check(Property), Filter.PROPERTY)
        self.assertEqual(Filter.DatatypeMask.check(Lexeme), Filter.LEXEME)
        self.assertEqual(
            Filter.DatatypeMask.check(DataValue),
            Filter.DATA_VALUE)
        self.assertEqual(
            Filter.DatatypeMask.check(ShallowDataValue),
            Filter.SHALLOW_DATA_VALUE)
        self.assertEqual(Filter.DatatypeMask.check(IRI), Filter.IRI)
        self.assertEqual(Filter.DatatypeMask.check(Text), Filter.TEXT)
        self.assertEqual(Filter.DatatypeMask.check(String), Filter.STRING)
        self.assertEqual(
            Filter.DatatypeMask.check(ExternalId), Filter.EXTERNAL_ID)
        self.assertEqual(
            Filter.DatatypeMask.check(DeepDataValue),
            Filter.DEEP_DATA_VALUE)
        self.assertEqual(Filter.DatatypeMask.check(Quantity), Filter.QUANTITY)
        self.assertEqual(Filter.DatatypeMask.check(Time), Filter.TIME)
        self.assertEqual(
            Filter.DatatypeMask.check(Filter.ITEM), Filter.ITEM)
        self.assertEqual(
            Filter.DatatypeMask.check_optional(None, Filter.DatatypeMask.ALL),
            Filter.DatatypeMask.ALL)
        self.assertIsNone(Filter.DatatypeMask.check_optional(None))

    def test_match(self) -> None:
        assert_type(Filter.DatatypeMask(0).match(Item), bool)
        for m in (Filter.DatatypeMask.ALL, Filter.VALUE, Filter.ENTITY):
            self.assertTrue(m.match(Item))
            self.assertTrue(m.match(PropertyDatatype))
            self.assertTrue(m.match(LexemeDatatype()))
        for m in (Filter.DatatypeMask.check(0),
                  Filter.DATA_VALUE, Filter.STRING):
            self.assertFalse(m.match(Item))
            self.assertFalse(m.match(PropertyDatatype))
            self.assertFalse(m.match(LexemeDatatype()))
        for m in (Filter.DatatypeMask.ALL, Filter.VALUE,
                  Filter.DATA_VALUE, Filter.SHALLOW_DATA_VALUE):
            self.assertTrue(m.match(IRI_Datatype()))
            self.assertTrue(m.match(Text))
            self.assertTrue(m.match(String))
            self.assertTrue(m.match(ExternalId.datatype))
        for m in (Filter.DatatypeMask.check(0),
                  Filter.ENTITY, Filter.ITEM, Filter.QUANTITY):
            self.assertFalse(m.match(IRI_Datatype()))
            self.assertFalse(m.match(Text))
            self.assertFalse(m.match(String))
            self.assertFalse(m.match(ExternalId.datatype))
        for m in (Filter.DatatypeMask.ALL, Filter.VALUE,
                  Filter.DATA_VALUE, Filter.DEEP_DATA_VALUE):
            self.assertTrue(m.match(QuantityDatatype))
            self.assertTrue(m.match(Time))
        for m in (Filter.DatatypeMask.check(0), Filter.ENTITY,
                  Filter.SHALLOW_DATA_VALUE, Filter.IRI):
            self.assertFalse(m.match(QuantityDatatype))
            self.assertFalse(m.match(Time))


if __name__ == '__main__':
    Test.main()
