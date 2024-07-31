# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    DatatypeVariable,
    ExternalId,
    ExternalIdDatatype,
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
    String,
    StringDatatype,
    Text,
    TextDatatype,
    Time,
    TimeDatatype,
)
from kif_lib.typing import assert_type

from ...tests import kif_ValueTestCase


class Test(kif_ValueTestCase):

    def test_variable_class(self) -> None:
        assert_type(Datatype.variable_class, type[DatatypeVariable])

    def test_check(self) -> None:
        assert_type(Datatype.check(Item), Datatype)
        super()._test_check(
            Datatype,
            success=[
                (Item, ItemDatatype()),
                (ItemDatatype, ItemDatatype()),
                (ItemDatatype(), ItemDatatype()),
                (Property, PropertyDatatype()),
                (PropertyDatatype, PropertyDatatype()),
                (PropertyDatatype(), PropertyDatatype()),
                (Lexeme, LexemeDatatype()),
                (LexemeDatatype, LexemeDatatype()),
                (LexemeDatatype(), LexemeDatatype()),
                (IRI, IRI_Datatype()),
                (IRI_Datatype, IRI_Datatype()),
                (IRI_Datatype(), IRI_Datatype()),
                (Text, TextDatatype()),
                (TextDatatype, TextDatatype()),
                (TextDatatype(), TextDatatype()),
                (String, StringDatatype()),
                (StringDatatype, StringDatatype()),
                (StringDatatype(), StringDatatype()),
                (ExternalId, ExternalIdDatatype()),
                (ExternalIdDatatype, ExternalIdDatatype()),
                (ExternalIdDatatype(), ExternalIdDatatype()),
                (Quantity, QuantityDatatype()),
                (QuantityDatatype, QuantityDatatype()),
                (QuantityDatatype(), QuantityDatatype()),
                (Time, TimeDatatype()),
                (TimeDatatype, TimeDatatype()),
                (TimeDatatype(), TimeDatatype()),
            ],
            failure=[None, 0, {}])

    def test__init__(self):
        super()._test__init__(
            Datatype,
            self.assert_datatype,
            success=[
                ([Item], ItemDatatype()),
                ([ItemDatatype], ItemDatatype()),
                ([ItemDatatype()], ItemDatatype()),
                ([Property], PropertyDatatype()),
                ([PropertyDatatype], PropertyDatatype()),
                ([PropertyDatatype()], PropertyDatatype()),
                ([Lexeme], LexemeDatatype()),
                ([LexemeDatatype], LexemeDatatype()),
                ([LexemeDatatype()], LexemeDatatype()),
                ([IRI], IRI_Datatype()),
                ([IRI_Datatype], IRI_Datatype()),
                ([IRI_Datatype()], IRI_Datatype()),
                ([Text], TextDatatype()),
                ([TextDatatype], TextDatatype()),
                ([TextDatatype()], TextDatatype()),
                ([String], StringDatatype()),
                ([StringDatatype], StringDatatype()),
                ([StringDatatype()], StringDatatype()),
                ([ExternalId], ExternalIdDatatype()),
                ([ExternalIdDatatype], ExternalIdDatatype()),
                ([ExternalIdDatatype()], ExternalIdDatatype()),
                ([Quantity], QuantityDatatype()),
                ([QuantityDatatype], QuantityDatatype()),
                ([QuantityDatatype()], QuantityDatatype()),
                ([Time], TimeDatatype()),
                ([TimeDatatype], TimeDatatype()),
                ([TimeDatatype()], TimeDatatype()),
            ],
            failure=[
                [None], [0], [{}],
            ])

    def test__from_rdflib(self):
        from kif_lib.namespace import WIKIBASE
        self.assert_raises_bad_argument(
            TypeError, 1, 'uri',
            'cannot coerce LexemeDatatype into ItemDatatype',
            ItemDatatype._from_rdflib, WIKIBASE.WikibaseLexeme)
        # fallback
        self.assert_string_datatype(Datatype._from_rdflib(WIKIBASE.claim))
        # item
        self.assert_item_datatype(
            ItemDatatype._from_rdflib(WIKIBASE.WikibaseItem))
        self.assert_item_datatype(
            Datatype._from_rdflib(WIKIBASE.WikibaseItem))
        # property
        self.assert_property_datatype(
            PropertyDatatype._from_rdflib(WIKIBASE.WikibaseProperty))
        self.assert_property_datatype(
            Datatype._from_rdflib(WIKIBASE.WikibaseProperty))
        # lexeme
        self.assert_lexeme_datatype(
            LexemeDatatype._from_rdflib(WIKIBASE.WikibaseLexeme))
        self.assert_lexeme_datatype(
            Datatype._from_rdflib(WIKIBASE.WikibaseLexeme))
        # iri
        self.assert_iri_datatype(IRI_Datatype._from_rdflib(WIKIBASE.Url))
        self.assert_iri_datatype(Datatype._from_rdflib(WIKIBASE.Url))
        # text
        self.assert_text_datatype(
            TextDatatype._from_rdflib(WIKIBASE.Monolingualtext))
        self.assert_text_datatype(
            Datatype._from_rdflib(WIKIBASE.Monolingualtext))
        # string
        self.assert_string_datatype(
            StringDatatype._from_rdflib(WIKIBASE.String))
        self.assert_string_datatype(Datatype._from_rdflib(WIKIBASE.String))
        # external id
        self.assert_external_id_datatype(
            ExternalIdDatatype._from_rdflib(WIKIBASE.ExternalId))
        self.assert_external_id_datatype(
            Datatype._from_rdflib(WIKIBASE.ExternalId))
        # quantity
        self.assert_quantity_datatype(
            QuantityDatatype._from_rdflib(WIKIBASE.Quantity))
        self.assert_quantity_datatype(
            Datatype._from_rdflib(WIKIBASE.Quantity))
        # time
        self.assert_time_datatype(TimeDatatype._from_rdflib(WIKIBASE.Time))
        self.assert_time_datatype(Datatype._from_rdflib(WIKIBASE.Time))

    def test__to_rdflib(self):
        from kif_lib.namespace import WIKIBASE
        self.assertEqual(
            ItemDatatype()._to_rdflib(), WIKIBASE.WikibaseItem)
        self.assertEqual(
            PropertyDatatype()._to_rdflib(), WIKIBASE.WikibaseProperty)
        self.assertEqual(
            LexemeDatatype()._to_rdflib(), WIKIBASE.WikibaseLexeme)
        self.assertEqual(
            IRI_Datatype()._to_rdflib(), WIKIBASE.Url)
        self.assertEqual(
            TextDatatype()._to_rdflib(), WIKIBASE.Monolingualtext)
        self.assertEqual(
            StringDatatype()._to_rdflib(), WIKIBASE.String)
        self.assertEqual(
            ExternalIdDatatype()._to_rdflib(), WIKIBASE.ExternalId)
        self.assertEqual(
            QuantityDatatype()._to_rdflib(), WIKIBASE.Quantity)
        self.assertEqual(
            TimeDatatype()._to_rdflib(), WIKIBASE.Time)


if __name__ == '__main__':
    Test.main()
