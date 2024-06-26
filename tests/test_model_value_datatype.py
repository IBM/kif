# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    Entity,
    ExternalId,
    ExternalIdDatatype,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    KIF_Object,
    Lexeme,
    LexemeDatatype,
    Property,
    PropertyDatatype,
    Quantity,
    QuantityDatatype,
    String,
    StringDatatype,
    Text,
    TextDatatype,
    Time,
    TimeDatatype,
)

from .tests import kif_TestCase


class TestModelValueDatatype(kif_TestCase):

    def test__new__(self):
        self.assert_raises_bad_argument(
            TypeError, 1, 'datatype_class',
            'cannot coerce NoneType into Datatype', Datatype)
        self.assert_raises_bad_argument(
            TypeError, 1, 'datatype_class',
            'cannot coerce int into Datatype', Datatype, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, 'datatype_class',
            'cannot coerce Datatype into Datatype', Datatype, Datatype)
        self.assert_raises_bad_argument(
            TypeError, 1, 'datatype_class',
            'cannot coerce KIF_Object into Datatype',
            Datatype, KIF_Object)
        self.assert_raises_bad_argument(
            TypeError, 1, 'datatype_class',
            'cannot coerce Entity into Datatype',
            Datatype, Entity)
        self.assert_item_datatype(ItemDatatype())
        self.assert_item_datatype(Datatype(Item))
        self.assert_item_datatype(Item.datatype)
        self.assert_property_datatype(PropertyDatatype())
        self.assert_property_datatype(Datatype(Property))
        self.assert_property_datatype(Property.datatype)
        self.assert_lexeme_datatype(LexemeDatatype())
        self.assert_lexeme_datatype(Datatype(Lexeme))
        self.assert_lexeme_datatype(Lexeme.datatype)
        self.assert_iri_datatype(IRI_Datatype())
        self.assert_iri_datatype(Datatype(IRI))
        self.assert_iri_datatype(IRI.datatype)
        self.assert_text_datatype(TextDatatype())
        self.assert_text_datatype(Datatype(Text))
        self.assert_text_datatype(Text.datatype)
        self.assert_string_datatype(StringDatatype())
        self.assert_string_datatype(Datatype(String))
        self.assert_string_datatype(String.datatype)
        self.assert_external_id_datatype(ExternalIdDatatype())
        self.assert_external_id_datatype(Datatype(ExternalId))
        self.assert_external_id_datatype(ExternalId.datatype)
        self.assert_quantity_datatype(QuantityDatatype())
        self.assert_quantity_datatype(Datatype(Quantity))
        self.assert_quantity_datatype(Quantity.datatype)
        self.assert_time_datatype(TimeDatatype())
        self.assert_time_datatype(Datatype(Time))
        self.assert_time_datatype(Time.datatype)


if __name__ == '__main__':
    TestModelValueDatatype.main()
