# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    Entity,
    ExternalIdDatatype,
    IRI,
    IRI_Datatype,
    ItemDatatype,
    LexemeDatatype,
    PropertyDatatype,
    QuantityDatatype,
    StringDatatype,
    TextDatatype,
    TimeDatatype,
)
from kif_lib.error import MustBeImplementedInSubclass

from .tests import kif_TestCase


class TestModelValueDatatype(kif_TestCase):

    def test__preprocess_arg_datatype(self):
        self.assertRaises(TypeError, Datatype._preprocess_arg_datatype, 0, 1)
        self.assertRaises(
            ValueError, Datatype._preprocess_arg_datatype, 'x', 1)
        self.assertEqual(
            Datatype._preprocess_arg_datatype(ItemDatatype(), 1),
            ItemDatatype())
        self.assertEqual(
            Datatype._preprocess_arg_datatype(ItemDatatype()._uri, 1),
            ItemDatatype())
        self.assertEqual(
            Datatype._preprocess_arg_datatype(str(ItemDatatype()._uri), 1),
            ItemDatatype())
        self.assertEqual(
            Datatype._preprocess_arg_datatype(IRI(ItemDatatype()._uri), 1),
            ItemDatatype())

    def test_aliases(self):
        self.assert_item_datatype(ItemDatatype())
        self.assert_property_datatype(PropertyDatatype())
        self.assert_lexeme_datatype(LexemeDatatype())
        self.assert_iri_datatype(IRI_Datatype())
        self.assert_text_datatype(TextDatatype())
        self.assert_string_datatype(StringDatatype())
        self.assert_external_id_datatype(ExternalIdDatatype())
        self.assert_quantity_datatype(QuantityDatatype())
        self.assert_time_datatype(TimeDatatype())

    def test_from_value_class(self):
        self.assertRaisesRegex(
            TypeError, r'\(expected type, got int\)',
            Datatype.from_value_class, 0)
        self.assertRaisesRegex(
            ValueError, r'\(expected subclass of Value, got int\)',
            Datatype.from_value_class, int)
        self.assertRaisesRegex(
            ValueError, r'\(no datatype for Entity\)',
            Datatype.from_value_class, Entity)

    def test_to_value_class(self):
        self.assertRaises(
            MustBeImplementedInSubclass, Datatype.to_value_class)


if __name__ == '__main__':
    TestModelValueDatatype.main()
