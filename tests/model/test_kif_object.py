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
    Fingerprint,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    ItemDescriptor,
    KIF_Object,
    KIF_ObjectSet,
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
            re.compile(r'^([a-z]|_check_arg_|_check_optional_arg_)').match,
            dir(KIF_Object)))
        defined -= {
            '_check_arg_',
            '_check_arg__class',
            '_check_arg_callable_details',
            '_check_arg_isinstance_details',
            '_check_arg_isinstance_exception',
            '_check_arg_issubclass_details',
            '_check_optional_arg_',
            '_check_optional_arg__class',
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

# == Argument checking =====================================================

    def test__check_arg_kif_object_class(self):
        self.assertRaises(
            TypeError, KIF_Object._check_arg_kif_object_class, 0)
        self.assertRaises(
            ValueError, KIF_Object._check_arg_kif_object_class, int)
        self.assertIs(
            KIF_Object._check_arg_kif_object_class(KIF_Object), KIF_Object)
        self.assertIs(
            KIF_Object._check_arg_kif_object_class(Statement), Statement)

    def test__check_optional_arg_kif_object_class(self):
        self.assertRaises(
            TypeError, KIF_Object._check_optional_arg_kif_object_class, 0)
        self.assertIsNone(
            KIF_Object._check_optional_arg_kif_object_class(None))
        self.assertIs(
            KIF_Object._check_optional_arg_kif_object_class(None, Statement),
            Statement)
        self.assertIs(
            KIF_Object._check_optional_arg_kif_object_class(Item, Statement),
            Item)

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
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertTrue(SnakSet().is_kif_object_set())
        self.assertTrue(KIF_ObjectSet(snak).test_kif_object_set())
        self.assertFalse(String('x').is_kif_object_set())
        self.assertFalse(snak.test_kif_object_set())

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

# -- test_check_ -----------------------------------------------------------

    def test_check(self):
        self.assert_test_is_defined_for_kif_object_classes('check_')

    def test_check_annotation_record(self):
        self.assertEqual(
            AnnotationRecord().check_annotation_record(),
            AnnotationRecord())
        self.assertRaises(TypeError, Item('x').check_annotation_record)

    def test_check_annotation_record_set(self):
        annots = AnnotationRecordSet(AnnotationRecord())
        self.assertEqual(annots.check_annotation_record_set(), annots)
        self.assertRaises(TypeError, Item('x').check_annotation_record_set)

    def test_check_data_value(self):
        self.assertEqual(IRI('x').check_data_value(), IRI('x'))
        self.assertRaises(TypeError, Item('x').check_data_value)

    def test_check_data_value_template(self):
        self.assertEqual(
            IRI_Template(Variable('x')).check_data_value_template(),
            IRI_Template(Variable('x')))
        self.assertRaises(TypeError, IRI('x').check_data_value_template)

    def test_check_data_value_variable(self):
        self.assertEqual(
            DataValueVariable('x').check_data_value_variable(),
            DataValueVariable('x'))
        self.assertEqual(
            IRI_Variable('x').check_data_value_variable(), IRI_Variable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_data_value_variable)

    def test_check_datatype(self):
        self.assertEqual(IRI_Datatype().check_datatype(), IRI_Datatype())
        self.assertRaises(TypeError, Item('x').check_datatype)

    def test_check_datatype_variable(self):
        self.assertEqual(
            DatatypeVariable('x').check_datatype_variable(),
            DatatypeVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_datatype_variable)

    def test_check_deep_data_value(self):
        self.assertEqual(Quantity(0).check_deep_data_value(), Quantity(0))
        self.assertRaises(TypeError, String('x').check_deep_data_value)

    def test_check_deep_data_value_template(self):
        self.assertEqual(
            QuantityTemplate(Variable('x')).check_deep_data_value_template(),
            QuantityTemplate(Variable('x')))
        self.assertRaises(TypeError, IRI('x').check_deep_data_value_template)

    def test_check_deep_data_value_variable(self):
        self.assertEqual(
            DeepDataValueVariable('x').check_deep_data_value_variable(),
            DeepDataValueVariable('x'))
        self.assertEqual(
            QuantityVariable('x').check_deep_data_value_variable(),
            QuantityVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_deep_data_value_variable)

    def test_check_deprecated_rank(self):
        self.assertEqual(Deprecated.check_deprecated_rank(), Deprecated)
        self.assertRaises(TypeError, Preferred.check_deprecated_rank)

    def test_check_descriptor(self):
        self.assertEqual(
            ItemDescriptor('x').check_descriptor(), ItemDescriptor('x'))
        self.assertRaises(TypeError, String('x').check_descriptor)

    def test_check_entity(self):
        self.assertEqual(Item('x').check_entity(), Item('x'))
        self.assertRaises(TypeError, String('x').check_entity)

    def test_check_entity_fingerprint(self):
        fp = EntityFingerprint(Item('x'))
        self.assertEqual(fp.check_entity_fingerprint(), fp)
        self.assertRaises(TypeError, String('x').check_entity_fingerprint)

    def test_check_entity_template(self):
        self.assertEqual(
            ItemTemplate(Variable('x')).check_entity_template(),
            ItemTemplate(Variable('x')))
        self.assertRaises(
            TypeError, IRI_Template(Variable('x')).check_entity_template)

    def test_check_entity_variable(self):
        self.assertEqual(
            EntityVariable('x').check_entity_variable(), EntityVariable('x'))
        self.assertEqual(
            ItemVariable('x').check_entity_variable(), ItemVariable('x'))
        self.assertRaises(TypeError, IRI_Variable('x').check_entity_variable)

    def test_check_external_id(self):
        self.assertEqual(
            ExternalId('x').check_external_id(), ExternalId('x'))
        self.assertEqual(
            String('x').check_external_id(), ExternalId('x'))

    def test_check_external_id_datatype(self):
        self.assertEqual(
            ExternalIdDatatype().check_external_id_datatype(),
            ExternalIdDatatype())
        self.assertRaises(
            TypeError, ItemDatatype().check_external_id_datatype)

    def test_check_external_id_template(self):
        self.assertEqual(
            ExternalIdTemplate(Variable('x')).check_external_id_template(),
            ExternalIdTemplate(Variable('x')))
        self.assertRaises(
            TypeError,
            ItemTemplate(Variable('x')).check_external_id_template)

    def test_check_external_id_variable(self):
        self.assertEqual(
            ExternalIdVariable('x').check_external_id_variable(),
            ExternalIdVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_external_id_variable)

    def test_check_filter_pattern(self):
        self.assertEqual(
            FilterPattern().check_filter_pattern(), FilterPattern())
        self.assertRaises(TypeError, Item('x').check_filter_pattern)

    def test_check_fingerprint(self):
        fp = Fingerprint(String('x'))
        self.assertEqual(fp.check_fingerprint(), fp)
        self.assertRaises(TypeError, Item('x').check_fingerprint)

    def test_check_iri(self):
        self.assertEqual(IRI('x').check_iri(), IRI('x'))
        self.assertRaises(TypeError, Item('x').check_iri)

    def test_check_iri_datatype(self):
        self.assertEqual(
            IRI_Datatype().check_iri_datatype(), IRI_Datatype())
        self.assertRaises(TypeError, Item('x').check_iri_datatype)

    def test_check_iri_template(self):
        self.assertEqual(
            IRI_Template(Variable('x')).check_iri_template(),
            IRI_Template(Variable('x')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).check_iri_template)

    def test_check_iri_variable(self):
        self.assertEqual(
            IRI_Variable('x').check_iri_variable(), IRI_Variable('x'))
        self.assertRaises(TypeError, ItemVariable('x').check_iri_variable)

    def test_check_item(self):
        pass

    def test_check_item_datatype(self):
        self.assertEqual(ItemDatatype().check_item_datatype(), ItemDatatype())
        self.assertRaises(TypeError, String('x').check_item_datatype)

    def test_check_item_descriptor(self):
        self.assertEqual(
            ItemDescriptor().check_item_descriptor(), ItemDescriptor())
        self.assertRaises(
            TypeError, PropertyDescriptor().check_item_descriptor)

    def test_check_item_template(self):
        self.assertEqual(
            ItemTemplate(Variable('x')).check_item_template(),
            ItemTemplate(Variable('x')))
        self.assertRaises(
            TypeError, IRI_Template(Variable('x')).check_item_template)

    def test_check_item_variable(self):
        self.assertEqual(
            ItemVariable('x').check_item_variable(), ItemVariable('x'))
        self.assertRaises(TypeError, IRI_Variable('x').check_item_variable)

    def test_check_kif_object(self):
        self.assertEqual(Item('x').check_kif_object(), Item('x'))

    def test_check_kif_object_set(self):
        objs = KIF_ObjectSet(Item('x'), Property('y'))
        self.assertEqual(objs.check_kif_object_set(), objs)
        self.assertEqual(SnakSet().check_kif_object_set(), SnakSet())
        self.assertRaises(TypeError, Item('x').check_kif_object_set)

    def test_check_lexeme(self):
        self.assertEqual(Lexeme('x').check_lexeme(), Lexeme('x'))
        self.assertRaises(TypeError, Item('x').check_lexeme)

    def test_check_lexeme_datatype(self):
        self.assertEqual(
            LexemeDatatype().check_lexeme_datatype(), LexemeDatatype())
        self.assertRaises(TypeError, ItemDatatype().check_lexeme_datatype)

    def test_check_lexeme_descriptor(self):
        desc = LexemeDescriptor('x', Item('x'), Item('y'))
        self.assertEqual(desc.check_lexeme_descriptor(), desc)
        self.assertRaises(TypeError, Item('x').check_lexeme_descriptor)

    def test_check_lexeme_template(self):
        self.assertEqual(
            LexemeTemplate(Variable('x')).check_lexeme_template(),
            LexemeTemplate(Variable('x')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).check_lexeme_template)

    def test_check_lexeme_variable(self):
        self.assertEqual(
            LexemeVariable('x').check_lexeme_variable(), LexemeVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_lexeme_variable)

    def test_check_no_value_snak(self):
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.check_no_value_snak(), snak)
        self.assertRaises(TypeError, Item('x').check_no_value_snak)

    def test_check_no_value_snak_template(self):
        self.assertEqual(
            NoValueSnakTemplate(Variable('x')).check_no_value_snak_template(),
            NoValueSnakTemplate(Variable('x')))
        self.assertRaises(
            TypeError,
            SomeValueSnakTemplate(
                Variable('x')).check_no_value_snak_template)

    def test_check_no_value_snak_variable(self):
        self.assertEqual(
            NoValueSnakVariable('x').check_no_value_snak_variable(),
            NoValueSnakVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_no_value_snak_variable)

    def test_check_normal_rank(self):
        self.assertEqual(Normal.check_normal_rank(), Normal)
        self.assertRaises(TypeError, Preferred.check_normal_rank)

    def test_check_pattern(self):
        pass

    def test_check_plain_descriptor(self):
        self.assertEqual(
            ItemDescriptor().check_plain_descriptor(), ItemDescriptor())
        self.assertRaises(
            TypeError,
            LexemeDescriptor('abc', Item('x'),
                             Item('y')).check_plain_descriptor)

    def test_check_preferred_rank(self):
        self.assertEqual(Preferred.check_preferred_rank(), Preferred)
        self.assertRaises(TypeError, Normal.check_preferred_rank)

    def test_check_property(self):
        self.assertEqual(Property('x').check_property(), Property('x'))
        self.assertRaises(TypeError, Item('x').check_property)

    def test_check_property_datatype(self):
        self.assertEqual(
            PropertyDatatype().check_property_datatype(), PropertyDatatype())
        self.assertRaises(TypeError, ItemDatatype().check_property_datatype)

    def test_check_property_descriptor(self):
        self.assertEqual(
            PropertyDescriptor().check_property_descriptor(),
            PropertyDescriptor())
        self.assertRaises(
            TypeError, ItemDescriptor().check_property_descriptor)

    def test_check_property_fingerprint(self):
        fp = PropertyFingerprint(Property('p'))
        self.assertEqual(fp.check_property_fingerprint(), fp)
        self.assertRaises(
            TypeError, EntityFingerprint(Item('x')).check_property_fingerprint)

    def test_check_property_template(self):
        self.assertEqual(
            PropertyTemplate(Variable('x')).check_property_template(),
            PropertyTemplate(Variable('x')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).check_property_template)

    def test_check_property_variable(self):
        self.assertEqual(
            PropertyVariable('x').check_property_variable(),
            PropertyVariable('x'))
        self.assertRaises(TypeError, ItemVariable('x').check_property_variable)

    def test_check_quantity(self):
        self.assertEqual(Quantity(0).check_quantity(), Quantity(0))
        self.assertRaises(ValueError, String('x').check_quantity)

    def test_check_quantity_datatype(self):
        self.assertEqual(
            QuantityDatatype().check_quantity_datatype(), QuantityDatatype())
        self.assertRaises(TypeError, String('x').check_quantity_datatype)

    def test_check_quantity_template(self):
        self.assertEqual(
            QuantityTemplate(Variable('x')).check_quantity_template(),
            QuantityTemplate(Variable('x')))
        self.assertRaises(
            TypeError, TimeTemplate(Variable('x')).check_quantity_template)

    def test_check_quantity_variable(self):
        self.assertEqual(
            QuantityVariable('x').check_quantity_variable(),
            QuantityVariable('x'))
        self.assertRaises(
            TypeError, TimeVariable('x').check_quantity_variable)

    def test_check_rank(self):
        self.assertEqual(Preferred.check_rank(), Preferred)
        self.assertRaises(TypeError, String('x').check_rank)

    def test_check_reference_record(self):
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertEqual(refr.check_reference_record(), refr)
        self.assertRaises(TypeError, String('x').check_reference_record)

    def test_check_reference_record_set(self):
        refs = ReferenceRecordSet(ReferenceRecord(NoValueSnak(Property('p'))))
        self.assertEqual(refs.check_reference_record_set(), refs)
        self.assertRaises(TypeError, SnakSet().check_reference_record_set)

    def test_check_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.check_snak(), snak)
        self.assertRaises(TypeError, String('x').check_snak)

    def test_check_snak_template(self):
        self.assertEqual(
            NoValueSnakTemplate(Variable('x')).check_snak_template(),
            NoValueSnakTemplate(Variable('x')))
        self.assertRaises(
            TypeError,
            IRI_Template(Variable('x')).check_snak_template)

    def test_check_snak_variable(self):
        self.assertEqual(
            SnakVariable('x').check_snak_variable(),
            SnakVariable('x'))
        self.assertEqual(
            NoValueSnakVariable('x').check_snak_variable(),
            NoValueSnakVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_snak_variable)

    def test_check_snak_set(self):
        snak_set = SnakSet(ValueSnak(Property('x'), Item('y')))
        self.assertEqual(snak_set.check_snak_set(), snak_set)
        self.assertRaises(TypeError, String('x').check_snak_set)

    def test_check_shallow_data_value(self):
        self.assertEqual(
            ExternalId('').check_shallow_data_value(), ExternalId(''))
        self.assertRaises(TypeError, Item('x').check_shallow_data_value)

    def test_check_shallow_data_value_template(self):
        self.assertEqual(
            StringTemplate(
                Variable('x')).check_shallow_data_value_template(),
            StringTemplate(Variable('x')))
        self.assertRaises(
            TypeError, ItemTemplate(
                Variable('x')).check_shallow_data_value_template)

    def test_check_shallow_data_value_variable(self):
        self.assertEqual(
            ShallowDataValueVariable(
                'x').check_shallow_data_value_variable(),
            ShallowDataValueVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_shallow_data_value_variable)

    def test_check_some_value_snak(self):
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.check_some_value_snak(), snak)
        self.assertRaises(TypeError, Item('x').check_some_value_snak)

    def test_check_some_value_snak_template(self):
        self.assertEqual(
            SomeValueSnakTemplate(
                Variable('x')).check_some_value_snak_template(),
            SomeValueSnakTemplate(Variable('x')))
        self.assertRaises(
            TypeError,
            NoValueSnakTemplate(
                Variable('x')).check_some_value_snak_template)

    def test_check_some_value_snak_variable(self):
        self.assertEqual(
            SomeValueSnakVariable('x').check_some_value_snak_variable(),
            SomeValueSnakVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_some_value_snak_variable)

    def test_check_statement(self):
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(stmt.check_statement(), stmt)
        self.assertRaises(TypeError, String('x').check_statement)

    def test_check_statement_template(self):
        self.assertEqual(
            StatementTemplate(
                *Variables('x', 'y')).check_statement_template(),
            StatementTemplate(*Variables('x', 'y')))
        self.assertRaises(
            TypeError, ValueSnakTemplate(
                *Variables('x', 'y')).check_statement_template)

    def test_check_statement_variable(self):
        self.assertEqual(
            StatementVariable('x').check_statement_variable(),
            StatementVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_statement_variable)

    def test_check_string(self):
        self.assertEqual(String('x').check_string(), String('x'))
        self.assertEqual(ExternalId('x').check_string(), ExternalId('x'))
        self.assertRaises(TypeError, Item('x').check_string)

    def test_check_string_template(self):
        self.assertEqual(
            StringTemplate(Variable('x')).check_string_template(),
            StringTemplate(Variable('x')))
        self.assertEqual(
            ExternalIdTemplate(Variable('x')).check_string_template(),
            ExternalIdTemplate(Variable('x')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).check_string_template)

    def test_check_string_variable(self):
        self.assertEqual(
            StringVariable('x').check_string_variable(),
            StringVariable('x'))
        self.assertEqual(
            ExternalIdVariable('x').check_string_variable(),
            ExternalIdVariable('x'))
        self.assertRaises(TypeError, ItemVariable('x').check_string_variable)

    def test_check_string_datatype(self):
        self.assertEqual(
            StringDatatype().check_string_datatype(), StringDatatype())
        self.assertRaises(TypeError, ItemDatatype().check_string_datatype)

    def test_check_template(self):
        self.assertEqual(
            StringTemplate(Variable('x')).check_template(),
            StringTemplate(Variable('x')))
        self.assertRaises(TypeError, String('abc').check_template)
        self.assertRaises(TypeError, String('abc').check_string_template)

    def test_check_text(self):
        self.assertEqual(Text('abc').check_text(), Text('abc'))
        self.assertEqual(String('abc').check_text(), Text('abc'))

    def test_check_text_datatype(self):
        self.assertEqual(TextDatatype().check_text_datatype(), TextDatatype())
        self.assertRaises(TypeError, StringDatatype().check_text_datatype)

    def test_check_text_set(self):
        texts = TextSet(Text('abc'), Text('def'))
        self.assertEqual(texts.check_text_set(), texts)
        self.assertRaises(TypeError, Text('abc').check_text_set)

    def test_check_text_template(self):
        self.assertEqual(
            TextTemplate(Variable('x')).check_text_template(),
            TextTemplate(Variable('x')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).check_text_template)

    def test_check_text_variable(self):
        self.assertEqual(
            TextVariable('x').check_text_variable(), TextVariable('x'))
        self.assertRaises(TypeError, ItemVariable('x').check_text_variable)

    def test_check_time(self):
        self.assertEqual(Time('2023-09-18').check_time(), Time('2023-09-18'))
        self.assertEqual(String('2023-09-18').check_time(), Time('2023-09-18'))

    def test_check_time_datatype(self):
        self.assertEqual(
            TimeDatatype().check_time_datatype(), TimeDatatype())
        self.assertRaises(TypeError, ItemDatatype().check_time_datatype)

    def test_check_time_template(self):
        self.assertEqual(
            TimeTemplate(Variable('x')).check_time_template(),
            TimeTemplate(Variable('x')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).check_time_template)

    def test_check_time_variable(self):
        self.assertEqual(
            TimeVariable('x').check_time_variable(), TimeVariable('x'))
        self.assertRaises(TypeError, ItemVariable('x').check_time_variable)

    def test_check_value(self):
        self.assertEqual(Item('x').check_value(), Item('x'))
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertRaises(TypeError, stmt.check_value)

    def test_check_value_template(self):
        self.assertEqual(
            ItemTemplate(Variable('x')).check_value_template(),
            ItemTemplate(Variable('x')))
        self.assertRaises(
            TypeError,
            NoValueSnakTemplate(Variable('x')).check_value_template)

    def test_check_value_variable(self):
        self.assertEqual(
            ValueVariable('x').check_value_variable(), ValueVariable('x'))
        self.assertEqual(
            ItemVariable('x').check_value_variable(), ItemVariable('x'))
        self.assertEqual(
            StringVariable('x').check_value_variable(), StringVariable('x'))
        self.assertRaises(TypeError, SnakVariable('x').check_value_variable)

    def test_check_value_set(self):
        values = ValueSet(Item('abc'), Text('def'))
        self.assertEqual(values.check_value_set(), values)
        self.assertRaises(TypeError, Item('abc').check_value_set)

    def test_check_value_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.check_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_value_snak)

    def test_check_value_snak_template(self):
        self.assertEqual(
            ValueSnakTemplate(
                *Variables('x', 'y')).check_value_snak_template(),
            ValueSnakTemplate(*Variables('x', 'y')))
        self.assertRaises(
            TypeError,
            SomeValueSnakTemplate(
                Variable('x')).check_value_snak_template)

    def test_check_value_snak_variable(self):
        self.assertEqual(
            ValueSnakVariable('x').check_value_snak_variable(),
            ValueSnakVariable('x'))
        self.assertRaises(
            TypeError, ItemVariable('x').check_value_snak_variable)

    def test_check_variable(self):
        self.assertEqual(Variable('x').check_variable(), Variable('x'))
        self.assertEqual(
            ItemVariable('x').check_variable(), ItemVariable('x'))
        self.assertRaises(TypeError, Item('x').check_variable)

# -- test_unpack_ ----------------------------------------------------------

    def test_unpack(self):
        self.assert_test_is_defined_for_kif_object_classes('unpack_')

    def test_unpack_annotation_record(self):
        quals = [ValueSnak(Property('p'), Item('y')),
                 NoValueSnak(Property('q'))]
        annot = AnnotationRecord(quals, [ReferenceRecord(*quals)], Normal)
        self.assertEqual(annot.unpack_annotation_record(), (
            SnakSet(*quals),
            ReferenceRecordSet(ReferenceRecord(*quals)),
            Normal))
        self.assertRaises(TypeError, Item('x').unpack_annotation_record)

    def test_unpack_annotation_record_set(self):
        quals = [ValueSnak(Property('p'), Item('y')),
                 NoValueSnak(Property('q'))]
        annot = AnnotationRecord(quals, [ReferenceRecord(*quals)], Normal)
        annots = AnnotationRecordSet(annot)
        self.assertEqual(
            annots.unpack_annotation_record_set(), (annot,))
        self.assertRaises(TypeError, Item('x').unpack_annotation_record_set)

    def test_unpack_data_value(self):
        self.assertEqual(IRI('x').unpack_data_value(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_data_value)

    def test_unpack_data_value_template(self):
        self.assertEqual(
            IRI_Template(Variable('x')).unpack_data_value_template(),
            (StringVariable('x'),))
        self.assertRaises(
            TypeError, ItemTemplate(
                Variable('x')).unpack_data_value_template)

    def test_unpack_data_value_variable(self):
        self.assertEqual(
            IRI_Variable('x').unpack_data_value_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_data_value_template)

    def test_unpack_datatype(self):
        self.assertEqual(IRI_Datatype().unpack_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_datatype)

    def test_unpack_datatype_variable(self):
        self.assertEqual(
            DatatypeVariable('x').unpack_datatype_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_datatype_variable)

    def test_unpack_deep_data_value(self):
        self.assertEqual(
            Quantity(0).unpack_deep_data_value(), (0, None, None, None))
        self.assertRaises(TypeError, String('x').unpack_deep_data_value)

    def test_unpack_deep_data_value_template(self):
        self.assertEqual(
            QuantityTemplate(Variable('x')).unpack_deep_data_value_template(),
            (QuantityVariable('x'), None, None, None))
        self.assertRaises(
            TypeError, ItemTemplate(
                Variable('x')).unpack_deep_data_value_template)

    def test_unpack_deep_data_value_variable(self):
        self.assertEqual(
            QuantityVariable('x').unpack_deep_data_value_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_deep_data_value_variable)

    def test_unpack_deprecated_rank(self):
        self.assertEqual(Deprecated.unpack_deprecated_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_deprecated_rank)

    def test_unpack_descriptor(self):
        desc = ItemDescriptor('abc', [Text('x'), Text('y')], 'z')
        self.assertEqual(desc.unpack_descriptor(), (
            Text('abc'), TextSet(Text('x'), Text('y')), Text('z')))
        self.assertRaises(TypeError, Item('x').unpack_descriptor)

    def test_unpack_entity(self):
        self.assertEqual(Item('x').unpack_entity(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_entity)

    def test_unpack_entity_fingerprint(self):
        fp = EntityFingerprint(Item('x'))
        self.assertEqual(fp.unpack_entity_fingerprint(), (Item('x'),))
        self.assertRaises(TypeError, String('x').unpack_entity_fingerprint)

    def test_unpack_entity_template(self):
        self.assertEqual(
            ItemTemplate(Variable('x')).unpack_entity_template(),
            (IRI_Variable('x'),))
        self.assertRaises(
            TypeError, StringTemplate(Variable('x')).unpack_entity_template)

    def test_unpack_entity_variable(self):
        self.assertEqual(ItemVariable('x').unpack_entity_variable(), ('x',))
        self.assertRaises(
            TypeError, StringVariable('x').unpack_entity_variable)

    def test_unpack_external_id(self):
        self.assertEqual(ExternalId('x').unpack_external_id(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_external_id)

    def test_unpack_external_id_datatype(self):
        self.assertEqual(
            ExternalIdDatatype().unpack_external_id_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_external_id_datatype)

    def test_unpack_external_id_template(self):
        self.assertEqual(
            ExternalIdTemplate(Variable('x')).unpack_external_id_template(),
            (StringVariable('x'),))
        self.assertRaises(
            TypeError,
            StringTemplate(Variable('x')).unpack_external_id_template)

    def test_unpack_external_id_variable(self):
        self.assertEqual(
            ExternalIdVariable('x').unpack_external_id_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_external_id_variable)

    def test_unpack_filter_pattern(self):
        pat = FilterPattern(
            Item('x'), Property('p'), String('y'), Snak.VALUE_SNAK)
        self.assertEqual(pat.unpack_filter_pattern(), (
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            Fingerprint(String('y')),
            Snak.Mask(1)))
        self.assertRaises(TypeError, Item('x').unpack_filter_pattern)

    def test_unpack_fingerprint(self):
        fp = EntityFingerprint(Item('x'))
        self.assertEqual(fp.unpack_fingerprint(), (Item('x'),))
        self.assertRaises(TypeError, String('x').unpack_fingerprint)

    def test_unpack_item(self):
        pass

    def test_unpack_item_datatype(self):
        self.assertEqual(ItemDatatype().unpack_item_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_item_datatype)

    def test_unpack_item_descriptor(self):
        desc = ItemDescriptor('x', [Text('y'), Text('z')], 'w')
        self.assertEqual(desc.unpack_item_descriptor(), (
            Text('x'), TextSet(Text('z'), Text('y')), Text('w')))
        self.assertRaises(TypeError, String('x').unpack_item_descriptor)

    def test_unpack_item_template(self):
        self.assertEqual(
            ItemTemplate(Variable('x')).unpack_item_template(),
            (IRI_Variable('x'),))
        self.assertRaises(
            TypeError, StringTemplate(Variable('x')).unpack_item_template)

    def test_unpack_item_variable(self):
        self.assertEqual(ItemVariable('x').unpack_item_variable(), ('x',))
        self.assertRaises(
            TypeError, StringVariable('x').unpack_item_variable)

    def test_unpack_iri(self):
        self.assertEqual(IRI('x').unpack_iri(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_iri)

    def test_unpack_iri_datatype(self):
        self.assertEqual(IRI_Datatype().unpack_iri_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_iri_datatype)

    def test_unpack_iri_template(self):
        self.assertEqual(
            IRI_Template(Variable('x')).unpack_iri_template(),
            (StringVariable('x'),))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).unpack_iri_template)

    def test_unpack_iri_variable(self):
        self.assertEqual(IRI_Variable('x').unpack_iri_variable(), ('x',))
        self.assertRaises(TypeError, ItemVariable('x').unpack_iri_variable)

    def test_unpack_kif_object(self):
        self.assertEqual(Item('x').unpack_kif_object(), (IRI('x'),))

    def test_unpack_kif_object_set(self):
        objs = KIF_ObjectSet(Item('x'), Property('y'))
        self.assertEqual(
            objs.unpack_kif_object_set(), (Item('x'), Property('y')))
        self.assertRaises(TypeError, Item('x').unpack_kif_object_set)

    def test_unpack_lexeme(self):
        pass

    def test_unpack_lexeme_datatype(self):
        self.assertEqual(LexemeDatatype().unpack_lexeme_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_lexeme_datatype)

    def test_unpack_lexeme_descriptor(self):
        desc = LexemeDescriptor('x', Item('y'), Item('z'))
        self.assertEqual(desc.unpack_lexeme_descriptor(), (
            Text('x'), Item('y'), Item('z')))
        self.assertRaises(TypeError, String('x').unpack_lexeme_descriptor)

    def test_unpack_lexeme_template(self):
        self.assertEqual(
            LexemeTemplate(Variable('x')).unpack_lexeme_template(),
            (IRI_Variable('x'),))
        self.assertRaises(
            TypeError,
            ItemTemplate(Variable('x')).unpack_lexeme_template)

    def test_unpack_lexeme_variable(self):
        self.assertEqual(
            LexemeVariable('x').unpack_lexeme_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_lexeme_variable)

    def test_unpack_no_value_snak(self):
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.unpack_no_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, Item('x').unpack_no_value_snak)

    def test_unpack_no_value_snak_template(self):
        self.assertEqual(
            NoValueSnakTemplate(
                Variable('x')).unpack_no_value_snak_template(),
            (PropertyVariable('x'),))
        self.assertRaises(
            TypeError, ItemTemplate(
                Variable('x')).unpack_no_value_snak_template)

    def test_unpack_no_value_snak_variable(self):
        self.assertEqual(
            NoValueSnakVariable('x').unpack_no_value_snak_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_no_value_snak_variable)

    def test_unpack_normal_rank(self):
        self.assertEqual(Normal.unpack_normal_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_normal_rank)

    def test_unpack_pattern(self):
        pass

    def test_unpack_plain_descriptor(self):
        desc = ItemDescriptor('x', [Text('y'), Text('z')], 'w')
        self.assertEqual(desc.unpack_plain_descriptor(), (
            Text('x'), TextSet(Text('z'), Text('y')), Text('w')))
        self.assertRaises(TypeError, String('x').unpack_plain_descriptor)

    def test_unpack_preferred_rank(self):
        self.assertEqual(Preferred.unpack_preferred_rank(), ())
        self.assertRaises(TypeError, Normal.unpack_preferred_rank)

    def test_unpack_property(self):
        self.assertEqual(Property('x').unpack_property(), (IRI('x'), None))
        self.assertEqual(
            Property('x', Item).unpack_property(),
            (IRI('x'), ItemDatatype()))
        self.assertRaises(TypeError, Item('x').unpack_property)

    def test_unpack_property_datatype(self):
        self.assertEqual(PropertyDatatype().unpack_property_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_property_datatype)

    def test_unpack_property_descriptor(self):
        desc = PropertyDescriptor('x', [Text('x'), Text('y')], 'z',
                                  ExternalIdDatatype())
        self.assertEqual(desc.unpack_property_descriptor(), (
            Text('x'), TextSet(Text('x'), Text('y')),
            Text('z'), ExternalIdDatatype()))
        self.assertRaises(TypeError, Item('x').unpack_property_descriptor)

    def test_unpack_property_fingerprint(self):
        fp = PropertyFingerprint(Property('x'))
        self.assertEqual(fp.unpack_property_fingerprint(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_property_fingerprint)

    def test_unpack_property_template(self):
        self.assertEqual(
            PropertyTemplate(Variable('x')).unpack_property_template(),
            (IRI_Variable('x'), None))
        self.assertEqual(
            PropertyTemplate(Variable('x'), String).unpack_property_template(),
            (IRI_Variable('x'), StringDatatype()))
        self.assertEqual(
            PropertyTemplate('x', Variable('y')).unpack_property_template(),
            (IRI('x'), DatatypeVariable('y')))
        self.assertEqual(
            PropertyTemplate(
                Variable('x'), Variable('y')).unpack_property_template(),
            (IRI_Variable('x'), DatatypeVariable('y')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).unpack_property_template)

    def test_unpack_property_variable(self):
        self.assertEqual(
            PropertyVariable('x').unpack_property_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_property_variable)

    def test_unpack_quantity(self):
        self.assertEqual(Quantity(0).unpack_quantity(),
                         (decimal.Decimal('0'), None, None, None))
        self.assertRaises(ValueError, String('x').unpack_quantity)

    def test_unpack_quantity_datatype(self):
        self.assertEqual(QuantityDatatype().unpack_quantity_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_quantity_datatype)

    def test_unpack_quantity_template(self):
        self.assertEqual(
            QuantityTemplate(Variable('x')).unpack_quantity_template(),
            (QuantityVariable('x'), None, None, None))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).unpack_quantity_template)

    def test_unpack_quantity_variable(self):
        self.assertEqual(
            QuantityVariable('x').unpack_quantity_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_quantity_variable)

    def test_unpack_rank(self):
        self.assertEqual(Preferred.unpack_rank(), ())
        self.assertRaises(TypeError, String('x').unpack_rank)

    def test_unpack_reference_record(self):
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertEqual(
            refr.unpack_reference_record(), (NoValueSnak(Property('p')),))
        self.assertRaises(TypeError, String('x').unpack_reference_record)

    def test_unpack_reference_record_set(self):
        ref1 = ReferenceRecord(NoValueSnak(Property('p')))
        ref2 = ReferenceRecord(ValueSnak(Property('p'), String('x')))
        refs = ReferenceRecordSet(ref1, ref2)
        self.assertEqual(
            refs.unpack_reference_record_set(), (ref1, ref2))
        self.assertRaises(TypeError, String('x').unpack_reference_record_set)

    def test_unpack_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.unpack_snak(), (Property('x'), Item('y')))
        self.assertRaises(TypeError, String('x').unpack_snak)

    def test_unpack_snak_set(self):
        snak1 = ValueSnak(Property('x'), Item('y'))
        snak2 = NoValueSnak(Property('p'))
        snaks = SnakSet(snak1, snak2)
        self.assertEqual(snaks.unpack_snak_set(), (snak2, snak1))
        self.assertRaises(TypeError, String('x').unpack_snak_set)

    def test_unpack_snak_template(self):
        snak = ValueSnakTemplate(Variable('x'), Variable('y'))
        self.assertEqual(
            snak.unpack_snak_template(),
            (PropertyVariable('x'), ValueVariable('y')))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).unpack_snak_template)

    def test_unpack_snak_variable(self):
        self.assertEqual(
            ValueSnakVariable('x').unpack_snak_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_snak_variable)

    def test_unpack_shallow_data_value(self):
        self.assertEqual(String('abc').unpack_shallow_data_value(), ('abc',))
        self.assertEqual(
            Text('abc').unpack_shallow_data_value(), ('abc', 'en'))
        self.assertRaises(TypeError, Quantity(0).unpack_shallow_data_value)

    def test_unpack_shallow_data_value_template(self):
        self.assertEqual(
            StringTemplate(
                StringVariable('x')).unpack_shallow_data_value_template(),
            (StringVariable('x'),))
        self.assertRaises(TypeError, QuantityTemplate(
            QuantityVariable('x')).unpack_shallow_data_value_template)

    def test_unpack_shallow_data_value_variable(self):
        self.assertEqual(
            StringVariable('x').unpack_shallow_data_value_variable(), ('x',))
        self.assertRaises(
            TypeError,
            QuantityVariable('x').unpack_shallow_data_value_variable)

    def test_unpack_some_value_snak(self):
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.unpack_some_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, Item('x').unpack_some_value_snak)

    def test_unpack_some_value_snak_template(self):
        self.assertEqual(
            SomeValueSnakTemplate(
                Variable('x')).unpack_some_value_snak_template(),
            (PropertyVariable('x'),))
        self.assertRaises(
            TypeError, String('x').unpack_some_value_snak_template)

    def test_unpack_some_value_snak_variable(self):
        self.assertEqual(
            SomeValueSnakVariable('x').unpack_some_value_snak_variable(),
            ('x',))
        self.assertRaises(
            TypeError, StringVariable('x').unpack_some_value_snak_variable)

    def test_unpack_statement(self):
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(
            stmt.unpack_statement(),
            (Item('x'), NoValueSnak(Property('y'))))
        self.assertRaises(TypeError, String('x').unpack_statement)

    def test_unpack_statement_template(self):
        self.assertEqual(
            StatementTemplate(
                Variable('x'), Variable('y')).unpack_statement_template(),
            (EntityVariable('x'), SnakVariable('y')))
        self.assertRaises(TypeError, String('x').unpack_statement_template)

    def test_unpack_statement_variable(self):
        self.assertEqual(
            StatementVariable('x').unpack_statement_variable(), ('x',))
        self.assertRaises(
            TypeError, StringVariable('x').unpack_statement_variable)

    def test_unpack_string(self):
        self.assertEqual(String('x').unpack_string(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_string)

    def test_unpack_string_template(self):
        self.assertEqual(
            StringTemplate(Variable('x')).unpack_string_template(),
            (StringVariable('x'),))
        self.assertEqual(
            ExternalIdTemplate(Variable('x')).unpack_string_template(),
            (StringVariable('x'),))
        self.assertRaises(
            TypeError, ItemTemplate(Variable('x')).unpack_string_template)

    def test_unpack_string_variable(self):
        self.assertEqual(
            StringVariable('x').unpack_string_variable(), ('x',))
        self.assertEqual(
            ExternalIdVariable('x').unpack_string_variable(), ('x',))
        self.assertRaises(
            TypeError, ItemVariable('x').unpack_string_variable)

    def test_unpack_string_datatype(self):
        self.assertEqual(StringDatatype().unpack_string_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_string_datatype)

    def test_unpack_template(self):
        self.assertEqual(
            TextTemplate(Variable('x')).unpack_template(),
            (StringVariable('x'), 'en'))
        self.assertRaises(TypeError, Time('2023-09-18').unpack_template)

    def test_unpack_text(self):
        self.assertEqual(Text('abc', 'pt').unpack_text(), ('abc', 'pt'))
        self.assertRaises(TypeError, Time('2023-09-18').unpack_text)

    def test_unpack_text_datatype(self):
        self.assertEqual(TextDatatype().unpack_text_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_text_datatype)

    def test_unpack_text_set(self):
        text1 = Text('abc')
        text2 = Text('def')
        texts = TextSet('abc', 'def')
        self.assertEqual(texts.unpack_text_set(), (text1, text2))
        self.assertRaises(TypeError, Time('2023-09-18').unpack_text_set)

    def test_unpack_text_template(self):
        self.assertEqual(
            TextTemplate(Variable('x')).unpack_text_template(),
            (StringVariable('x'), 'en'))
        self.assertRaises(
            TypeError, StringTemplate(Variable('x')).unpack_text_template)

    def test_unpack_text_variable(self):
        self.assertEqual(TextVariable('x').unpack_text_variable(), ('x',))
        self.assertRaises(
            TypeError, StringVariable('x').unpack_text_variable)

    def test_unpack_time(self):
        self.assertEqual(
            Time('2023-09-18').unpack_time(),
            (datetime.datetime(
                2023, 9, 18, tzinfo=datetime.timezone.utc), None, None, None))

    def test_unpack_time_datatype(self):
        self.assertEqual(TimeDatatype().unpack_time_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_time_datatype)

    def test_unpack_time_template(self):
        self.assertEqual(
            TimeTemplate(Variable('x')).unpack_time_template(),
            (TimeVariable('x'), None, None, None))
        self.assertRaises(
            TypeError, StringTemplate(Variable('x')).unpack_time_template)

    def test_unpack_time_variable(self):
        self.assertEqual(TimeVariable('x').unpack_time_variable(), ('x',))
        self.assertRaises(
            TypeError, StringVariable('x').unpack_time_variable)

    def test_unpack_value(self):
        self.assertEqual(Item('x').unpack_value(), (IRI('x'),))
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertRaises(TypeError, stmt.unpack_value)

    def test_unpack_value_set(self):
        value1 = String('abc')
        value2 = Quantity(33)
        values = ValueSet('abc', 33)
        self.assertEqual(values.unpack_value_set(), (value2, value1))
        self.assertRaises(TypeError, Time('2023-09-18').unpack_value_set)

    def test_unpack_value_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.unpack_value_snak(), (Property('x'), Item('y')))
        self.assertRaises(TypeError, String('x').unpack_value_snak)

    def test_unpack_value_snak_template(self):
        self.assertEqual(
            ValueSnak(
                Variable('x'), Variable('y')).unpack_value_snak_template(),
            (PropertyVariable('x'), ValueVariable('y')))
        self.assertRaises(TypeError, String('x').unpack_value_snak_template)

    def test_unpack_value_snak_variable(self):
        self.assertEqual(
            ValueSnakVariable('x').unpack_value_snak_variable(), ('x',))
        self.assertRaises(
            TypeError, StringVariable('x').unpack_value_snak_variable)

    def test_unpack_value_template(self):
        self.assertEqual(
            ItemTemplate(Variable('x')).unpack_value_template(),
            (IRI_Variable('x'),))
        self.assertRaises(
            TypeError, NoValueSnakTemplate(
                Variable('x')).unpack_value_template)

    def test_unpack_value_variable(self):
        self.assertEqual(ItemVariable('x').unpack_value_variable(), ('x',))
        self.assertRaises(
            TypeError, NoValueSnakVariable('x').unpack_value_variable)

    def test_unpack_variable(self):
        self.assertEqual(ItemVariable('x').unpack_variable(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_variable)

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
