# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re

from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    Deprecated,
    EntityFingerprint,
    ExternalId,
    FilterPattern,
    IRI,
    Item,
    ItemDescriptor,
    KIF_Object,
    KIF_ObjectSet,
    Lexeme,
    LexemeDescriptor,
    Normal,
    NoValueSnak,
    Preferred,
    Property,
    PropertyDescriptor,
    PropertyFingerprint,
    Quantity,
    ReferenceRecord,
    ReferenceRecordSet,
    SnakSet,
    SomeValueSnak,
    Statement,
    String,
    Text,
    TextSet,
    Time,
    ValueSnak,
)
from kif_lib.model import Datetime, Decimal, UTC

from .tests import kif_TestCase, main


class TestModelKIF_Object(kif_TestCase):

    ALL_KIF_OBJECT_CLASSES = set(filter(
        lambda c: isinstance(c, type) and issubclass(c, KIF_Object), map(
            lambda s: getattr(KIF_Object, s),
            filter(lambda s: re.match('^[A-Z]', s), dir(KIF_Object)))))

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
        self.assertTrue(Item.datatype.is_datatype())
        self.assertTrue(IRI.datatype.test_datatype())
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
        self.assertTrue(ExternalId.datatype.is_external_id_datatype())
        self.assertTrue(ExternalId.datatype.test_external_id_datatype())
        self.assertFalse(Item.datatype.is_external_id_datatype())
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
        self.assertTrue(IRI.datatype.is_iri_datatype())
        self.assertTrue(IRI.datatype.test_iri_datatype())
        self.assertFalse(Property.datatype.is_iri_datatype())
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
        self.assertTrue(Item.datatype.is_item_datatype())
        self.assertTrue(Item.datatype.test_item_datatype())
        self.assertFalse(Property.datatype.is_item_datatype())
        self.assertFalse(Item('x').test_item_datatype())

    def test_is_lexeme(self):
        self.assertTrue(Lexeme('x').is_lexeme())
        self.assertTrue(Lexeme('x').test_lexeme())
        self.assertFalse(String('x').is_lexeme())
        self.assertFalse(String('x').test_lexeme())

    def test_is_lexeme_datatype(self):
        self.assertTrue(Lexeme.datatype.is_lexeme_datatype())
        self.assertTrue(Lexeme.datatype.test_lexeme_datatype())
        self.assertFalse(String('x').datatype.is_lexeme_datatype())
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
        self.assertTrue(Property.datatype.is_property_datatype())
        self.assertTrue(Property.datatype.test_property_datatype())
        self.assertFalse(Item.datatype.is_property_datatype())
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
        self.assertTrue(Quantity.datatype.is_quantity_datatype())
        self.assertTrue(Quantity.datatype.test_quantity_datatype())
        self.assertFalse(Item.datatype.is_quantity_datatype())
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
        self.assertTrue(String.datatype.is_string_datatype())
        self.assertTrue(String.datatype.test_string_datatype())
        self.assertTrue(ExternalId.datatype.test_string_datatype())
        self.assertFalse(Property.datatype.is_string_datatype())
        self.assertFalse(Item('x').test_string_datatype())

    def test_is_text(self):
        self.assertTrue(Text('').is_text())
        self.assertTrue(Text('abc', 'pt').test_text())
        self.assertFalse(String('x').is_quantity())
        self.assertFalse(String('x').test_quantity())

    def test_is_text_datatype(self):
        self.assertTrue(Text.datatype.is_text_datatype())
        self.assertTrue(Text.datatype.test_text_datatype())
        self.assertFalse(Property.datatype.is_text_datatype())
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
        self.assertTrue(Time.datatype.is_time_datatype())
        self.assertTrue(Time.datatype.test_time_datatype())
        self.assertFalse(Property.datatype.is_time_datatype())
        self.assertFalse(Item('x').test_time_datatype())

    def test_is_value(self):
        self.assertTrue(Item('x').is_value())
        self.assertTrue(Item('x').test_value())

    def test_is_value_snak(self):
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertTrue(snak.is_value_snak())
        self.assertTrue(snak.test_value_snak())
        self.assertFalse(String('x').is_value_snak())
        self.assertFalse(String('x').test_value_snak())

    # -- test_check_ --

    def test_check(self):
        # check_kif_object
        self.assertEqual(Item('x').check_kif_object(), Item('x'))
        # check_value
        self.assertEqual(Item('x').check_value(), Item('x'))
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertRaises(TypeError, stmt.check_value)
        # check_entity
        self.assertEqual(Item('x').check_entity(), Item('x'))
        self.assertRaises(TypeError, String('x').check_entity)
        # check_item
        self.assertEqual(Item('x').check_item(), Item('x'))
        self.assertRaises(TypeError, String('x').check_item)
        # check_property
        self.assertEqual(Property('x').check_property(), Property('x'))
        self.assertRaises(TypeError, Item('x').check_property)
        # check_data_value
        self.assertEqual(IRI('x').check_data_value(), IRI('x'))
        self.assertRaises(TypeError, Item('x').check_data_value)
        # check_string
        self.assertEqual(String('x').check_string(), String('x'))
        self.assertRaises(TypeError, Item('x').check_string)
        # check_iri
        self.assertEqual(IRI('x').check_iri(), IRI('x'))
        self.assertRaises(TypeError, Item('x').check_iri)
        # check_deep_data_value
        self.assertEqual(Quantity(0).check_deep_data_value(), Quantity(0))
        self.assertRaises(TypeError, String('x').check_deep_data_value)
        # check_quantity
        self.assertEqual(Quantity(0).check_quantity(), Quantity(0))
        self.assertRaises(TypeError, String('x').check_quantity)
        # check_time
        self.assertEqual(Time('2023-09-18').check_time(), Time('2023-09-18'))
        self.assertRaises(TypeError, String('2023-09-18').check_time)
        # check_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.check_snak(), snak)
        self.assertRaises(TypeError, String('x').check_snak)
        # check_value_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.check_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_value_snak)
        # check_some_value_snak
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.check_some_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_some_value_snak)
        # check_no_value_snak
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.check_no_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_no_value_snak)
        # check_reference_record
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertEqual(refr.check_reference_record(), refr)
        self.assertRaises(TypeError, String('x').check_reference_record)
        # check_rank
        self.assertEqual(Preferred.check_rank(), Preferred)
        self.assertRaises(TypeError, String('x').check_rank)
        # check_preferred_rank
        self.assertEqual(Preferred.check_preferred_rank(), Preferred)
        self.assertRaises(TypeError, Normal.check_preferred_rank)
        # check_normal_rank
        self.assertEqual(Normal.check_normal_rank(), Normal)
        self.assertRaises(TypeError, Preferred.check_normal_rank)
        # check_deprecated_rank
        self.assertEqual(Deprecated.check_deprecated_rank(), Deprecated)
        self.assertRaises(TypeError, Preferred.check_deprecated_rank)
        # check_statement
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(stmt.check_statement(), stmt)
        self.assertRaises(TypeError, String('x').check_statement)

    def test_unpack(self):
        # unpack_kif_object
        self.assertEqual(Item('x').unpack_kif_object(), (IRI('x'),))
        # unpack_value
        self.assertEqual(Item('x').unpack_value(), (IRI('x'),))
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertRaises(TypeError, stmt.unpack_value)
        # unpack_entity
        self.assertEqual(Item('x').unpack_entity(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_entity)
        # unpack_item
        self.assertEqual(Item('x').unpack_item(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_item)
        # unpack_property
        self.assertEqual(Property('x').unpack_property(), (IRI('x'),))
        self.assertRaises(TypeError, Item('x').unpack_property)
        # unpack_data_value
        self.assertEqual(IRI('x').unpack_data_value(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_data_value)
        # unpack_string
        self.assertEqual(String('x').unpack_string(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_string)
        # unpack_iri
        self.assertEqual(IRI('x').unpack_iri(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_iri)
        # unpack_deep_data_value
        self.assertEqual(
            Quantity(0).unpack_deep_data_value(), (0, None, None, None))
        self.assertRaises(TypeError, String('x').unpack_deep_data_value)
        # unpack_quantity
        self.assertEqual(Quantity(0).unpack_quantity(),
                         (Decimal('0'), None, None, None))
        self.assertRaises(TypeError, String('x').unpack_quantity)
        # unpack_time
        self.assertEqual(
            Time('2023-09-18').unpack_time(),
            (Datetime(2023, 9, 18, tzinfo=UTC), None, None, None))
        self.assertRaises(TypeError, String('2023-09-18').unpack_time)
        # unpack_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.unpack_snak(), (Property('x'), Item('y')))
        self.assertRaises(TypeError, String('x').unpack_snak)
        # unpack_value_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.unpack_value_snak(), (Property('x'), Item('y')))
        self.assertRaises(TypeError, String('x').unpack_value_snak)
        # unpack_some_value_snak
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.unpack_some_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_some_value_snak)
        # unpack_no_value_snak
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.unpack_no_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_no_value_snak)
        # unpack_reference_record
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertEqual(
            refr.unpack_reference_record(), (NoValueSnak(Property('p')),))
        self.assertRaises(TypeError, String('x').unpack_reference_record)
        # unpack_rank
        self.assertEqual(Preferred.unpack_rank(), ())
        self.assertRaises(TypeError, String('x').unpack_rank)
        # unpack_preferred_rank
        self.assertEqual(Preferred.unpack_preferred_rank(), ())
        self.assertRaises(TypeError, Normal.unpack_preferred_rank)
        # unpack_normal_rank
        self.assertEqual(Normal.unpack_normal_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_normal_rank)
        # unpack_deprecated_rank
        self.assertEqual(Deprecated.unpack_deprecated_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_deprecated_rank)
        # unpack_statement
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(
            stmt.unpack_statement(),
            (Item('x'), NoValueSnak(Property('y'))))
        self.assertRaises(TypeError, String('x').unpack_statement)


if __name__ == '__main__':
    main()
