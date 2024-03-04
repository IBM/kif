# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools
import os
import re
import unittest

from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    Datatype,
    DataValue,
    DeepDataValue,
    DeprecatedRank,
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
    Items,
    KIF_Object,
    KIF_ObjectSet,
    Lexeme,
    LexemeDatatype,
    LexemeDescriptor,
    Lexemes,
    NormalRank,
    NoValueSnak,
    Pattern,
    PreferredRank,
    Properties,
    Property,
    PropertyDatatype,
    PropertyDescriptor,
    PropertyFingerprint,
    Quantity,
    QuantityDatatype,
    Rank,
    ReferenceRecord,
    ReferenceRecordSet,
    ShallowDataValue,
    Snak,
    SnakSet,
    SomeValueSnak,
    Statement,
    Store,
    String,
    StringDatatype,
    Text,
    TextDatatype,
    TextSet,
    Time,
    TimeDatatype,
    Value,
    ValueSet,
    ValueSnak,
)
from kif_lib.error import ShouldNotGetHere
from kif_lib.model import Decimal, UTC
from kif_lib.model.object import Object
from kif_lib.namespace import WIKIBASE, XSD
from kif_lib.typing import override
from kif_lib.vocabulary import wd


class kif_TestCase(unittest.TestCase):

    @classmethod
    def main(cls):
        return unittest.main()

    def assert_raises_bad_argument(
            self, exception, position, name, details, function,
            *args, **kwargs):
        regex = re.escape(str(KIF_Object._arg_error(
            details, function, name, position, exception)))
        self.assertRaisesRegex(
            exception, regex, function, *args, **kwargs)

    def assert_kif_object(self, obj):
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(obj, Object)
        self.assertTrue(obj.is_object())
        self.assertIsInstance(obj, KIF_Object)
        self.assertTrue(obj.is_kif_object())

    def assert_kif_object_set(self, obj, *args):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, KIF_ObjectSet)
        self.assertTrue(obj.is_kif_object_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, KIF_Object)
            self.assertEqual(arg, args[i])
        self.assertEqual(obj.frozenset, set(args))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for arg in args:
            self.assertIn(arg, obj)

    def assert_datatype(self, obj):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Datatype)
        self.assertTrue(obj.is_datatype())

    def assert_value(self, obj):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Value)
        self.assertTrue(obj.is_value())

    def assert_value_set(self, obj, *values):
        self.assert_kif_object_set(obj, *values)
        self.assertIsInstance(obj, ValueSet)
        self.assertTrue(obj.is_value_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, Value)
            self.assertEqual(arg, values[i])
        self.assertEqual(obj.frozenset, set(values))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for value in values:
            self.assertIn(value, obj)

    def assert_entity(self, obj, iri):
        self.assert_value(obj)
        self.assertIsInstance(obj, Entity)
        self.assertTrue(obj.is_entity())
        self.assertIsInstance(obj.args[0], IRI)
        self.assertTrue(obj.args[0].is_iri())
        self.assertEqual(obj.args[0], iri)
        self.assertIs(obj.iri, obj.args[0])
        self.assertIs(obj.get_iri(), obj.args[0])
        self.assertEqual(obj.value, obj.iri.value)
        self.assertEqual(obj.get_value(), obj.iri.get_value())
        self.assertEqual(obj.n3(), obj.iri.n3())

    def assert_item(self, obj, iri):
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Item)
        self.assertTrue(obj.is_item())
        self.assertEqual(obj.mask, Value.ITEM)
        self.assertEqual(obj.get_mask(), Value.ITEM)
        self.assert_item_datatype(Datatype.from_value_class(type(obj)))

    def assert_item_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, ItemDatatype)
        self.assertTrue(obj.is_item_datatype())
        self.assertEqual(obj._uri, WIKIBASE.WikibaseItem)

    def assert_property(self, obj, iri):
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Property)
        self.assertTrue(obj.is_property())
        self.assertEqual(obj.mask, Value.PROPERTY)
        self.assertEqual(obj.get_mask(), Value.PROPERTY)
        self.assert_property_datatype(Datatype.from_value_class(type(obj)))

    def assert_property_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, PropertyDatatype)
        self.assertTrue(obj.is_property_datatype())
        self.assertEqual(obj._uri, WIKIBASE.WikibaseProperty)

    def assert_lexeme(self, obj, iri):
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Lexeme)
        self.assertTrue(obj.is_lexeme())
        self.assertEqual(obj.mask, Value.LEXEME)
        self.assertEqual(obj.get_mask(), Value.LEXEME)
        self.assert_lexeme_datatype(Datatype.from_value_class(type(obj)))

    def assert_lexeme_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, LexemeDatatype)
        self.assertTrue(obj.is_lexeme_datatype())
        self.assertEqual(obj._uri, WIKIBASE.WikibaseLexeme)

    def assert_data_value(self, obj):
        self.assert_value(obj)
        self.assertIsInstance(obj, DataValue)
        self.assertTrue(obj.is_data_value())

    def assert_shallow_data_value(self, obj):
        self.assert_data_value(obj)
        self.assertIsInstance(obj, ShallowDataValue)
        self.assertTrue(obj.is_shallow_data_value())
        self.assertIs(obj.content, obj.args[0])
        self.assertIs(obj.get_content(), obj.args[0])

    def assert_iri(self, obj, iri):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, IRI)
        self.assertTrue(obj.is_iri())
        self.assertEqual(obj.mask, Value.IRI)
        self.assertEqual(obj.get_mask(), Value.IRI)
        self.assert_iri_datatype(Datatype.from_value_class(type(obj)))
        self.assertEqual(obj.args[0], iri)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'<{obj.value}>')

    def assert_iri_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, IRI_Datatype)
        self.assertTrue(obj.is_iri_datatype())
        self.assertEqual(obj._uri, WIKIBASE.Url)

    def assert_text(self, obj, s, lang=None):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, Text)
        self.assertTrue(obj.is_text())
        self.assertEqual(obj.mask, Value.TEXT)
        self.assertEqual(obj.get_mask(), Value.TEXT)
        self.assert_text_datatype(Datatype.from_value_class(type(obj)))
        self.assertEqual(obj.args[0], s)
        if lang is None:
            lang = Text.default_language
        self.assertEqual(obj.args[1], lang)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'"{obj.value}"@{lang}')

    def assert_text_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, TextDatatype)
        self.assertTrue(obj.is_text_datatype())
        self.assertEqual(obj._uri, WIKIBASE.Monolingualtext)

    def assert_text_set(self, obj, *texts):
        self.assert_value_set(obj, *texts)
        self.assertIsInstance(obj, TextSet)
        self.assertTrue(obj.is_text_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, Text)
            self.assertEqual(arg, texts[i])
        self.assertEqual(obj.frozenset, set(texts))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for text in texts:
            self.assertIn(text, obj)

    def assert_string(self, obj, s):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assertTrue(obj.is_string())
        self.assertEqual(obj.mask, Value.STRING)
        self.assertEqual(obj.get_mask(), Value.STRING)
        self.assert_string_datatype(Datatype.from_value_class(type(obj)))
        self.assertEqual(obj.args[0], s)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'"{obj.value}"')

    def assert_string_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, StringDatatype)
        self.assertTrue(obj.is_string_datatype())
        self.assertEqual(obj._uri, WIKIBASE.String)

    def assert_external_id(self, obj, s):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assertIsInstance(obj, ExternalId)
        self.assertEqual(obj.mask, Value.EXTERNAL_ID)
        self.assertEqual(obj.get_mask(), Value.EXTERNAL_ID)
        self.assertTrue(obj.is_external_id())
        self.assert_external_id_datatype(Datatype.from_value_class(type(obj)))
        self.assertEqual(obj.args[0], s)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'"{obj.value}"')

    def assert_external_id_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, ExternalIdDatatype)
        self.assertTrue(obj.is_external_id_datatype())
        self.assertEqual(obj._uri, WIKIBASE.ExternalId)

    def assert_deep_data_value(self, obj):
        self.assert_data_value(obj)
        self.assertIsInstance(obj, DeepDataValue)
        self.assertTrue(obj.is_deep_data_value())

    def assert_quantity(self, obj, amount, unit=None, lb=None, ub=None):
        self.assert_deep_data_value(obj)
        self.assertIsInstance(obj, Quantity)
        self.assertTrue(obj.is_quantity())
        self.assertEqual(obj.mask, Value.QUANTITY)
        self.assertEqual(obj.get_mask(), Value.QUANTITY)
        self.assert_quantity_datatype(Datatype.from_value_class(type(obj)))
        self.assertEqual(obj.args[0], Decimal(amount))
        self.assertEqual(obj.value, str(obj.args[0]))
        self.assertEqual(obj.get_value(), str(obj.args[0]))
        self.assertEqual(obj.n3(), f'"{obj.value}"^^<{XSD.decimal}>')
        self.assertEqual(obj.amount, obj.args[0])
        self.assertEqual(obj.get_amount(), obj.args[0])
        self.assertEqual(obj.args[1], unit)
        self.assertEqual(obj.unit, obj.args[1])
        self.assertEqual(obj.get_unit(), obj.args[1])
        self.assertEqual(
            obj.args[2], Decimal(lb) if lb is not None else None)
        self.assertEqual(obj.lower_bound, obj.args[2])
        self.assertEqual(obj.get_lower_bound(), obj.args[2])
        self.assertEqual(
            obj.args[3], Decimal(ub) if ub is not None else None)
        self.assertEqual(obj.upper_bound, obj.args[3])
        self.assertEqual(obj.get_upper_bound(), obj.args[3])

    def assert_quantity_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, QuantityDatatype)
        self.assertTrue(obj.is_quantity_datatype())
        self.assertEqual(obj._uri, WIKIBASE.Quantity)

    def assert_time(self, obj, time, prec=None, tz=None, cal=None):
        self.assert_deep_data_value(obj)
        self.assertIsInstance(obj, Time)
        self.assertTrue(obj.is_time())
        self.assertEqual(obj.mask, Value.TIME)
        self.assertEqual(obj.get_mask(), Value.TIME)
        self.assert_time_datatype(Datatype.from_value_class(type(obj)))
        self.assertEqual(obj.args[0], time.replace(tzinfo=UTC))
        self.assertEqual(obj.value, obj.args[0].isoformat())
        self.assertEqual(obj.get_value(), obj.args[0].isoformat())
        self.assertEqual(obj.n3(), f'"{obj.value}"^^<{XSD.dateTime}>')
        self.assertEqual(obj.time, obj.args[0])
        self.assertEqual(obj.get_time(), obj.args[0])
        self.assertEqual(obj.args[1], prec)
        self.assertEqual(obj.precision, obj.args[1])
        self.assertEqual(obj.get_precision(), obj.args[1])
        self.assertEqual(
            obj.args[2], tz if tz is not None else None)
        self.assertEqual(obj.timezone, obj.args[2])
        self.assertEqual(obj.get_timezone(), obj.args[2])
        self.assertEqual(
            obj.args[3], cal if cal is not None else None)
        self.assertEqual(obj.calendar, obj.args[3])
        self.assertEqual(obj.get_calendar(), obj.args[3])

    def assert_time_datatype(self, obj):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, TimeDatatype)
        self.assertTrue(obj.is_time_datatype())
        self.assertEqual(obj._uri, WIKIBASE.Time)

    def assert_snak(self, obj, prop):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Snak)
        self.assertTrue(obj.is_snak())
        self.assertIsInstance(obj.property, Property)
        self.assertTrue(obj.property.is_property())
        self.assertEqual(obj.args[0], prop)
        self.assertEqual(obj.property, obj.args[0])
        self.assertEqual(obj.get_property(), obj.args[0])

    def assert_value_snak(self, obj, prop, value):
        self.assert_snak(obj, prop)
        self.assertIsInstance(obj, ValueSnak)
        self.assertTrue(obj.is_value_snak())
        self.assert_value(obj.args[1])
        self.assertEqual(obj.args[1], value)
        self.assertEqual(obj.value, obj.args[1])
        self.assertEqual(obj.get_value(), obj.args[1])
        self.assertEqual(obj.mask, Snak.VALUE_SNAK)
        self.assertEqual(obj.get_mask(), Snak.VALUE_SNAK)

    def assert_some_value_snak(self, obj, prop):
        self.assert_snak(obj, prop)
        self.assertIsInstance(obj, SomeValueSnak)
        self.assertTrue(obj.is_some_value_snak())
        self.assertEqual(obj.mask, Snak.SOME_VALUE_SNAK)
        self.assertEqual(obj.get_mask(), Snak.SOME_VALUE_SNAK)

    def assert_no_value_snak(self, obj, prop):
        self.assert_snak(obj, prop)
        self.assertIsInstance(obj, NoValueSnak)
        self.assertTrue(obj.is_no_value_snak())
        self.assertEqual(obj.mask, Snak.NO_VALUE_SNAK)
        self.assertEqual(obj.get_mask(), Snak.NO_VALUE_SNAK)

    def assert_snak_set(self, obj, *snaks):
        self.assert_kif_object_set(obj, *snaks)
        self.assertIsInstance(obj, SnakSet)
        self.assertTrue(obj.is_snak_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, Snak)
            self.assertEqual(arg, snaks[i])
        self.assertEqual(obj.frozenset, set(snaks))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for snak in snaks:
            self.assertIn(snak, obj)

    def assert_reference_record(self, obj, *snaks):
        self.assert_snak_set(obj, *snaks)
        self.assertIsInstance(obj, ReferenceRecord)
        self.assertTrue(obj.is_reference_record())

    def assert_reference_record_set(self, obj, *refs):
        self.assert_kif_object_set(obj, *refs)
        self.assertIsInstance(obj, ReferenceRecordSet)
        self.assertTrue(obj.is_reference_record_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, ReferenceRecord)
            self.assertEqual(arg, refs[i])
        self.assertEqual(obj.frozenset, set(refs))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for ref in refs:
            self.assertIn(ref, obj)

    def assert_rank(self, obj):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Rank)
        self.assertTrue(obj.is_rank())

    def assert_preferred_rank(self, obj):
        self.assert_rank(obj)
        self.assertIsInstance(obj, PreferredRank)
        self.assertTrue(obj.is_preferred_rank())

    def assert_normal_rank(self, obj):
        self.assert_rank(obj)
        self.assertIsInstance(obj, NormalRank)
        self.assertTrue(obj.is_normal_rank())

    def assert_deprecated_rank(self, obj):
        self.assert_rank(obj)
        self.assertIsInstance(obj, DeprecatedRank)
        self.assertTrue(obj.is_deprecated_rank())

    def assert_statement(self, obj, subject, snak):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Statement)
        self.assertTrue(obj.is_statement())
        self.assertIsInstance(obj.args[0], Entity)
        self.assertTrue(obj.args[0].is_entity())
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.subject, obj.args[0])
        self.assertEqual(obj.get_subject(), obj.args[0])
        self.assertIsInstance(obj.args[1], Snak)
        self.assertTrue(obj.args[1].is_snak())
        self.assertEqual(obj.args[1], snak)
        self.assertEqual(obj.snak, obj.args[1])
        self.assertEqual(obj.get_snak(), obj.args[1])

    def assert_annotation_record(self, obj, quals, refs, rank):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, AnnotationRecord)
        self.assertTrue(obj.is_annotation_record())
        self.assertIsInstance(obj.args[0], SnakSet)
        self.assertTrue(obj.args[0].is_snak_set())
        self.assertEqual(obj.args[0], quals)
        self.assertEqual(obj.qualifiers, obj.args[0])
        self.assertEqual(obj.get_qualifiers(), obj.args[0])
        self.assertIsInstance(obj.args[1], ReferenceRecordSet)
        self.assertTrue(obj.args[1].is_reference_record_set())
        self.assertEqual(obj.args[1], refs)
        self.assertEqual(obj.references, obj.args[1])
        self.assertEqual(obj.get_references(), obj.args[1])
        self.assertIsInstance(obj.args[2], Rank)
        self.assertTrue(obj.args[2].is_rank())
        self.assertEqual(obj.args[2], rank)
        self.assertEqual(obj.rank, obj.args[2])
        self.assertEqual(obj.get_rank(), obj.args[2])

    def assert_annotation_record_set(self, obj, *annots):
        self.assert_kif_object_set(obj, *annots)
        self.assertIsInstance(obj, AnnotationRecordSet)
        self.assertTrue(obj.is_annotation_record_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, AnnotationRecord)
            self.assertEqual(arg, annots[i])
        self.assertEqual(obj.frozenset, set(annots))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for ref in annots:
            self.assertIn(ref, obj)

    def assert_item_descriptor(self, obj, label, aliases, desc):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, ItemDescriptor)
        self.assertTrue(obj.is_descriptor())
        self.assertTrue(obj.is_item_descriptor())
        if label is None:
            self.assertIsNone(obj.args[0])
            self.assertIsNone(obj.label)
            self.assertIsNone(obj.get_label())
        else:
            self.assert_text(obj.args[0], *label)
            self.assert_text(obj.label, *label)
            self.assert_text(obj.get_label(), *label)
        self.assert_text_set(obj.args[1], *aliases)
        self.assert_text_set(obj.aliases, *aliases)
        self.assert_text_set(obj.get_aliases(), *aliases)
        if desc is None:
            self.assertIsNone(obj.args[2])
            self.assertIsNone(obj.description)
            self.assertIsNone(obj.get_description())
        else:
            self.assert_text(obj.args[2], *desc)
            self.assert_text(obj.description, *desc)
            self.assert_text(obj.get_description(), *desc)

    def assert_property_descriptor(self, obj, label, aliases, desc, dt):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, PropertyDescriptor)
        self.assertTrue(obj.is_descriptor())
        self.assertTrue(obj.is_plain_descriptor())
        self.assertTrue(obj.is_property_descriptor())
        if label is None:
            self.assertIsNone(obj.args[0])
            self.assertIsNone(obj.label)
            self.assertIsNone(obj.get_label())
        else:
            self.assert_text(obj.args[0], *label)
            self.assert_text(obj.label, *label)
            self.assert_text(obj.get_label(), *label)
        self.assert_text_set(obj.args[1], *aliases)
        self.assert_text_set(obj.aliases, *aliases)
        self.assert_text_set(obj.get_aliases(), *aliases)
        if desc is None:
            self.assertIsNone(obj.args[2])
            self.assertIsNone(obj.description)
            self.assertIsNone(obj.get_description())
        else:
            self.assert_text(obj.args[2], *desc)
            self.assert_text(obj.description, *desc)
            self.assert_text(obj.get_description(), *desc)
        if dt is None:
            self.assertIsNone(obj.args[3])
            self.assertIsNone(obj.datatype)
            self.assertIsNone(obj.get_datatype())
        else:
            self.assert_datatype(obj.args[3], *dt)
            self.assert_datatype(obj.datatype, *dt)
            self.assert_datatype(obj.get_datatype(), *dt)

    def assert_lexeme_descriptor(self, obj, lemma, cat, lang):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, LexemeDescriptor)
        self.assertTrue(obj.is_descriptor())
        self.assertFalse(obj.is_plain_descriptor())
        self.assertTrue(obj.is_lexeme_descriptor())
        if lemma is None:
            self.assertIsNone(obj.args[0])
            self.assertIsNone(obj.lemma)
            self.assertIsNone(obj.get_lemma())
        else:
            self.assert_text(obj.args[0], *lemma)
            self.assert_text(obj.lemma, *lemma)
            self.assert_text(obj.get_lemma(), *lemma)
        if cat is None:
            self.assertIsNone(obj.args[1])
            self.assertIsNone(obj.category)
            self.assertIsNone(obj.get_category())
        else:
            self.assert_item(obj.args[1], *cat)
            self.assert_item(obj.category, *cat)
            self.assert_item(obj.get_category(), *cat)
        if lang is None:
            self.assertIsNone(obj.args[2])
            self.assertIsNone(obj.language)
            self.assertIsNone(obj.get_language())
        else:
            self.assert_item(obj.args[2], *lang)
            self.assert_item(obj.language, *lang)
            self.assert_item(obj.get_language(), *lang)

    def assert_fingerprint(self, obj, val):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Fingerprint)
        self.assertTrue(obj.is_fingerprint())
        self.assertIsInstance(obj.args[0], (Value, SnakSet))
        self.assertEqual(obj.args[0], val)
        if isinstance(obj.args[0], Value):
            self.assertEqual(obj.value, obj.args[0])
            self.assertEqual(obj.value, val)
            self.assertIsNone(obj.snak_set)
        else:
            self.assertEqual(obj.snak_set, obj.args[0])
            self.assertEqual(obj.snak_set, val)
            self.assertIsNone(obj.value)

    def assert_entity_fingerprint(self, obj, val):
        self.assert_fingerprint(obj, val)
        self.assertIsInstance(obj, EntityFingerprint)
        self.assertTrue(obj.is_entity_fingerprint())

    def assert_property_fingerprint(self, obj, val):
        self.assert_fingerprint(obj, val)
        self.assertIsInstance(obj, PropertyFingerprint)
        self.assertTrue(obj.is_property_fingerprint())

    def assert_pattern(self, obj):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Pattern)
        self.assertTrue(obj.is_pattern())

    def assert_filter_pattern(
            self, obj, subject=None, property=None, value=None, mask=Snak.ALL):
        self.assert_pattern(obj)
        self.assertIsInstance(obj, FilterPattern)
        self.assertTrue(obj.is_filter_pattern())
        if subject is not None:
            subject = EntityFingerprint(subject)
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.subject, subject)
        self.assertEqual(obj.get_subject(), subject)
        if property is not None:
            property = PropertyFingerprint(property)
        self.assertEqual(obj.args[1], property)
        self.assertEqual(obj.property, property)
        self.assertEqual(obj.get_property(), property)
        if value is not None:
            value = Fingerprint(value)
        self.assertEqual(obj.args[2], value)
        self.assertEqual(obj.value, value)
        self.assertEqual(obj.get_value(), value)
        self.assertEqual(Snak.Mask(obj.args[3]), mask)
        self.assertEqual(obj.snak_mask, mask)


# == kif_StoreTestCase =====================================================

class kif_StoreTestCase(kif_TestCase):

    @classmethod
    def new_Store(cls, store_name, *args, **kwargs):
        return Store(store_name, *args, **kwargs)

    @classmethod
    def parse(cls, text):
        from kif_lib.namespace import PREFIXES
        pre = '\n'.join(
            map(lambda t: f'@prefix {t[0]}: <{t[1]}> .', PREFIXES.items()))
        return Store('rdf', format='ttl', data=pre + '\n\n' + text)

    def store_sanity_checks(self, kb):
        self.assert_raises_bad_argument(
            ValueError, 1, 'store_name', None, Store, 'xxx')
        # extra references
        self.store_test_extra_references(kb)
        # flags
        self.store_test_flags(kb)
        # page size
        self.store_test_page_size(kb)
        # timeout
        self.store_test_timeout(kb)
        # internal stuff
        self.store_test__error(kb)
        # contains
        self.store_test_contains_bad_argument(kb)
        # count
        self.store_test_count_bad_argument(kb)
        self.store_test_count_snak_bad_argument(kb)
        self.store_test_count_empty(kb)
        # filter
        self.store_test_filter_bad_argument(kb)
        self.store_test_filter_snak_bad_argument(kb)
        self.store_test_filter_empty(kb)
        # get_annotations
        self.store_test_get_annotations_bad_argument(kb)
        self.store_test_get_annotations_empty(kb)
        # TODO: get descriptor
        # self.store_test_get_descriptor_bad_argument(kb)
        # self.store_test_get_descriptor_empty(kb)

    def store_test_extra_references(self, kb, default=ReferenceRecordSet()):
        self.assertRaises(TypeError, kb.set_extra_references, 'abc')
        self.assertEqual(kb.extra_references, default)
        kb.extra_references = [
            ReferenceRecord(), ReferenceRecord(wd.stated_in(wd.PubChem))]
        self.assertEqual(
            kb.extra_references, ReferenceRecordSet(
                ReferenceRecord(), ReferenceRecord(wd.stated_in(wd.PubChem))))
        kb.extra_references = None
        self.assertEqual(kb.extra_references, default)

    def store_test_flags(self, kb):
        saved_flags = kb.flags
        kb.flags = Store.ALL
        # has flags
        self.assertTrue(kb.has_flags(Store.CACHE))
        self.assertTrue(kb.has_flags(Store.CACHE))
        self.assertTrue(kb.has_flags(Store.BEST_RANK))
        self.assertTrue(kb.has_flags(Store.CACHE | Store.BEST_RANK))
        self.assertTrue(kb.has_flags(Store.NO_VALUE_SNAK))
        self.assertTrue(kb.has_flags(Store.SOME_VALUE_SNAK))
        kb.flags = kb.flags & ~Store.CACHE
        self.assertFalse(kb.has_flags(Store.CACHE))
        self.assertTrue(kb.has_flags(Store.BEST_RANK))
        self.assertTrue(kb.has_flags(Store.NO_VALUE_SNAK))
        self.assertTrue(kb.has_flags(Store.SOME_VALUE_SNAK))
        # set flags
        kb.flags = Store.ALL & ~Store.CACHE
        self.assertFalse(kb.has_flags(Store.CACHE))
        self.assertTrue(kb.has_flags(Store.BEST_RANK))
        self.assertTrue(kb.has_flags(Store.NO_VALUE_SNAK))
        self.assertTrue(kb.has_flags(Store.SOME_VALUE_SNAK))
        kb.set_flags(Store.CACHE)
        self.assertEqual(kb.flags, Store.ALL)
        # unset_flags
        kb.flags = Store.ALL
        self.assertTrue(kb.has_flags(Store.CACHE))
        self.assertTrue(kb.has_flags(Store.BEST_RANK))
        self.assertTrue(kb.has_flags(Store.NO_VALUE_SNAK))
        self.assertTrue(kb.has_flags(Store.SOME_VALUE_SNAK))
        kb.unset_flags(Store.CACHE | Store.BEST_RANK)
        self.assertEqual(
            kb.flags, Store.ALL ^ (Store.CACHE | Store.BEST_RANK))
        kb.set_flags(Store.CACHE | Store.BEST_RANK)
        self.assertEqual(kb.flags, Store.ALL)
        kb.flags = saved_flags

    def store_test_page_size(self, kb, default=100):
        self.assert_raises_bad_argument(
            TypeError, 1, 'page_size', None, kb.set_page_size, 'abc')
        self.assertEqual(kb.page_size, default)
        kb.page_size = 10
        self.assertEqual(kb.page_size, 10)
        kb.page_size = None
        self.assertEqual(kb.page_size, default)

    def store_test_timeout(self, kb, default=None):
        self.assert_raises_bad_argument(
            TypeError, 1, 'timeout', None, kb.set_timeout, 'abc')
        self.assertEqual(kb.timeout, default)
        kb.timeout = 10
        self.assertEqual(kb.timeout, 10)
        kb.timeout = None
        self.assertIsNone(kb.timeout)

    def store_test__error(self, kb):
        err = Store._error('x')
        self.assertIsInstance(err, Store.Error)
        self.assertEqual(str(err), 'x')

    def store_test_contains_bad_argument(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'stmt', None, kb.contains, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, 'stmt', None, kb.contains, True)
        self.assert_raises_bad_argument(
            TypeError, 1, 'stmt', None, kb.contains, Item('x'))

    def store_test_contains(self, kb, stmt1, *stmts):
        self.assertNotIn(0, kb)
        self.assertNotIn(True, kb)
        self.assertNotIn(Item('x'), kb)
        values, some_values, no_values = [], [], []
        for stmt in itertools.chain([stmt1], stmts):
            self._store_test_contains1(kb, stmt)
            if stmt.snak.is_value_snak():
                values.append(stmt)
            elif stmt.snak.is_some_value_snak():
                some_values.append(stmt)
            elif stmt.snak.is_no_value_snak():
                no_values.append(stmt)
            else:
                raise ShouldNotGetHere
        saved_flags = kb.flags
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        kb.set_flags(kb.VALUE_SNAK)
        self._store_test_contains(kb, values)
        self._store_test_not_contains(kb, some_values)
        self._store_test_not_contains(kb, no_values)
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        kb.set_flags(kb.SOME_VALUE_SNAK)
        self._store_test_not_contains(kb, values)
        self._store_test_contains(kb, some_values)
        self._store_test_not_contains(kb, no_values)
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        kb.set_flags(kb.NO_VALUE_SNAK)
        self._store_test_not_contains(kb, values)
        self._store_test_not_contains(kb, some_values)
        self._store_test_contains(kb, no_values)
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        self._store_test_not_contains(kb, values)
        self._store_test_not_contains(kb, some_values)
        self._store_test_not_contains(kb, no_values)
        kb.flags = saved_flags

    def _store_test_contains(self, kb, stmts):
        for stmt in stmts:
            self._store_test_contains1(kb, stmt)

    def _store_test_contains1(self, kb, stmt):
        self.assertIn(stmt, kb)
        self.assertTrue(kb.contains(stmt))
        kb._cache.clear()
        self.assertTrue(kb.contains(stmt))
        kb._cache.clear()
        self.assertIn(stmt, kb)

    def store_test_not_contains(self, kb, stmt1, *stmts):
        self._store_test_not_contains(kb, itertools.chain([stmt1], stmts))

    def _store_test_not_contains(self, kb, stmts):
        for stmt in stmts:
            self._store_test_not_contains1(kb, stmt)

    def _store_test_not_contains1(self, kb, stmt):
        self.assertNotIn(stmt, kb)
        self.assertFalse(kb.contains(stmt))
        kb._cache.clear()
        self.assertFalse(kb.contains(stmt))
        kb._cache.clear()
        self.assertNotIn(stmt, kb)

    def store_test_count_bad_argument(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'subject', None, kb.count, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'property', None, kb.count, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'value', None, kb.count, None, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.count, None, None, None, 'abc')
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.count, None, None, Item('x'), NoValueSnak)
        self.assert_raises_bad_argument(
            TypeError, 5, 'pattern', None, kb.count, pattern=Item('x'))

    def store_test_count_snak_bad_argument(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'subject', None, kb.count_snak, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'snak', None, kb.count_snak, None, 0)

    def store_test_count_empty(self, kb):
        saved_flags = kb.flags
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        self.assertEqual(kb.count(), 0)
        kb.flags = saved_flags
        empty = FilterPattern(None, None, None, Snak.Mask(0))
        self.assertEqual(kb.count(pattern=empty), 0)

    def store_test_count(
            self, kb, n, subject=None, property=None, value=None,
            snak_mask=None, pattern=None):
        self.assertEqual(kb.count(
            subject, property, value, snak_mask, pattern), n)
        if (pattern is None
            and property is not None and value is not None
                and property.is_property() and value.is_value()):
            self.assertEqual(kb.count_snak(subject, property(value)), n)
            saved_flags = kb.flags
            kb.unset_flags(kb.VALUE_SNAK)
            self.assertEqual(kb.count_snak(subject, property(value)), 0)
            kb.flags = saved_flags
        elif (pattern is None
              and property is not None and property.is_property()
              and snak_mask == Snak.SOME_VALUE_SNAK):
            some_value = SomeValueSnak(property)
            self.assertEqual(kb.count_snak(subject, some_value), n)
            saved_flags = kb.flags
            kb.unset_flags(kb.SOME_VALUE_SNAK)
            self.assertEqual(kb.count_snak(subject, some_value), 0)
            kb.flags = saved_flags
        elif (pattern is None
              and property is not None and property.is_property()
              and snak_mask == Snak.NO_VALUE_SNAK):
            no_value = NoValueSnak(property)
            self.assertEqual(kb.count_snak(subject, no_value), n)
            saved_flags = kb.flags
            kb.unset_flags(kb.NO_VALUE_SNAK)
            self.assertEqual(kb.count_snak(subject, no_value), 0)
            kb.flags = saved_flags

    def store_test_filter_bad_argument(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'subject', None, kb.filter, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'property', None, kb.filter, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'value', None, kb.filter, None, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.filter, None, None, None, 'a')
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.filter, None, None, Item('x'), NoValueSnak)
        self.assert_raises_bad_argument(
            TypeError, 5, 'pattern', None, kb.filter, pattern=Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 6, 'limit', None, kb.filter, limit=Item('x'))

    def store_test_filter_snak_bad_argument(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'subject', None, kb.filter_snak, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'snak', None, kb.filter_snak, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'limit', None, kb.filter_snak, limit=Item('x'))

    def store_test_filter_empty(self, kb):
        saved_flags = kb.flags
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        self.assertFalse(bool(set(kb.filter())))
        kb.flags = saved_flags
        empty = FilterPattern(None, None, None, Snak.Mask(0))
        self.assertFalse(bool(set(kb.filter(pattern=empty))))
        self.assertFalse(bool(set(kb.filter(limit=0))))
        self.assertFalse(bool(set(kb.filter(limit=-1))))

    def store_test_filter(
            self, kb, stmts, subject=None, property=None, value=None,
            snak_mask=None, pattern=None, limit=None):
        res = set(kb.filter(
            subject, property, value, snak_mask, pattern, limit))
        self.assertEqual(set(stmts), res)
        res_annotated = set(kb.filter_annotated(
            subject, property, value, snak_mask, pattern, limit))
        for i, (stmt, annots) in enumerate(res_annotated):
            self.assertIn(stmt, set(stmts))
            self.assertIsInstance(annots, AnnotationRecordSet)
        for stmt in stmts:
            res_annotated_snak = list(kb.filter_snak_annotated(
                stmt.subject, stmt.snak))
            self.assertEqual(len(res_annotated_snak), 1)
            self.assertEqual(res_annotated_snak[0][0], stmt)
            self.assertIsInstance(
                res_annotated_snak[0][1], AnnotationRecordSet)
            break               # check only the first
        if (pattern is None
            and property is not None and value is not None
                and property.is_property() and value.is_value()):
            self.assertEqual(set(kb.filter_snak(
                subject, property(value))), res)
            saved_flags = kb.flags
            kb.unset_flags(kb.VALUE_SNAK)
            self.assertFalse(bool(set(kb.filter_snak(
                subject, property(value)))))
            kb.flags = saved_flags
        elif (pattern is None
              and property is not None and property.is_property()
              and snak_mask == Snak.SOME_VALUE_SNAK):
            some_value = SomeValueSnak(property)
            self.assertEqual(set(kb.filter_snak(subject, some_value)), res)
            saved_flags = kb.flags
            kb.unset_flags(kb.SOME_VALUE_SNAK)
            self.assertFalse(bool(set(kb.filter_snak(subject, some_value))))
            kb.flags = saved_flags
        elif (pattern is None
              and property is not None and property.is_property()
              and snak_mask == Snak.NO_VALUE_SNAK):
            no_value = NoValueSnak(property)
            self.assertEqual(set(kb.filter_snak(subject, no_value)), res)
            saved_flags = kb.flags
            kb.unset_flags(kb.NO_VALUE_SNAK)
            self.assertFalse(bool(set(kb.filter_snak(subject, no_value))))
            kb.flags = saved_flags

    def store_test_get_annotations_bad_argument(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'stmts', None, kb.get_annotations, 0)

    def store_test_get_annotations_empty(self, kb):
        self.assertRaises(StopIteration, next, kb.get_annotations([]))

    def store_test_get_annotations(self, kb, pairs, stmt, *stmts):
        # single entity
        got1 = list(kb.get_annotations(stmt))
        # print()
        # if got1[0][1] is not None:
        #     print(got1[0][1].to_markdown())
        # if pairs[0][1] is not None:
        #     print(pairs[0][1].to_markdown())
        self.assertEqual(got1[0][0], pairs[0][0])
        self.assertEqual(got1[0][1], pairs[0][1])
        # multiple entities
        gotn = list(kb.get_annotations(stmts))
        self.assertEqual(len(gotn), len(pairs[1:]))
        got = got1 + gotn
        values, some_values, no_values = [], [], []
        for i in range(len(got)):
            # print()
            # print(f'-- got {i} --')
            # print(got[i][1])
            # print(f'-- expected {i} --')
            # print(pairs[i][1])
            # print()
            self.assertEqual(got[i][0], pairs[i][0])
            self.assertEqual(got[i][1], pairs[i][1])
            stmt, annots = got[i]
            if stmt.snak.is_value_snak():
                values.append((i, got[i]))
            elif stmt.snak.is_some_value_snak():
                some_values.append((i, got[i]))
            elif stmt.snak.is_no_value_snak():
                no_values.append((i, got[i]))
            else:
                raise ShouldNotGetHere
        saved_flags = kb.flags
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        kb.set_flags(kb.VALUE_SNAK)
        for i, t in values:
            self.assertEqual(t, pairs[i])
        empty = list(itertools.chain(some_values, no_values))
        it = zip(map(lambda t: t[0], empty), kb.get_annotations(map(
            lambda t: t[1][0], empty)))
        for i, (stmt, annots) in it:
            self.assertEqual(stmt, pairs[i][0])
            self.assertIsNone(annots)
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        kb.set_flags(kb.SOME_VALUE_SNAK)
        for i, t in some_values:
            self.assertEqual(t, pairs[i])
        empty = list(itertools.chain(values, no_values))
        it = zip(map(lambda t: t[0], empty), kb.get_annotations(map(
            lambda t: t[1][0], empty)))
        for i, (stmt, annots) in it:
            self.assertEqual(stmt, pairs[i][0])
            self.assertIsNone(annots)
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        kb.set_flags(kb.NO_VALUE_SNAK)
        for i, t in no_values:
            self.assertEqual(t, pairs[i])
        empty = list(itertools.chain(values, some_values))
        it = zip(map(lambda t: t[0], empty), kb.get_annotations(map(
            lambda t: t[1][0], empty)))
        for i, (stmt, annots) in it:
            self.assertEqual(stmt, pairs[i][0])
            self.assertIsNone(annots)
        kb.flags = saved_flags

# -- Descriptors -----------------------------------------------------------

    def sanity_check_get_descriptor(self, kb):
        self.sanity_check_get_descriptor_bad_args(kb)
        self.sanity_check_get_descriptor_vacuous_calls(kb)
        it = kb.get_descriptor([Item('x'), Text('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_descriptor' "
            r'\(expected Entity, got Text\)', list, it)

    # -- get_descriptor --

    def sanity_check_get_descriptor_bad_args(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'entities', 'expected Entity or Iterable, got int',
            kb.get_descriptor, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'language', 'expected str, got int',
            kb.get_descriptor, Item('Q1'), 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'mask',
            'expected Descriptor.AttributeMask or int, got str',
            kb.get_descriptor, Item('Q1'), 'pt', 'abc')

    def sanity_check_get_descriptor_vacuous_calls(self, kb):
        items = list(Items('_Q0', '_Q1', '_Q2', '_Q0'))
        props = list(Properties('_P0', '_P1', '_P2', '_P0'))
        lexemes = list(Lexemes('_L0', '_L1', '_L2', '_L0'))
        entities = items + props + lexemes
        desc = list(kb.get_descriptor([]))
        self.assertEqual(desc, list())
        desc = list(kb.get_descriptor(items[0]))
        self.assertEqual(desc, [(items[0], None)])
        desc = list(kb.get_descriptor(entities, 'pt'))
        self.assertEqual(desc, [
            (items[0], None),
            (items[1], None),
            (items[2], None),
            (items[0], None),
            (props[0], None),
            (props[1], None),
            (props[2], None),
            (props[0], None),
            (lexemes[0], None),
            (lexemes[1], None),
            (lexemes[2], None),
            (lexemes[0], None)
        ])
        desc = list(kb.get_descriptor(entities[1:], None, 0))
        self.assertEqual(desc, [
            (items[1], None),
            (items[2], None),
            (items[0], None),
            (props[0], None),
            (props[1], None),
            (props[2], None),
            (props[0], None),
            (lexemes[0], None),
            (lexemes[1], None),
            (lexemes[2], None),
            (lexemes[0], None)
        ])

    # -- get_item_descriptor --

    def sanity_check_get_item_descriptor(self, kb):
        self.sanity_check_get_item_descriptor_bad_args(kb)
        self.sanity_check_get_item_descriptor_vacuous_calls(kb)
        it = kb.get_item_descriptor([Item('x'), Property('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_item_descriptor' "
            r'\(expected Item, got Property\)', list, it)

    def sanity_check_get_item_descriptor_bad_args(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'items', 'expected Item or Iterable, got int',
            kb.get_item_descriptor, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'language', 'expected str, got int',
            kb.get_item_descriptor, Item('Q1'), 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'mask',
            'expected Descriptor.AttributeMask or int, got str',
            kb.get_item_descriptor, Item('Q1'), 'pt', 'abc')

    def sanity_check_get_item_descriptor_vacuous_calls(self, kb):
        items = list(Items('_Q0', '_Q1', '_Q2', '_Q0'))
        desc = list(kb.get_item_descriptor([]))
        self.assertEqual(desc, list())
        desc = list(kb.get_item_descriptor(items[0]))
        self.assertEqual(desc, [(items[0], None)])
        desc = list(kb.get_item_descriptor(items, 'pt'))
        self.assertEqual(desc, [
            (items[0], None),
            (items[1], None),
            (items[2], None),
            (items[0], None),
        ])
        desc = list(kb.get_item_descriptor(items[1:], None, 0))
        self.assertEqual(desc, [
            (items[1], None),
            (items[2], None),
            (items[0], None),
        ])

    # -- get_property_descriptor --

    def sanity_check_get_property_descriptor(self, kb):
        self.sanity_check_get_property_descriptor_bad_args(kb)
        self.sanity_check_get_property_descriptor_vacuous_calls(kb)
        it = kb.get_property_descriptor([Property('x'), Item('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_property_descriptor' "
            r'\(expected Property, got Item\)', list, it)

    def sanity_check_get_property_descriptor_bad_args(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1,
            'properties', 'expected Iterable or Property, got int',
            kb.get_property_descriptor, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'language', 'expected str, got int',
            kb.get_property_descriptor, Property('P1'), 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'mask',
            'expected Descriptor.AttributeMask or int, got str',
            kb.get_property_descriptor, Property('P1'), 'pt', 'abc')

    def sanity_check_get_property_descriptor_vacuous_calls(self, kb):
        props = list(Properties('_P0', '_P1', '_P2', '_P0'))
        desc = list(kb.get_property_descriptor([]))
        self.assertEqual(desc, list())
        desc = list(kb.get_property_descriptor(props[0]))
        self.assertEqual(desc, [(props[0], None)])
        desc = list(kb.get_property_descriptor(props, 'pt'))
        self.assertEqual(desc, [
            (props[0], None),
            (props[1], None),
            (props[2], None),
            (props[0], None),
        ])
        desc = list(kb.get_property_descriptor(props[1:], None, 0))
        self.assertEqual(desc, [
            (props[1], None),
            (props[2], None),
            (props[0], None),
        ])

    # -- get_lexeme_descriptor --

    def sanity_check_get_lexeme_descriptor(self, kb):
        self.sanity_check_get_lexeme_descriptor_bad_args(kb)
        self.sanity_check_get_lexeme_descriptor_vacuous_calls(kb)
        it = kb.get_lexeme_descriptor([Lexeme('x'), Property('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_lexeme_descriptor' "
            r'\(expected Lexeme, got Property\)', list, it)

    def sanity_check_get_lexeme_descriptor_bad_args(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1,
            'lexemes', 'expected Iterable or Lexeme, got int',
            kb.get_lexeme_descriptor, 0)

    def sanity_check_get_lexeme_descriptor_vacuous_calls(self, kb):
        lexs = list(Lexemes('_L0', '_L1', '_L2', '_L0'))
        desc = list(kb.get_lexeme_descriptor([]))
        self.assertEqual(desc, list())
        desc = list(kb.get_lexeme_descriptor(lexs[0]))
        self.assertEqual(desc, [(lexs[0], None)])
        desc = list(kb.get_lexeme_descriptor(lexs))
        self.assertEqual(desc, [
            (lexs[0], None),
            (lexs[1], None),
            (lexs[2], None),
            (lexs[0], None),
        ])
        desc = list(kb.get_lexeme_descriptor(lexs[1:]))
        self.assertEqual(desc, [
            (lexs[1], None),
            (lexs[2], None),
            (lexs[0], None)
        ])


# == kif_EmptyStoreTestCase ================================================

class kif_EmptyStoreTestCase(kif_StoreTestCase):

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs):
        return super().new_Store('empty', *args, **kwargs)


# == kif_SPARQL_StoreTestCase ==============================================

class kif_SPARQL_StoreTestCase(kif_StoreTestCase):

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs):
        return super().new_Store('sparql', *args, **kwargs)


# == kif_WikidataSPARQL_StoreTestCase ======================================

class kif_WikidataSPARQL_StoreTestCase(kif_SPARQL_StoreTestCase):

    WIKIDATA = os.getenv('WIKIDATA')

    @classmethod
    def setUpClass(cls):
        if not cls.WIKIDATA:
            raise unittest.SkipTest('WIKIDATA is not set')

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs):
        return super().new_Store(cls.WIKIDATA, *args, **kwargs)


# == kif_PubChemSPARQL_StoreTestCase =======================================

class kif_PubChemSPARQL_StoreTestCase(kif_SPARQL_StoreTestCase):

    PUBCHEM = os.getenv('PUBCHEM')

    @classmethod
    def setUpClass(cls):
        if not cls.PUBCHEM:
            raise unittest.SkipTest('PUBCHEM is not set')

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs):
        from kif_lib.store.mapping import PubChemMapping
        return Store(
            'sparql-mapper', cls.PUBCHEM, PubChemMapping, *args, **kwargs)
