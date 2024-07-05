# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal
import re

from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    Datatype,
    Deprecated,
    EncoderError,
    Entity,
    EntityFingerprint,
    ExternalId,
    ExternalIdDatatype,
    FilterPattern,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    ItemDescriptor,
    KIF_Object,
    Lexeme,
    LexemeDatatype,
    LexemeDescriptor,
    Normal,
    NoValueSnak,
    Preferred,
    Property,
    PropertyDatatype,
    PropertyDescriptor,
    PropertyFingerprint,
    Quantity,
    QuantityDatatype,
    ReferenceRecord,
    ReferenceRecordSet,
    Snak,
    SnakSet,
    SomeValueSnak,
    Statement,
    String,
    StringDatatype,
    Text,
    TextDatatype,
    TextSet,
    Time,
    TimeDatatype,
    ValueSet,
    ValueSnak,
    Variable,
    Variables,
)
from kif_lib.model import (
    DatatypeVariable,
    DataValueVariable,
    DeepDataValueVariable,
    EntityVariable,
    ExternalIdTemplate,
    ExternalIdVariable,
    IRI_Template,
    IRI_Variable,
    ItemTemplate,
    ItemVariable,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    PropertyTemplate,
    PropertyVariable,
    QuantityTemplate,
    QuantityVariable,
    ShallowDataValueVariable,
    SnakVariable,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    StatementTemplate,
    StatementVariable,
    StringTemplate,
    StringVariable,
    TextTemplate,
    TextVariable,
    TimeTemplate,
    TimeVariable,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueVariable,
)
from kif_lib.typing import cast

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, KIF_Object)

    def test_kif_object_pyi(self):
        defined = set(filter(
            re.compile(r'^[a-z]').match,
            dir(KIF_Object)))
        defined -= {
            '_check_arg_callable_details',
            '_check_arg_isinstance_details',
            '_check_arg_isinstance_exception',
            '_check_arg_issubclass_details',
            'count',
            'index',
        }

        def get_decl(path):
            with open(path) as fp:
                return set(re.findall(
                    r'def\b\s*'
                    r'([a-z]\w*|_check_arg_\w*|_check_optional_arg_\w*)',
                    fp.read()))
        declared = get_decl('kif_lib/model/object.py')
        declared_pyi = get_decl('kif_lib/model/kif_object.pyi')
        self.assertEqual(defined - declared, declared_pyi)

# == __new__ ===============================================================

    def test__new__(self):
        self.assertIsInstance(Item('x'), Item)
        self.assertIsInstance(ItemTemplate('x'), Item)
        self.assertIsInstance(Item(iri='x'), Item)
        self.assertIsInstance(ItemTemplate(iri='x'), Item)
        self.assertIsInstance(Item(IRI_Variable('x')), ItemTemplate)
        self.assertIsInstance(ItemTemplate(IRI_Variable('x')), ItemTemplate)
        self.assertIsInstance(Item(iri=IRI_Variable('x')), ItemTemplate)
        self.assertIsInstance(
            ItemTemplate(iri=IRI_Variable('x')), ItemTemplate)

# == Auto-defined stuff ====================================================
# -- test_is_ --------------------------------------------------------------

    def test_is(self):
        self.assert_test_is_defined_for_kif_object_classes('is_')

    def test_is_annotation_record(self):
        self.assertTrue(AnnotationRecord().is_annotation_record())
        self.assertTrue(AnnotationRecord().test_annotation_record())
        self.assertFalse(Item('x').is_annotation_record())
        self.assertFalse(PropertyDescriptor().test_annotation_record())

    def test_is_annotation_record_set(self):
        self.assertTrue(AnnotationRecordSet().is_annotation_record_set())
        self.assertTrue(
            AnnotationRecordSet(AnnotationRecord()).
            test_annotation_record_set())
        self.assertFalse(Item('x').is_annotation_record_set())
        self.assertFalse(SnakSet().test_annotation_record_set())

    def test_is_descriptor(self):
        self.assertTrue(ItemDescriptor().is_descriptor())
        self.assertTrue(ItemDescriptor().test_descriptor())
        self.assertFalse(Item('x').is_descriptor())
        self.assertFalse(SnakSet().test_descriptor())

    def test_is_datatype(self):
        self.assertTrue(Datatype(Item).is_datatype())
        self.assertTrue(ItemDatatype().is_datatype())
        self.assertTrue(IRI_Datatype().test_datatype())
        self.assertFalse(Item('x').is_datatype())
        self.assertFalse(Item('x').test_datatype())

    def test_is_datatype_variable(self):
        self.assertTrue(DatatypeVariable('x').is_datatype_variable())
        self.assertTrue(DatatypeVariable('x').test_datatype_variable())
        self.assertFalse(ItemVariable('x').is_datatype_variable())
        self.assertFalse(ItemVariable('x').test_datatype_variable())

    def test_is_data_value(self):
        self.assertTrue(IRI('x').is_data_value())
        self.assertTrue(IRI('x').test_data_value())
        self.assertFalse(Item('x').is_data_value())
        self.assertFalse(Item('x').test_data_value())

    def test_is_data_value_template(self):
        self.assertTrue(
            IRI_Template(Variable('x')).is_data_value_template())
        self.assertTrue(
            IRI_Template(Variable('x')).test_data_value_template())
        self.assertFalse(
            ItemTemplate(Variable('x')).is_data_value_template())
        self.assertFalse(
            ItemTemplate(Variable('x')).test_data_value_template())

    def test_is_data_value_variable(self):
        self.assertTrue(DataValueVariable('x').is_data_value_variable())
        self.assertTrue(DataValueVariable('x').test_data_value_variable())
        self.assertTrue(IRI_Variable('x').is_data_value_variable())
        self.assertTrue(IRI_Variable('x').test_data_value_variable())
        self.assertFalse(ItemVariable('x').is_data_value_variable())
        self.assertFalse(ItemVariable('x').test_data_value_variable())

    def test_is_deep_data_value(self):
        self.assertTrue(Quantity(0).is_deep_data_value())
        self.assertTrue(Quantity(0).test_deep_data_value())
        self.assertFalse(String('x').is_deep_data_value())
        self.assertFalse(String('x').test_deep_data_value())

    def test_is_deep_data_value_template(self):
        self.assertTrue(
            QuantityTemplate(Variable('x')).is_deep_data_value_template())
        self.assertTrue(
            QuantityTemplate(Variable('x')).test_deep_data_value_template())
        self.assertFalse(
            StringTemplate(Variable('x')).is_deep_data_value_template())
        self.assertFalse(
            StringTemplate(Variable('x')).test_deep_data_value_template())

    def test_is_deep_data_value_variable(self):
        self.assertTrue(
            DeepDataValueVariable('x').is_deep_data_value_variable())
        self.assertTrue(
            DeepDataValueVariable('x').test_deep_data_value_variable())
        self.assertTrue(
            QuantityVariable('x').is_deep_data_value_variable())
        self.assertTrue(
            QuantityVariable('x').test_deep_data_value_variable())
        self.assertFalse(ItemVariable('x').is_deep_data_value_variable())
        self.assertFalse(ItemVariable('x').test_deep_data_value_variable())
        self.assertFalse(StringVariable('x').is_deep_data_value_variable())
        self.assertFalse(StringVariable('x').test_deep_data_value_variable())

    def test_is_deprecated_rank(self):
        self.assertTrue(Deprecated.is_deprecated_rank())
        self.assertTrue(Deprecated.test_deprecated_rank())
        self.assertFalse(Preferred.is_deprecated_rank())
        self.assertFalse(Preferred.test_deprecated_rank())

    def test_is_kif_object(self):
        self.assertTrue(Item('x').is_kif_object())
        self.assertTrue(Item('x').test_kif_object())

    def test_is_kif_object_set(self):
        pass

    def test_is_entity(self):
        self.assertTrue(Item('x').is_entity())
        self.assertTrue(Item('x').test_entity())
        self.assertFalse(String('x').is_entity())
        self.assertFalse(String('x').test_entity())

    def test_is_entity_fingerprint(self):
        self.assertTrue(EntityFingerprint(Item('x')).is_entity_fingerprint())
        self.assertTrue(
            EntityFingerprint(SnakSet()).test_entity_fingerprint())
        self.assertFalse(Item('x').is_entity_fingerprint())
        self.assertFalse(String('x').test_entity_fingerprint())

    def test_is_entity_template(self):
        self.assertTrue(ItemTemplate(Variable('x')).is_entity_template())
        self.assertTrue(ItemTemplate(Variable('x')).test_entity_template())
        self.assertFalse(StringTemplate(Variable('x')).is_entity_template())
        self.assertFalse(StringTemplate(Variable('x')).test_entity_template())

    def test_is_entity_variable(self):
        self.assertTrue(EntityVariable('x').is_entity_variable())
        self.assertTrue(EntityVariable('x').test_entity_variable())
        self.assertTrue(ItemVariable('x').is_entity_variable())
        self.assertTrue(ItemVariable('x').test_entity_variable())
        self.assertFalse(StringVariable('x').is_entity_variable())
        self.assertFalse(StringVariable('x').test_entity_variable())

    def test_is_external_id(self):
        self.assertTrue(ExternalId('x').is_external_id())
        self.assertTrue(ExternalId('x').test_external_id())
        self.assertFalse(String('x').is_external_id())
        self.assertFalse(Item('x').test_external_id())

    def test_is_external_id_datatype(self):
        self.assertTrue(ExternalIdDatatype().is_external_id_datatype())
        self.assertTrue(ExternalIdDatatype().test_external_id_datatype())
        self.assertFalse(ItemDatatype().is_external_id_datatype())
        self.assertFalse(Item('x').test_external_id_datatype())

    def test_is_external_id_template(self):
        self.assertTrue(
            ExternalIdTemplate(Variable('x')).is_external_id_template())
        self.assertTrue(
            ExternalIdTemplate(Variable('x')).test_external_id_template())
        self.assertFalse(
            StringTemplate(Variable('x')).is_external_id_template())
        self.assertFalse(
            StringTemplate(Variable('x')).test_external_id_template())

    def test_is_external_id_variable(self):
        self.assertTrue(ExternalIdVariable('x').is_external_id_variable())
        self.assertTrue(ExternalIdVariable('x').test_external_id_variable())
        self.assertFalse(StringVariable('x').is_external_id_variable())
        self.assertFalse(StringVariable('x').test_external_id_variable())

    def test_is_filter_pattern(self):
        self.assertTrue(FilterPattern().is_filter_pattern())
        self.assertTrue(FilterPattern().test_filter_pattern())
        self.assertFalse(String('x').is_filter_pattern())
        self.assertFalse(String('x').test_filter_pattern())

    def test_is_fingerprint(self):
        self.assertTrue(EntityFingerprint(Item('x')).is_fingerprint())
        self.assertTrue(EntityFingerprint(SnakSet()).test_fingerprint())
        self.assertFalse(Item('x').is_fingerprint())
        self.assertFalse(String('x').test_fingerprint())

    def test_is_iri(self):
        self.assertTrue(IRI('x').is_iri())
        self.assertTrue(IRI('x').test_iri())
        self.assertFalse(Item('x').is_iri())
        self.assertFalse(Item('x').test_iri())

    def test_is_iri_datatype(self):
        self.assertTrue(IRI_Datatype().is_iri_datatype())
        self.assertTrue(IRI_Datatype().test_iri_datatype())
        self.assertFalse(PropertyDatatype().is_iri_datatype())
        self.assertFalse(Item('x').test_iri_datatype())

    def test_is_iri_template(self):
        self.assertTrue(IRI_Template(Variable('x')).is_iri_template())
        self.assertTrue(IRI_Template(Variable('x')).test_iri_template())
        self.assertFalse(StringTemplate(Variable('x')).is_iri_template())
        self.assertFalse(StringTemplate(Variable('x')).test_iri_template())

    def test_is_iri_variable(self):
        self.assertTrue(IRI_Variable('x').is_iri_variable())
        self.assertTrue(IRI_Variable('x').test_iri_variable())
        self.assertFalse(StringVariable('x').is_iri_variable())
        self.assertFalse(StringVariable('x').test_iri_variable())

    def test_is_item(self):
        self.assertTrue(Item('x').is_item())
        self.assertTrue(Item('x').test_item())
        self.assertFalse(String('x').is_item())
        self.assertFalse(String('x').test_item())

    def test_is_item_datatype(self):
        self.assertTrue(ItemDatatype().is_item_datatype())
        self.assertTrue(ItemDatatype().test_item_datatype())
        self.assertFalse(PropertyDatatype().is_item_datatype())
        self.assertFalse(Item('x').test_item_datatype())

    def test_is_item_descriptor(self):
        self.assertTrue(ItemDescriptor().is_item_descriptor())
        self.assertTrue(ItemDescriptor().test_item_descriptor())
        self.assertFalse(Item('x').is_item_descriptor())
        self.assertFalse(PropertyDescriptor().test_item_descriptor())

    def test_is_item_template(self):
        self.assertTrue(ItemTemplate(Variable('x')).is_item_template())
        self.assertTrue(ItemTemplate(Variable('x')).test_item_template())
        self.assertFalse(StringTemplate(Variable('x')).is_item_template())
        self.assertFalse(StringTemplate(Variable('x')).test_item_template())

    def test_is_item_variable(self):
        self.assertTrue(ItemVariable('x').is_item_variable())
        self.assertTrue(ItemVariable('x').test_item_variable())
        self.assertFalse(StringVariable('x').is_item_variable())
        self.assertFalse(StringVariable('x').test_item_variable())

    def test_is_lexeme(self):
        self.assertTrue(Lexeme('x').is_lexeme())
        self.assertTrue(Lexeme('x').test_lexeme())
        self.assertFalse(String('x').is_lexeme())
        self.assertFalse(String('x').test_lexeme())

    def test_is_lexeme_datatype(self):
        self.assertTrue(LexemeDatatype().is_lexeme_datatype())
        self.assertTrue(LexemeDatatype().test_lexeme_datatype())
        self.assertFalse(StringDatatype().is_lexeme_datatype())
        self.assertFalse(String('x').test_lexeme_datatype())

    def test_is_lexeme_descriptor(self):
        self.assertTrue(LexemeDescriptor(
            'x', Item('x'), Item('x')).is_lexeme_descriptor())
        self.assertTrue(LexemeDescriptor(
            'x', Item('x'), Item('x')).test_lexeme_descriptor())
        self.assertFalse(String('x').is_lexeme_descriptor())
        self.assertFalse(String('x').test_lexeme_descriptor())

    def test_is_lexeme_template(self):
        self.assertTrue(LexemeTemplate(Variable('x')).is_lexeme_template())
        self.assertTrue(LexemeTemplate(Variable('x')).test_lexeme_template())
        self.assertFalse(StringTemplate(Variable('x')).is_lexeme_template())
        self.assertFalse(StringTemplate(Variable('x')).test_lexeme_template())

    def test_is_lexeme_variable(self):
        self.assertTrue(LexemeVariable('x').is_lexeme_variable())
        self.assertTrue(LexemeVariable('x').test_lexeme_variable())
        self.assertFalse(StringVariable('x').is_lexeme_variable())
        self.assertFalse(StringVariable('x').test_lexeme_variable())

    def test_is_no_value_snak(self):
        snak = NoValueSnak(Property('x'))
        self.assertTrue(snak.is_no_value_snak())
        self.assertTrue(snak.test_no_value_snak())
        self.assertFalse(String('x').is_no_value_snak())
        self.assertFalse(String('x').test_no_value_snak())

    def test_is_no_value_snak_template(self):
        self.assertTrue(
            NoValueSnakTemplate(
                Variable('x')).is_no_value_snak_template())
        self.assertTrue(
            NoValueSnakTemplate(
                Variable('x')).test_no_value_snak_template())
        self.assertFalse(
            ValueSnakTemplate(
                *Variables('x', 'y')).is_no_value_snak_template())
        self.assertFalse(
            ValueSnakTemplate(
                *Variables('x', 'y')).test_no_value_snak_template())

    def test_is_no_value_snak_variable(self):
        self.assertTrue(
            NoValueSnakVariable('x').is_no_value_snak_variable())
        self.assertTrue(
            NoValueSnakVariable('x').test_no_value_snak_variable())
        self.assertFalse(
            SnakVariable('x').is_no_value_snak_variable())
        self.assertFalse(
            SnakVariable('x').test_no_value_snak_variable())
        self.assertFalse(
            SomeValueSnakVariable('x').is_no_value_snak_variable())
        self.assertFalse(
            SomeValueSnakVariable('x').test_no_value_snak_variable())

    def test_is_normal_rank(self):
        self.assertTrue(Normal.is_normal_rank())
        self.assertTrue(Normal.test_normal_rank())
        self.assertFalse(Preferred.is_normal_rank())
        self.assertFalse(Preferred.test_normal_rank())

    def test_is_pattern(self):
        pass

    def test_is_plain_descriptor(self):
        self.assertTrue(ItemDescriptor().is_plain_descriptor())
        self.assertTrue(PropertyDescriptor().test_plain_descriptor())
        self.assertFalse(Item('x').is_plain_descriptor())
        self.assertFalse(LexemeDescriptor(
            'x', Item('x'), Item('x')).test_plain_descriptor())

    def test_is_preferred_rank(self):
        self.assertTrue(Preferred.is_preferred_rank())
        self.assertTrue(Preferred.test_preferred_rank())
        self.assertFalse(Normal.is_preferred_rank())
        self.assertFalse(Normal.test_preferred_rank())

    def test_is_property(self):
        self.assertTrue(Property('x').is_property())
        self.assertTrue(Property('x').test_property())
        self.assertFalse(Item('x').is_property())
        self.assertFalse(Item('x').test_property())

    def test_is_property_datatype(self):
        self.assertTrue(PropertyDatatype().is_property_datatype())
        self.assertTrue(PropertyDatatype().test_property_datatype())
        self.assertFalse(ItemDatatype().is_property_datatype())
        self.assertFalse(Item('x').test_property_datatype())

    def test_is_property_descriptor(self):
        self.assertTrue(PropertyDescriptor().is_property_descriptor())
        self.assertTrue(PropertyDescriptor().test_property_descriptor())
        self.assertFalse(Item('x').is_property_descriptor())
        self.assertFalse(ItemDescriptor().test_property_descriptor())

    def test_is_property_fingerprint(self):
        self.assertTrue(
            PropertyFingerprint(Property('x')).is_property_fingerprint())
        self.assertTrue(
            PropertyFingerprint(SnakSet()).test_property_fingerprint())
        self.assertFalse(Item('x').is_property_fingerprint())
        self.assertFalse(String('x').test_property_fingerprint())

    def test_is_property_template(self):
        self.assertTrue(
            PropertyTemplate(Variable('x')).is_property_template())
        self.assertTrue(
            PropertyTemplate(Variable('x')).test_property_template())
        self.assertFalse(
            StringTemplate(Variable('x')).is_property_template())
        self.assertFalse(
            StringTemplate(Variable('x')).test_property_template())

    def test_is_property_variable(self):
        self.assertTrue(PropertyVariable('x').is_property_variable())
        self.assertTrue(PropertyVariable('x').test_property_variable())
        self.assertFalse(StringVariable('x').is_property_variable())
        self.assertFalse(StringVariable('x').test_property_variable())

    def test_is_quantity(self):
        self.assertTrue(Quantity(0).is_quantity())
        self.assertTrue(Quantity(0).test_quantity())
        self.assertFalse(String('x').is_quantity())
        self.assertFalse(String('x').test_quantity())

    def test_is_quantity_datatype(self):
        self.assertTrue(QuantityDatatype().is_quantity_datatype())
        self.assertTrue(QuantityDatatype().test_quantity_datatype())
        self.assertFalse(ItemDatatype().is_quantity_datatype())
        self.assertFalse(Item('x').test_quantity_datatype())

    def test_is_quantity_template(self):
        self.assertTrue(
            QuantityTemplate(Variable('x')).is_quantity_template())
        self.assertTrue(
            QuantityTemplate(Variable('x')).test_quantity_template())
        self.assertFalse(
            ItemTemplate(Variable('x')).is_quantity_template())
        self.assertFalse(
            ItemTemplate(Variable('x')).test_quantity_template())

    def test_is_quantity_variable(self):
        self.assertTrue(QuantityVariable('x').is_quantity_variable())
        self.assertTrue(QuantityVariable('x').test_quantity_variable())
        self.assertFalse(ItemVariable('x').is_quantity_variable())
        self.assertFalse(ItemVariable('x').test_quantity_variable())

    def test_is_rank(self):
        self.assertTrue(Preferred.is_rank())
        self.assertTrue(Preferred.test_rank())
        self.assertFalse(String('x').is_rank())
        self.assertFalse(String('x').test_rank())

    def test_is_reference_record(self):
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertTrue(refr.is_reference_record())
        self.assertTrue(refr.test_reference_record())
        self.assertFalse(String('x').is_reference_record())
        self.assertFalse(String('x').test_reference_record())

    def test_is_reference_record_set(self):
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertTrue(ReferenceRecordSet().is_reference_record_set())
        self.assertTrue(ReferenceRecordSet(refr).test_reference_record_set())
        self.assertFalse(String('x').is_reference_record_set())
        self.assertFalse(refr.test_reference_record_set())

    def test_is_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertTrue(snak.is_snak())
        self.assertTrue(snak.test_snak())
        self.assertFalse(String('x').is_snak())
        self.assertFalse(String('x').test_snak())

    def test_is_snak_template(self):
        self.assertTrue(
            SomeValueSnakTemplate(Variable('x')).is_snak_template())
        self.assertTrue(
            SomeValueSnakTemplate(Variable('x')).test_snak_template())
        self.assertFalse(IRI_Template(Variable('x')).is_snak_template())
        self.assertFalse(IRI_Template(Variable('x')).test_snak_template())

    def test_is_snak_variable(self):
        self.assertTrue(SnakVariable('x').is_snak_variable())
        self.assertTrue(SnakVariable('x').test_snak_variable())
        self.assertTrue(SomeValueSnakVariable('x').is_snak_variable())
        self.assertTrue(SomeValueSnakVariable('x').test_snak_variable())
        self.assertFalse(ItemVariable('x').is_snak_variable())
        self.assertFalse(ItemVariable('x').test_snak_variable())

    def test_is_snak_set(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertTrue(SnakSet().is_snak_set())
        self.assertTrue(SnakSet(snak).test_snak_set())
        self.assertFalse(String('x').is_snak_set())
        self.assertFalse(snak.test_snak_set())

    def test_is_shallow_data_value(self):
        self.assertTrue(String('').is_shallow_data_value())
        self.assertTrue(Text('').test_shallow_data_value())
        self.assertFalse(Quantity(0).is_shallow_data_value())
        self.assertFalse(Quantity(0).test_shallow_data_value())

    def test_is_shallow_data_value_template(self):
        self.assertTrue(
            IRI_Template(Variable('x')).is_shallow_data_value_template())
        self.assertTrue(
            IRI_Template(Variable('x')).test_shallow_data_value_template())
        self.assertFalse(
            ItemTemplate(Variable('x')).is_shallow_data_value_template())
        self.assertFalse(
            ItemTemplate(Variable('x')).test_shallow_data_value_template())

    def test_is_shallow_data_value_variable(self):
        self.assertTrue(
            ShallowDataValueVariable('x').is_shallow_data_value_variable())
        self.assertTrue(
            ShallowDataValueVariable('x').test_shallow_data_value_variable())
        self.assertTrue(IRI_Variable('x').is_shallow_data_value_variable())
        self.assertTrue(IRI_Variable('x').test_shallow_data_value_variable())
        self.assertFalse(ItemVariable('x').is_shallow_data_value_variable())
        self.assertFalse(ItemVariable('x').test_shallow_data_value_variable())

    def test_is_some_value_snak(self):
        snak = SomeValueSnak(Property('x'))
        self.assertTrue(snak.is_some_value_snak())
        self.assertTrue(snak.test_some_value_snak())
        self.assertFalse(String('x').is_some_value_snak())
        self.assertFalse(String('x').test_some_value_snak())

    def test_is_some_value_snak_template(self):
        self.assertTrue(
            SomeValueSnakTemplate(
                Variable('x')).is_some_value_snak_template())
        self.assertTrue(
            SomeValueSnakTemplate(
                Variable('x')).test_some_value_snak_template())
        self.assertFalse(
            NoValueSnakTemplate(
                Variable('x')).is_some_value_snak_template())
        self.assertFalse(
            NoValueSnakTemplate(
                Variable('x')).test_some_value_snak_template())

    def test_is_some_value_snak_variable(self):
        self.assertTrue(
            SomeValueSnakVariable('x').is_some_value_snak_variable())
        self.assertTrue(
            SomeValueSnakVariable('x').test_some_value_snak_variable())
        self.assertFalse(
            SnakVariable('x').is_some_value_snak_variable())
        self.assertFalse(
            SnakVariable('x').test_some_value_snak_variable())
        self.assertFalse(
            NoValueSnakVariable('x').is_some_value_snak_variable())
        self.assertFalse(
            NoValueSnakVariable('x').test_some_value_snak_variable())

    def test_is_statement(self):
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertTrue(stmt.is_statement())
        self.assertTrue(stmt.test_statement())
        self.assertFalse(String('x').is_statement())
        self.assertFalse(String('x').test_statement())

    def test_is_statement_template(self):
        self.assertTrue(
            StatementTemplate(*Variables('x', 'y')).is_statement_template())
        self.assertFalse(
            NoValueSnakTemplate(Variable('x')).is_statement_template())

    def test_is_statement_variable(self):
        self.assertTrue(StatementVariable('x').is_statement_variable())
        self.assertFalse(NoValueSnakVariable('x').test_statement_variable())

    def test_is_string(self):
        self.assertTrue(String('x').is_string())
        self.assertTrue(String('x').test_string())
        self.assertFalse(Item('x').is_string())
        self.assertFalse(Item('x').test_string())

    def test_is_string_datatype(self):
        self.assertTrue(StringDatatype().is_string_datatype())
        self.assertTrue(StringDatatype().test_string_datatype())
        self.assertTrue(ExternalIdDatatype().test_string_datatype())
        self.assertFalse(PropertyDatatype().is_string_datatype())
        self.assertFalse(Item('x').test_string_datatype())

    def test_is_string_template(self):
        self.assertTrue(StringTemplate(Variable('x')).is_string_template())
        self.assertTrue(StringTemplate(Variable('x')).test_string_template())
        self.assertFalse(ItemTemplate(Variable('x')).is_string_template())
        self.assertFalse(ItemTemplate(Variable('x')).test_string_template())

    def test_is_string_variable(self):
        self.assertTrue(StringVariable('x').is_string_variable())
        self.assertTrue(StringVariable('x').test_string_variable())
        self.assertFalse(ItemVariable('x').is_string_variable())
        self.assertFalse(ItemVariable('x').test_string_variable())

    def test_is_template(self):
        self.assertTrue(TextTemplate(Variable('x')).is_template())
        self.assertFalse(String('x').is_template())

    def test_is_text(self):
        self.assertTrue(Text('').is_text())
        self.assertTrue(Text('abc', 'pt').test_text())
        self.assertFalse(String('x').is_quantity())
        self.assertFalse(String('x').test_quantity())

    def test_is_text_datatype(self):
        self.assertTrue(TextDatatype().is_text_datatype())
        self.assertTrue(TextDatatype().test_text_datatype())
        self.assertFalse(PropertyDatatype().is_text_datatype())
        self.assertFalse(Item('x').test_text_datatype())

    def test_is_text_set(self):
        text = Text('x')
        self.assertTrue(TextSet().is_text_set())
        self.assertTrue(TextSet(text).test_text_set())
        self.assertFalse(String('x').is_text_set())
        self.assertFalse(SnakSet().test_text_set())

    def test_is_text_template(self):
        self.assertTrue(TextTemplate(Variable('x')).is_text_template())
        self.assertTrue(TextTemplate(Variable('x')).test_text_template())
        self.assertFalse(ItemTemplate(Variable('x')).is_text_template())
        self.assertFalse(ItemTemplate(Variable('x')).test_text_template())

    def test_is_text_variable(self):
        self.assertTrue(TextVariable('x').is_text_variable())
        self.assertTrue(TextVariable('x').test_text_variable())
        self.assertFalse(ItemVariable('x').is_text_variable())
        self.assertFalse(ItemVariable('x').test_text_variable())

    def test_is_time(self):
        self.assertTrue(Time('2023-09-18').is_time())
        self.assertTrue(Time('2023-09-18').test_time())
        self.assertFalse(String('2023-09-18').is_time())
        self.assertFalse(String('2023-09-18').test_time())

    def test_is_time_datatype(self):
        self.assertTrue(TimeDatatype().is_time_datatype())
        self.assertTrue(TimeDatatype().test_time_datatype())
        self.assertFalse(PropertyDatatype().is_time_datatype())
        self.assertFalse(Item('x').test_time_datatype())

    def test_is_time_template(self):
        self.assertTrue(TimeTemplate(Variable('x')).is_time_template())
        self.assertTrue(TimeTemplate(Variable('x')).test_time_template())
        self.assertFalse(ItemTemplate(Variable('x')).is_time_template())
        self.assertFalse(ItemTemplate(Variable('x')).test_time_template())

    def test_is_time_variable(self):
        self.assertTrue(TimeVariable('x').is_time_variable())
        self.assertTrue(TimeVariable('x').test_time_variable())
        self.assertFalse(ItemVariable('x').is_time_variable())
        self.assertFalse(ItemVariable('x').test_time_variable())

    def test_is_value(self):
        self.assertTrue(Item('x').is_value())
        self.assertTrue(Item('x').test_value())
        self.assertFalse(NoValueSnak(Property('x')).is_value())
        self.assertFalse(NoValueSnak(Property('x')).test_value())

    def test_is_value_template(self):
        self.assertTrue(TimeTemplate(Variable('x')).is_value_template())
        self.assertTrue(TimeTemplate(Variable('x')).test_value_template())
        self.assertFalse(
            NoValueSnakTemplate(Variable('x')).is_value_template())
        self.assertFalse(
            NoValueSnakTemplate(Variable('x')).test_value_template())

    def test_is_value_variable(self):
        self.assertTrue(ValueVariable('x').is_value_variable())
        self.assertTrue(ValueVariable('x').test_value_variable())
        self.assertTrue(ItemVariable('x').is_value_variable())
        self.assertTrue(ItemVariable('x').test_value_variable())
        self.assertFalse(NoValueSnakVariable('x').is_value_variable())
        self.assertFalse(NoValueSnakVariable('x').test_value_variable())

    def test_is_value_set(self):
        value = Item('x')
        self.assertTrue(ValueSet().is_value_set())
        self.assertTrue(ValueSet(value).test_value_set())
        self.assertFalse(String('x').is_value_set())
        self.assertFalse(SnakSet().test_value_set())

    def test_is_value_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertTrue(snak.is_value_snak())
        self.assertTrue(snak.test_value_snak())
        self.assertFalse(String('x').is_value_snak())
        self.assertFalse(String('x').test_value_snak())

    def test_is_value_snak_template(self):
        self.assertTrue(
            ValueSnakTemplate(*Variables('x', 'y')).is_value_snak_template())
        self.assertTrue(
            ValueSnakTemplate(*Variables('x', 'y')).test_value_snak_template())
        self.assertFalse(
            NoValueSnakTemplate(Variable('x')).is_value_snak_template())
        self.assertFalse(
            NoValueSnakTemplate(Variable('x')).test_value_snak_template())

    def test_is_value_snak_variable(self):
        self.assertTrue(ValueSnakVariable('x').is_value_snak_variable())
        self.assertTrue(ValueSnakVariable('x').test_value_snak_variable())
        self.assertFalse(SnakVariable('x').is_value_snak_variable())
        self.assertFalse(SnakVariable('x').test_value_snak_variable())
        self.assertFalse(NoValueSnakVariable('x').is_value_snak_variable())
        self.assertFalse(NoValueSnakVariable('x').test_value_snak_variable())

    def test_is_variable(self):
        self.assertTrue(Variable('x').is_variable())
        self.assertTrue(ItemVariable('x').test_variable())
        self.assertFalse(Item('x').is_variable())

# == misc ==================================================================

    def test__repr_markdown_(self):
        self.assertEqual(
            Item('x')._repr_markdown_(),
            '(**Item** [x](http://x))')

    def test_traverse(self):
        obj = Variable('p')(Item('x'), Quantity(5, Item('u')))
        self.assert_statement_template(
            obj, Item('x'), Variable('p')(Quantity(5, Item('u'))))
        self.assert_raises_bad_argument(
            TypeError, 1, 'filter', 'expected callable, got int',
            obj.traverse, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'visit', 'expected callable, got int',
            obj.traverse, None, 0)
        self.assertEqual(
            list(obj.traverse()), [
                obj,
                Item('x'),
                IRI('x'),
                'x',
                obj.snak,
                PropertyVariable('p'),
                'p',
                Quantity(5, Item('u')),
                decimal.Decimal(5),
                Item('u'),
                IRI('u'),
                'u',
                None,
                None])
        self.assertEqual(
            list(obj.traverse(IRI.test)), [IRI('x'), IRI('u')])
        self.assertEqual(
            list(obj.traverse(lambda x: isinstance(x, str))),
            ['x', 'p', 'u'])
        self.assertEqual(
            list(obj.traverse(None, lambda x: not isinstance(x, Entity))),
            [obj,
             obj.snak,
             PropertyVariable('p'),
             'p',
             cast(ValueSnak, obj.snak).value,
             decimal.Decimal(5),
             None,
             None])

# == Codecs ================================================================

    def test_repr_decoder_extensions(self):
        from kif_lib.model.kif_object import KIF_ReprDecoder
        dec = KIF_ReprDecoder()
        self.assertEqual(dec.decode('5'), 5)
        self.assertEqual(
            dec.decode('datetime.datetime(2024, 2, 6)'),
            datetime.datetime(2024, 2, 6))
        self.assertEqual(dec.decode("Decimal('.5')"), decimal.Decimal('.5'))
        self.assertEqual(dec.decode("set()"), set())

    def test_repr_encoder_extensions(self):
        from kif_lib.model.kif_object import KIF_ReprEncoder
        enc = KIF_ReprEncoder()
        self.assertEqual(enc.encode(IRI('x')), "IRI('x')")
        self.assertEqual(
            enc.encode(datetime.datetime(2024, 2, 6)),  # pyright: ignore
            'datetime.datetime(2024, 2, 6, 0, 0)')
        self.assertEqual(
            enc.encode(decimal.Decimal(0)), "Decimal('0')")  # pyright: ignore
        self.assertEqual(
            enc.encode(decimal.Decimal(3.5)),  # pyright: ignore
            "Decimal('3.5')")
        self.assertEqual(enc.encode(Snak.ALL), '7')      # pyright: ignore
        self.assertEqual(enc.encode(set()), 'set()')     # pyright: ignore

    def test_json_encoder_extensions(self):
        from kif_lib.model.kif_object import KIF_JSON_Encoder
        enc = KIF_JSON_Encoder()
        self.assertEqual(
            enc.encode(IRI('x')), '{"class": "IRI", "args": ["x"]}')
        self.assertEqual(
            enc.encode(datetime.datetime(2024, 2, 6)),  # pyright: ignore
            '"2024-02-06 00:00:00"')
        self.assertEqual(enc.encode(
            decimal.Decimal(0)), '"0"')  # pyright: ignore
        self.assertEqual(enc.encode(
            decimal.Decimal(3.5)), '"3.5"')  # pyright: ignore
        self.assertEqual(enc.encode(Snak.ALL), '"7"')      # pyright: ignore
        self.assertRaises(EncoderError, enc.encode, set())  # pyright: ignore

    def test_sexp_encoder_extensions(self):
        from kif_lib.model.kif_object import KIF_SExpEncoder
        enc = KIF_SExpEncoder()
        self.assertEqual(enc.encode(Preferred), 'PreferredRank')
        self.assertEqual(
            enc.encode(datetime.datetime(2024, 2, 6)),     # pyright: ignore
            '2024-02-06 00:00:00')                         # pyright: ignore
        self.assertEqual(
            enc.encode(decimal.Decimal(0)), '0')  # pyright: ignore
        self.assertEqual(
            enc.encode(decimal.Decimal(3.5)), '3.5')       # pyright: ignore
        self.assertEqual(enc.encode(Snak.ALL), '7')        # pyright: ignore
        self.assertRaises(EncoderError, enc.encode, set())  # pyright: ignore


if __name__ == '__main__':
    Test.main()
