# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re

from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    Deprecated,
    EncoderError,
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
)
from kif_lib.model import Datetime, Decimal, UTC

from .tests import kif_TestCase


class TestModelKIF_Object(kif_TestCase):

    ALL_KIF_OBJECT_CLASSES = set(filter(
        lambda c: isinstance(c, type) and issubclass(c, KIF_Object), map(
            lambda s: getattr(KIF_Object, s),
            filter(lambda s: re.match('^_[A-Z]', s), dir(KIF_Object)))))

    def test__init__(self):
        self.assertRaises(TypeError, KIF_Object)

    def test_kif_object_pyi(self):
        def get_decl(path):
            with open(path) as fp:
                return set(re.findall(r'def\b\s*([a-zA-Z]\w*)', fp.read()))
        defined = {x for x in dir(KIF_Object) if re.match(r'[a-z]', x[0])}
        defined -= {'count', 'index'}
        declared = get_decl('kif_lib/model/object.py')
        declared_pyi = get_decl('kif_lib/model/kif_object.pyi')
        self.assertEqual(defined - declared, declared_pyi)

    # -- IPython -----------------------------------------------------------

    def test__repr_markdown_(self):
        self.assertEqual(
            Item('x')._repr_markdown_(),
            '(**Item** [x](http://x))')

    # -- Argument checking -------------------------------------------------

    # -- datetime --

    def test__check_arg_datetime(self):
        self.assertRaises(TypeError, KIF_Object._check_arg_datetime, 0)
        self.assertRaises(ValueError, KIF_Object._check_arg_datetime, 'xyz')
        dt = Datetime(2024, 2, 5, 0, 0, tzinfo=UTC)
        self.assertEqual(KIF_Object._check_arg_datetime('2024-02-05'), dt)
        self.assertEqual(KIF_Object._check_arg_datetime('+2024-02-05'), dt)
        self.assertEqual(KIF_Object._check_arg_datetime('-2024-02-05'), dt)
        self.assertEqual(
            KIF_Object._check_arg_datetime(Datetime(2024, 2, 5)), dt)

    def test__check_optional_arg_datetime(self):
        self.assertRaises(
            TypeError, KIF_Object._check_optional_arg_datetime, 0)
        self.assertIsNone(KIF_Object._check_optional_arg_datetime(None))
        dt = Datetime(2024, 2, 5, 0, 0, tzinfo=UTC)
        self.assertEqual(
            KIF_Object._check_optional_arg_datetime(None, dt), dt)
        self.assertEqual(
            KIF_Object._check_optional_arg_datetime('2024-02-05', None), dt)

    def test__preprocess_arg_datetime(self):
        self.assertRaises(
            TypeError, KIF_Object._preprocess_arg_datetime, 0, 1)
        self.assertRaises(
            ValueError, KIF_Object._preprocess_arg_datetime, 'xyz', 1)
        dt = Datetime(2024, 2, 5, 0, 0, tzinfo=UTC)
        self.assertEqual(
            KIF_Object._preprocess_arg_datetime('2024-02-05', 1), dt)
        self.assertEqual(
            KIF_Object._check_arg_datetime('+2024-02-05', 1), dt)
        self.assertEqual(
            KIF_Object._check_arg_datetime('-2024-02-05', 1), dt)

    def test__preprocess_optional_arg_datetime(self):
        self.assertRaises(
            TypeError, KIF_Object._preprocess_optional_arg_datetime, 0, 1)
        self.assertIsNone(
            KIF_Object._preprocess_optional_arg_datetime(None, 1))
        dt = Datetime(2024, 2, 5, 0, 0, tzinfo=UTC)
        self.assertEqual(
            KIF_Object._preprocess_optional_arg_datetime(None, 1, dt), dt)
        self.assertEqual(
            KIF_Object._preprocess_optional_arg_datetime(
                '2024-02-05', 1, None), dt)

    # -- decimal --

    def test__check_arg_decimal(self):
        self.assertRaises(TypeError, KIF_Object._check_arg_decimal, dict())
        self.assertRaises(ValueError, KIF_Object._check_arg_decimal, '1.a')
        self.assertEqual(
            KIF_Object._check_arg_decimal('5.81'), Decimal('5.81'))
        self.assertEqual(
            KIF_Object._check_arg_decimal(5.81), Decimal(5.81))
        self.assertEqual(
            KIF_Object._check_arg_decimal(5), Decimal(5))

    def test__check_optional_arg_decimal(self):
        self.assertRaises(
            TypeError, KIF_Object._check_optional_arg_decimal, dict())
        self.assertRaises(
            ValueError, KIF_Object._check_optional_arg_decimal, '1.a')
        self.assertIsNone(KIF_Object._check_optional_arg_decimal(None))
        self.assertEqual(
            KIF_Object._check_optional_arg_decimal('5.81'),
            Decimal('5.81'))
        self.assertEqual(
            KIF_Object._check_optional_arg_decimal(None, 5.81),
            Decimal(5.81))

    def test__preprocess_arg_decimal(self):
        self.assertRaises(
            TypeError, KIF_Object._preprocess_arg_decimal, dict(), 1)
        self.assertRaises(
            ValueError, KIF_Object._preprocess_arg_decimal, '1.a', 1)
        self.assertEqual(
            KIF_Object._preprocess_arg_decimal('5.81', 1), Decimal('5.81'))
        self.assertEqual(
            KIF_Object._preprocess_arg_decimal(5.81, 1), Decimal(5.81))
        self.assertEqual(
            KIF_Object._preprocess_arg_decimal(5, 1), Decimal(5))

    def test__preprocess_optional_arg_decimal(self):
        self.assertRaises(
            TypeError, KIF_Object._preprocess_optional_arg_decimal, dict(), 1)
        self.assertRaises(
            ValueError, KIF_Object._preprocess_optional_arg_decimal, '1.a', 1)
        self.assertIsNone(KIF_Object._preprocess_optional_arg_decimal(None, 1))
        self.assertEqual(
            KIF_Object._preprocess_optional_arg_decimal('5.81', 1),
            Decimal('5.81'))
        self.assertEqual(
            KIF_Object._preprocess_optional_arg_decimal(None, 1, 5.81),
            Decimal(5.81))

    # -- Auto-defined stuff ------------------------------------------------

    def assert_test_is_defined_for_all_object_classes(self, prefix):
        tests = set(filter(
            lambda s: s.startswith('test_' + prefix), dir(self)))
        meths = set(map(
            lambda c: 'test_' + prefix + c._snake_case_name,
            self.ALL_KIF_OBJECT_CLASSES))
        self.assertEqual(meths, tests)

    # -- test_is_ --

    def test_is(self):
        self.assert_test_is_defined_for_all_object_classes('is_')

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
        self.assertTrue(ItemDatatype().is_datatype())
        self.assertTrue(IRI_Datatype().test_datatype())
        self.assertFalse(Item('x').is_datatype())
        self.assertFalse(Item('x').test_datatype())

    def test_is_data_value(self):
        self.assertTrue(IRI('x').is_data_value())
        self.assertTrue(IRI('x').test_data_value())
        self.assertFalse(Item('x').is_data_value())
        self.assertFalse(Item('x').test_data_value())

    def test_is_deep_data_value(self):
        self.assertTrue(Quantity(0).is_deep_data_value())
        self.assertTrue(Quantity(0).test_deep_data_value())
        self.assertFalse(String('x').is_deep_data_value())
        self.assertFalse(String('x').test_deep_data_value())

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

    def test_is_item(self):
        self.assertTrue(Item('x').is_item())
        self.assertTrue(Item('x').test_item())
        self.assertFalse(String('x').is_item())
        self.assertFalse(String('x').test_item())

    def test_is_item_descriptor(self):
        self.assertTrue(ItemDescriptor().is_item_descriptor())
        self.assertTrue(ItemDescriptor().test_item_descriptor())
        self.assertFalse(Item('x').is_item_descriptor())
        self.assertFalse(PropertyDescriptor().test_item_descriptor())

    def test_is_item_datatype(self):
        self.assertTrue(ItemDatatype().is_item_datatype())
        self.assertTrue(ItemDatatype().test_item_datatype())
        self.assertFalse(PropertyDatatype().is_item_datatype())
        self.assertFalse(Item('x').test_item_datatype())

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

    def test_is_no_value_snak(self):
        snak = NoValueSnak(Property('x'))
        self.assertTrue(snak.is_no_value_snak())
        self.assertTrue(snak.test_no_value_snak())
        self.assertFalse(String('x').is_no_value_snak())
        self.assertFalse(String('x').test_no_value_snak())

    def test_is_normal_rank(self):
        self.assertTrue(Normal.is_normal_rank())
        self.assertTrue(Normal.test_normal_rank())
        self.assertFalse(Preferred.is_normal_rank())
        self.assertFalse(Preferred.test_normal_rank())

    def test_is_pattern(self):
        self.assertTrue(FilterPattern().is_pattern())
        self.assertTrue(FilterPattern().test_pattern())
        self.assertFalse(String('x').is_pattern())
        self.assertFalse(String('x').test_pattern())

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

    def test_is_some_value_snak(self):
        snak = SomeValueSnak(Property('x'))
        self.assertTrue(snak.is_some_value_snak())
        self.assertTrue(snak.test_some_value_snak())
        self.assertFalse(String('x').is_some_value_snak())
        self.assertFalse(String('x').test_some_value_snak())

    def test_is_statement(self):
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertTrue(stmt.is_statement())
        self.assertTrue(stmt.test_statement())
        self.assertFalse(String('x').is_statement())
        self.assertFalse(String('x').test_statement())

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

    def test_is_value(self):
        self.assertTrue(Item('x').is_value())
        self.assertTrue(Item('x').test_value())

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

    # -- test_check_ --

    def test_check(self):
        self.assert_test_is_defined_for_all_object_classes('check_')

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

    def test_check_datatype(self):
        self.assertEqual(IRI_Datatype().check_datatype(), IRI_Datatype())
        self.assertRaises(TypeError, Item('x').check_datatype)

    def test_check_deep_data_value(self):
        self.assertEqual(Quantity(0).check_deep_data_value(), Quantity(0))
        self.assertRaises(TypeError, String('x').check_deep_data_value)

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

    def test_check_external_id(self):
        self.assertEqual(
            ExternalId('x').check_external_id(), ExternalId('x'))
        self.assertRaises(TypeError, String('x').check_external_id)

    def test_check_external_id_datatype(self):
        self.assertEqual(
            ExternalIdDatatype().check_external_id_datatype(),
            ExternalIdDatatype())
        self.assertRaises(
            TypeError, ItemDatatype().check_external_id_datatype)

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

    def test_check_item(self):
        self.assertEqual(Item('x').check_item(), Item('x'))
        self.assertRaises(TypeError, String('x').check_item)

    def test_check_item_datatype(self):
        self.assertEqual(ItemDatatype().check_item_datatype(), ItemDatatype())
        self.assertRaises(TypeError, String('x').check_item_datatype)

    def test_check_item_descriptor(self):
        self.assertEqual(
            ItemDescriptor().check_item_descriptor(), ItemDescriptor())
        self.assertRaises(
            TypeError, PropertyDescriptor().check_item_descriptor)

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

    def test_check_no_value_snak(self):
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.check_no_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_no_value_snak)

    def test_check_normal_rank(self):
        self.assertEqual(Normal.check_normal_rank(), Normal)
        self.assertRaises(TypeError, Preferred.check_normal_rank)

    def test_check_pattern(self):
        self.assertEqual(FilterPattern().check_pattern(), FilterPattern())
        self.assertRaises(TypeError, Item('x').check_filter_pattern)

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

    def test_check_quantity(self):
        self.assertEqual(Quantity(0).check_quantity(), Quantity(0))
        self.assertRaises(TypeError, String('x').check_quantity)

    def test_check_quantity_datatype(self):
        self.assertEqual(
            QuantityDatatype().check_quantity_datatype(), QuantityDatatype())
        self.assertRaises(TypeError, String('x').check_quantity_datatype)

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

    def test_check_snak_set(self):
        snak_set = SnakSet(ValueSnak(Property('x'), Item('y')))
        self.assertEqual(snak_set.check_snak_set(), snak_set)
        self.assertRaises(TypeError, String('x').check_snak_set)

    def test_check_shallow_data_value(self):
        self.assertEqual(
            ExternalId('').check_shallow_data_value(), ExternalId(''))
        self.assertRaises(TypeError, Item('x').check_shallow_data_value)

    def test_check_some_value_snak(self):
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.check_some_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_some_value_snak)

    def test_check_statement(self):
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(stmt.check_statement(), stmt)
        self.assertRaises(TypeError, String('x').check_statement)

    def test_check_string(self):
        self.assertEqual(String('x').check_string(), String('x'))
        self.assertEqual(ExternalId('x').check_string(), ExternalId('x'))
        self.assertRaises(TypeError, Item('x').check_string)

    def test_check_string_datatype(self):
        self.assertEqual(
            StringDatatype().check_string_datatype(), StringDatatype())
        self.assertRaises(TypeError, ItemDatatype().check_string_datatype)

    def test_check_text(self):
        self.assertEqual(Text('abc').check_text(), Text('abc'))
        self.assertRaises(TypeError, String('abc').check_text)

    def test_check_text_datatype(self):
        self.assertEqual(TextDatatype().check_text_datatype(), TextDatatype())
        self.assertRaises(TypeError, StringDatatype().check_text_datatype)

    def test_check_text_set(self):
        texts = TextSet(Text('abc'), Text('def'))
        self.assertEqual(texts.check_text_set(), texts)
        self.assertRaises(TypeError, Text('abc').check_text_set)

    def test_check_time(self):
        self.assertEqual(Time('2023-09-18').check_time(), Time('2023-09-18'))
        self.assertRaises(TypeError, String('2023-09-18').check_time)

    def test_check_time_datatype(self):
        self.assertEqual(
            TimeDatatype().check_time_datatype(), TimeDatatype())
        self.assertRaises(TypeError, ItemDatatype().check_time_datatype)

    def test_check_value(self):
        self.assertEqual(Item('x').check_value(), Item('x'))
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertRaises(TypeError, stmt.check_value)

    def test_check_value_set(self):
        values = ValueSet(Item('abc'), Text('def'))
        self.assertEqual(values.check_value_set(), values)
        self.assertRaises(TypeError, Item('abc').check_value_set)

    def test_check_value_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.check_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_value_snak)

    # -- test_unpack_ --

    def test_unpack(self):
        self.assert_test_is_defined_for_all_object_classes('unpack_')

    def test_unpack_annotation_record(self):
        quals = [ValueSnak(Property('p'), Item('y')),
                 NoValueSnak(Property('q'))]
        annot = AnnotationRecord(quals, [SnakSet(*quals)], Normal)
        self.assertEqual(annot.unpack_annotation_record(), (
            SnakSet(*quals),
            ReferenceRecordSet(SnakSet(*quals)),
            Normal))
        self.assertRaises(TypeError, Item('x').unpack_annotation_record)

    def test_unpack_annotation_record_set(self):
        quals = [ValueSnak(Property('p'), Item('y')),
                 NoValueSnak(Property('q'))]
        annot = AnnotationRecord(quals, [SnakSet(*quals)], Normal)
        annots = AnnotationRecordSet(annot)
        self.assertEqual(
            annots.unpack_annotation_record_set(), (annot,))
        self.assertRaises(TypeError, Item('x').unpack_annotation_record_set)

    def test_unpack_data_value(self):
        self.assertEqual(IRI('x').unpack_data_value(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_data_value)

    def test_unpack_datatype(self):
        self.assertEqual(IRI_Datatype().unpack_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_datatype)

    def test_unpack_deep_data_value(self):
        self.assertEqual(
            Quantity(0).unpack_deep_data_value(), (0, None, None, None))
        self.assertRaises(TypeError, String('x').unpack_deep_data_value)

    def test_unpack_deprecated_rank(self):
        self.assertEqual(Deprecated.unpack_deprecated_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_deprecated_rank)

    def test_unpack_descriptor(self):
        desc = ItemDescriptor('abc', ['x', 'y'], 'z')
        self.assertEqual(desc.unpack_descriptor(), (
            Text('abc'), TextSet('x', 'y'), Text('z')))
        self.assertRaises(TypeError, Item('x').unpack_descriptor)

    def test_unpack_entity(self):
        self.assertEqual(Item('x').unpack_entity(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_entity)

    def test_unpack_entity_fingerprint(self):
        fp = EntityFingerprint(Item('x'))
        self.assertEqual(fp.unpack_entity_fingerprint(), (Item('x'),))
        self.assertRaises(TypeError, String('x').unpack_entity_fingerprint)

    def test_unpack_external_id(self):
        self.assertEqual(ExternalId('x').unpack_external_id(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_external_id)

    def test_unpack_external_id_datatype(self):
        self.assertEqual(
            ExternalIdDatatype().unpack_external_id_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_external_id_datatype)

    def test_unpack_filter_pattern(self):
        pat = FilterPattern(
            Item('x'), Property('p'), String('y'), Snak.VALUE_SNAK)
        self.assertEqual(pat.unpack_filter_pattern(), (
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            Fingerprint(String('y')),
            1))
        self.assertRaises(TypeError, Item('x').unpack_filter_pattern)

    def test_unpack_fingerprint(self):
        fp = EntityFingerprint(Item('x'))
        self.assertEqual(fp.unpack_fingerprint(), (Item('x'),))
        self.assertRaises(TypeError, String('x').unpack_fingerprint)

    def test_unpack_item(self):
        self.assertEqual(Item('x').unpack_item(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_item)

    def test_unpack_item_datatype(self):
        self.assertEqual(ItemDatatype().unpack_item_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_item_datatype)

    def test_unpack_item_descriptor(self):
        desc = ItemDescriptor('x', ['y', 'z'], 'w')
        self.assertEqual(desc.unpack_item_descriptor(), (
            Text('x'), TextSet('z', 'y'), Text('w')))
        self.assertRaises(TypeError, String('x').unpack_item_descriptor)

    def test_unpack_iri(self):
        self.assertEqual(IRI('x').unpack_iri(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_iri)

    def test_unpack_iri_datatype(self):
        self.assertEqual(IRI_Datatype().unpack_iri_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_iri_datatype)

    def test_unpack_kif_object(self):
        self.assertEqual(Item('x').unpack_kif_object(), (IRI('x'),))

    def test_unpack_kif_object_set(self):
        objs = KIF_ObjectSet(Item('x'), Property('y'))
        self.assertEqual(
            objs.unpack_kif_object_set(), (Item('x'), Property('y')))
        self.assertRaises(TypeError, Item('x').unpack_kif_object_set)

    def test_unpack_lexeme(self):
        self.assertEqual(Lexeme('x').unpack_lexeme(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_lexeme)

    def test_unpack_lexeme_datatype(self):
        self.assertEqual(LexemeDatatype().unpack_lexeme_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_lexeme_datatype)

    def test_unpack_lexeme_descriptor(self):
        desc = LexemeDescriptor('x', Item('y'), Item('z'))
        self.assertEqual(desc.unpack_lexeme_descriptor(), (
            Text('x'), Item('y'), Item('z')))
        self.assertRaises(TypeError, String('x').unpack_lexeme_descriptor)

    def test_unpack_no_value_snak(self):
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.unpack_no_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_no_value_snak)

    def test_unpack_normal_rank(self):
        self.assertEqual(Normal.unpack_normal_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_normal_rank)

    def test_unpack_pattern(self):
        pat = FilterPattern(
            Item('x'), Property('p'), Item('y'), Snak.VALUE_SNAK)
        self.assertEqual(pat.unpack_pattern(), (
            EntityFingerprint(Item('x')),
            PropertyFingerprint(Property('p')),
            Fingerprint(Item('y')),
            1))
        self.assertRaises(TypeError, Item('x').unpack_pattern)

    def test_unpack_plain_descriptor(self):
        desc = ItemDescriptor('x', ['y', 'z'], 'w')
        self.assertEqual(desc.unpack_plain_descriptor(), (
            Text('x'), TextSet('z', 'y'), Text('w')))
        self.assertRaises(TypeError, String('x').unpack_plain_descriptor)

    def test_unpack_preferred_rank(self):
        self.assertEqual(Preferred.unpack_preferred_rank(), ())
        self.assertRaises(TypeError, Normal.unpack_preferred_rank)

    def test_unpack_property(self):
        self.assertEqual(Property('x').unpack_property(), (IRI('x'),))
        self.assertRaises(TypeError, Item('x').unpack_property)

    def test_unpack_property_datatype(self):
        self.assertEqual(PropertyDatatype().unpack_property_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_property_datatype)

    def test_unpack_property_descriptor(self):
        desc = PropertyDescriptor('x', ['x', 'y'], 'z', ExternalIdDatatype())
        self.assertEqual(desc.unpack_property_descriptor(), (
            Text('x'), TextSet('x', 'y'), Text('z'), ExternalIdDatatype()))
        self.assertRaises(TypeError, Item('x').unpack_property_descriptor)

    def test_unpack_property_fingerprint(self):
        fp = PropertyFingerprint(Property('x'))
        self.assertEqual(fp.unpack_property_fingerprint(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_property_fingerprint)

    def test_unpack_quantity(self):
        self.assertEqual(Quantity(0).unpack_quantity(),
                         (Decimal('0'), None, None, None))
        self.assertRaises(TypeError, String('x').unpack_quantity)

    def test_unpack_quantity_datatype(self):
        self.assertEqual(QuantityDatatype().unpack_quantity_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_quantity_datatype)

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

    def test_unpack_shallow_data_value(self):
        self.assertEqual(String('abc').unpack_shallow_data_value(), ('abc',))
        self.assertEqual(
            Text('abc').unpack_shallow_data_value(), ('abc', 'en'))
        self.assertRaises(TypeError, Quantity(0).unpack_shallow_data_value)

    def test_unpack_some_value_snak(self):
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.unpack_some_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_some_value_snak)

    def test_unpack_statement(self):
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(
            stmt.unpack_statement(),
            (Item('x'), NoValueSnak(Property('y'))))
        self.assertRaises(TypeError, String('x').unpack_statement)

    def test_unpack_string(self):
        self.assertEqual(String('x').unpack_string(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_string)

    def test_unpack_string_datatype(self):
        self.assertEqual(StringDatatype().unpack_string_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_string_datatype)

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

    def test_unpack_time(self):
        self.assertEqual(
            Time('2023-09-18').unpack_time(),
            (Datetime(2023, 9, 18, tzinfo=UTC), None, None, None))
        self.assertRaises(TypeError, String('2023-09-18').unpack_time)

    def test_unpack_time_datatype(self):
        self.assertEqual(TimeDatatype().unpack_time_datatype(), ())
        self.assertRaises(TypeError, Item('x').unpack_time_datatype)

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

    # -- Codecs ------------------------------------------------------------

    def test_json_encoder_extensions(self):
        from kif_lib.model.kif_object import KIF_JSON_Encoder
        enc = KIF_JSON_Encoder()
        self.assertEqual(
            enc.encode(IRI('x')), '{"class": "IRI", "args": ["x"]}')
        self.assertEqual(
            enc.encode(Datetime(2024, 2, 6)), '"2024-02-06 00:00:00"')
        self.assertEqual(enc.encode(Decimal(0)), '"0"')
        self.assertEqual(enc.encode(Decimal(3.5)), '"3.5"')
        self.assertEqual(enc.encode(Snak.ALL), '"7"')
        self.assertRaises(EncoderError, enc.encode, set())

    def test_sexp_encoder_extensions(self):
        from kif_lib.model.kif_object import KIF_SExpEncoder
        enc = KIF_SExpEncoder()
        self.assertEqual(enc.encode(Preferred), 'PreferredRank')
        self.assertEqual(
            enc.encode(Datetime(2024, 2, 6)), '2024-02-06 00:00:00')
        self.assertEqual(enc.encode(Decimal(0)), '0')
        self.assertEqual(enc.encode(Decimal(3.5)), '3.5')
        self.assertEqual(enc.encode(Snak.ALL), '7')
        self.assertRaises(EncoderError, enc.encode, set())


if __name__ == '__main__':
    TestModelKIF_Object.main()
