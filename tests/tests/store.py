# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools
import os
import unittest

from kif_lib import (
    AnnotationRecordSet,
    Filter,
    Item,
    Items,
    Lexeme,
    Lexemes,
    NoValueSnak,
    Properties,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
    SomeValueSnak,
    Store,
    Text,
    Value,
    ValueSnak,
)
from kif_lib.error import ShouldNotGetHere
from kif_lib.store import (
    EmptyStore,
    RDF_Store,
    SPARQL_MapperStore,
    SPARQL_Store,
)
from kif_lib.typing import cast, Final, Optional, override
from kif_lib.vocabulary import wd

from .tests import kif_TestCase


class kif_StoreTestCase(kif_TestCase):

    @classmethod
    def new_Store(cls, store_name: str, *args, **kwargs):
        return Store(store_name, *args, **kwargs)

    @classmethod
    def parse(cls, text: str) -> Store:
        from kif_lib.namespace import PREFIXES
        pre = '\n'.join(
            map(lambda t: f'@prefix {t[0]}: <{t[1]}> .', PREFIXES.items()))
        return Store('rdf', format='ttl', data=pre + '\n\n' + text)

    def store_sanity_checks(self, kb: Store):
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
        self.store_test_count_empty(kb)
        # filter
        self.store_test_filter_bad_argument(kb)
        self.store_test_filter_empty(kb)
        # get_annotations
        self.store_test_get_annotations_bad_argument(kb)
        self.store_test_get_annotations_empty(kb)
        # TODO: get descriptor
        # self.store_test_get_descriptor_bad_argument(kb)
        # self.store_test_get_descriptor_empty(kb)

    def store_test_extra_references(
            self,
            kb: Store,
            default: ReferenceRecordSet = ReferenceRecordSet()
    ):
        self.assertRaises(TypeError, kb.set_extra_references, 'abc')
        self.assertEqual(kb.extra_references, default)
        kb.extra_references = ReferenceRecordSet(
            ReferenceRecord(),
            ReferenceRecord(wd.stated_in(wd.PubChem)))
        self.assertEqual(
            kb.extra_references, ReferenceRecordSet(
                ReferenceRecord(), ReferenceRecord(wd.stated_in(wd.PubChem))))
        kb.extra_references = ReferenceRecordSet()
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
            if isinstance(stmt.snak, ValueSnak):
                values.append(stmt)
            elif isinstance(stmt.snak, SomeValueSnak):
                some_values.append(stmt)
            elif isinstance(stmt.snak, NoValueSnak):
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
            TypeError, 1, 'subject', None, kb.count, {})
        self.assert_raises_bad_argument(
            TypeError, 2, 'property', None, kb.count, None, {})
        self.assert_raises_bad_argument(
            TypeError, 3, 'value', None, kb.count, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.count, None, None, None, 'abc')
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.count, None, None, Item('x'), Item)
        self.assert_raises_bad_argument(
            TypeError, 5, 'snak', None,
            kb.count, None, None, Item('x'), Filter.NO_VALUE_SNAK, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 6, 'filter', None, kb.count, filter=Item('x'))

    def store_test_count_empty(self, kb):
        saved_flags = kb.flags
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        self.assertEqual(kb.count(), 0)
        kb.flags = saved_flags
        empty = Filter(None, None, None, Filter.SnakMask(0))
        self.assertEqual(kb.count(filter=empty), 0)

    def store_test_count(
            self, kb, n, subject=None, property=None, value=None,
            snak_mask=None, filter=None):
        self.assertEqual(kb.count(
            subject, property, value, snak_mask, filter), n)
        if (filter is None
            and property is not None and value is not None
                and isinstance(property, Property)
                and isinstance(value, Value)):
            self.assertEqual(kb.count(subject, snak=property(value)), n)
            saved_flags = kb.flags
            kb.unset_flags(kb.VALUE_SNAK)
            self.assertEqual(kb.count(subject, snak=property(value)), 0)
            kb.flags = saved_flags
        elif (filter is None
              and property is not None
              and isinstance(property, Property)
              and snak_mask == Filter.SOME_VALUE_SNAK):
            some_value = SomeValueSnak(property)
            self.assertEqual(kb.count(subject, snak=some_value), n)
            saved_flags = kb.flags
            kb.unset_flags(kb.SOME_VALUE_SNAK)
            self.assertEqual(kb.count(subject, snak=some_value), 0)
            kb.flags = saved_flags
        elif (filter is None
              and property is not None
              and isinstance(property, Property)
              and snak_mask == Filter.NO_VALUE_SNAK):
            no_value = NoValueSnak(property)
            self.assertEqual(kb.count(subject, snak=no_value), n)
            saved_flags = kb.flags
            kb.unset_flags(kb.NO_VALUE_SNAK)
            self.assertEqual(kb.count(subject, snak=no_value), 0)
            kb.flags = saved_flags

    def store_test_filter_bad_argument(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'subject', None, kb.filter, {})
        self.assert_raises_bad_argument(
            TypeError, 2, 'property', None, kb.filter, None, {})
        self.assert_raises_bad_argument(
            TypeError, 3, 'value', None, kb.filter, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.filter, None, None, None, 'a')
        self.assert_raises_bad_argument(
            TypeError, 4, 'snak_mask', None,
            kb.filter, None, None, Item('x'), Item)
        self.assert_raises_bad_argument(
            TypeError, 5, 'snak', None,
            kb.filter, None, None, Item('x'),
            Filter.NO_VALUE_SNAK, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 6, 'filter', None, kb.filter, filter=Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 7, 'limit', None, kb.filter, limit=Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 8, 'distinct', None, kb.filter, distinct=Item('x'))

    def store_test_filter_empty(self, kb):
        saved_flags = kb.flags
        kb.unset_flags(kb.VALUE_SNAK | kb.SOME_VALUE_SNAK | kb.NO_VALUE_SNAK)
        self.assertFalse(bool(set(kb.filter())))
        kb.flags = saved_flags
        empty = Filter(None, None, None, Filter.SnakMask(0))
        self.assertFalse(bool(set(kb.filter(filter=empty))))
        self.assertFalse(bool(set(kb.filter(limit=0))))
        self.assertFalse(bool(set(kb.filter(limit=-1))))

    def store_test_filter(
            self, kb, stmts, subject=None, property=None, value=None,
            snak_mask=None, filter=None, limit=None):
        res = set(kb.filter(
            subject, property, value, snak_mask, filter, limit))
        self.assertEqual(set(stmts), res)
        res_annotated = set(kb.filter_annotated(
            subject, property, value, snak_mask, filter, limit))
        for i, (stmt, annots) in enumerate(res_annotated):
            self.assertIn(stmt, set(stmts))
            self.assertIsInstance(annots, AnnotationRecordSet)
        for stmt in stmts:
            res_annotated_snak = list(kb.filter_annotated(
                stmt.subject, snak=stmt.snak))
            self.assertEqual(len(res_annotated_snak), 1)
            self.assertEqual(res_annotated_snak[0][0], stmt)
            self.assertIsInstance(
                res_annotated_snak[0][1], AnnotationRecordSet)
            break               # check only the first
        if (filter is None
            and property is not None and value is not None
            and isinstance(property, Property)
                and isinstance(value, Value)):
            self.assertEqual(set(kb.filter(
                subject, snak=property(value))), res)
            saved_flags = kb.flags
            kb.unset_flags(kb.VALUE_SNAK)
            self.assertFalse(bool(set(kb.filter(
                subject, snak=property(value)))))
            kb.flags = saved_flags
        elif (filter is None
              and property is not None
              and isinstance(property, Property)
              and snak_mask == Filter.SOME_VALUE_SNAK):
            some_value = SomeValueSnak(property)
            self.assertEqual(set(kb.filter(subject, snak=some_value)), res)
            saved_flags = kb.flags
            kb.unset_flags(kb.SOME_VALUE_SNAK)
            self.assertFalse(bool(set(kb.filter(subject, snak=some_value))))
            kb.flags = saved_flags
        elif (filter is None
              and property is not None
              and isinstance(property, Property)
              and snak_mask == Filter.NO_VALUE_SNAK):
            no_value = NoValueSnak(property)
            self.assertEqual(set(kb.filter(subject, snak=no_value)), res)
            saved_flags = kb.flags
            kb.unset_flags(kb.NO_VALUE_SNAK)
            self.assertFalse(bool(set(kb.filter(subject, snak=no_value))))
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
            if isinstance(stmt.snak, ValueSnak):
                values.append((i, got[i]))
            elif isinstance(stmt.snak, SomeValueSnak):
                some_values.append((i, got[i]))
            elif isinstance(stmt.snak, NoValueSnak):
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

    def sanity_check_get_descriptor(self, kb):
        self.sanity_check_get_descriptor_bad_args(kb)
        self.sanity_check_get_descriptor_vacuous_calls(kb)
        it = kb.get_descriptor([Item('x'), Text('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_descriptor' "
            r'\(cannot coerce Text into Entity\)', list, it)

    def sanity_check_get_descriptor_bad_args(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'entities', 'expected Entity or Iterable, got int',
            kb.get_descriptor, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'language', 'expected str, got int',
            kb.get_descriptor, Item('Q1'), 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'mask',
            'cannot coerce str into Descriptor.AttributeMask',
            kb.get_descriptor, Item('Q1'), 'pt', 'abc')

    def sanity_check_get_descriptor_vacuous_calls(self, kb):
        items = list(Items('_Q0', '_Q1', '_Q2', '_Q0'))
        props = list(Properties('_P0', '_P1', '_P2', '_P0'))
        lexemes = list(Lexemes('_L0', '_L1', '_L2', '_L0'))
        entities = items + props + lexemes
        desc = list(kb.get_descriptor([]))
        self.assertEqual(desc, [])
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

    def sanity_check_get_item_descriptor(self, kb):
        self.sanity_check_get_item_descriptor_bad_args(kb)
        self.sanity_check_get_item_descriptor_vacuous_calls(kb)
        it = kb.get_item_descriptor([Item('x'), Property('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_item_descriptor' "
            r'\(cannot coerce Property into IRI\)', list, it)

    def sanity_check_get_item_descriptor_bad_args(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1, 'items', 'expected Item or Iterable, got int',
            kb.get_item_descriptor, 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'language', 'expected str, got int',
            kb.get_item_descriptor, Item('Q1'), 0)
        self.assert_raises_bad_argument(
            TypeError, 3, 'mask',
            'cannot coerce str into Descriptor.AttributeMask',
            kb.get_item_descriptor, Item('Q1'), 'pt', 'abc')

    def sanity_check_get_item_descriptor_vacuous_calls(self, kb):
        items = list(Items('_Q0', '_Q1', '_Q2', '_Q0'))
        desc = list(kb.get_item_descriptor([]))
        self.assertEqual(desc, [])
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

    def sanity_check_get_property_descriptor(self, kb):
        self.sanity_check_get_property_descriptor_bad_args(kb)
        self.sanity_check_get_property_descriptor_vacuous_calls(kb)
        it = kb.get_property_descriptor([Property('x'), Item('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_property_descriptor' "
            r'\(cannot coerce Item into IRI\)', list, it)

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
            'cannot coerce str into Descriptor.AttributeMask',
            kb.get_property_descriptor, Property('P1'), 'pt', 'abc')

    def sanity_check_get_property_descriptor_vacuous_calls(self, kb):
        props = list(Properties('_P0', '_P1', '_P2', '_P0'))
        desc = list(kb.get_property_descriptor([]))
        self.assertEqual(desc, [])
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

    def sanity_check_get_lexeme_descriptor(self, kb):
        self.sanity_check_get_lexeme_descriptor_bad_args(kb)
        self.sanity_check_get_lexeme_descriptor_vacuous_calls(kb)
        it = kb.get_lexeme_descriptor([Lexeme('x'), Property('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_lexeme_descriptor' "
            r'\(cannot coerce Property into IRI\)', list, it)

    def sanity_check_get_lexeme_descriptor_bad_args(self, kb):
        self.assert_raises_bad_argument(
            TypeError, 1,
            'lexemes', 'expected Iterable or Lexeme, got int',
            kb.get_lexeme_descriptor, 0)

    def sanity_check_get_lexeme_descriptor_vacuous_calls(self, kb):
        lexs = list(Lexemes('_L0', '_L1', '_L2', '_L0'))
        desc = list(kb.get_lexeme_descriptor([]))
        self.assertEqual(desc, [])
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


class kif_EmptyStoreTestCase(kif_StoreTestCase):

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> EmptyStore:
        return cast(EmptyStore, super().new_Store('empty', *args, **kwargs))


class kif_SPARQL_StoreTestCase(kif_StoreTestCase):

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_Store:
        return cast(
            SPARQL_Store, super().new_Store('sparql', *args, **kwargs))


class kif_RDF_StoreTestCase(kif_StoreTestCase):

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> RDF_Store:
        return cast(RDF_Store, super().new_Store('rdf', *args, **kwargs))


class kif_WikidataSPARQL_StoreTestCase(kif_SPARQL_StoreTestCase):

    WIKIDATA: Final[Optional[str]] = os.getenv('WIKIDATA')

    @classmethod
    def setUpClass(cls):
        if not cls.WIKIDATA:
            raise unittest.SkipTest('WIKIDATA is not set')

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_Store:
        return cast(SPARQL_Store, super().new_Store(
            cls.WIKIDATA, *args, **kwargs))


class kif_SPARQL_MapperStoreTestCase(kif_SPARQL_StoreTestCase):

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_MapperStore:
        return cast(
            SPARQL_MapperStore,
            kif_StoreTestCase.new_Store('sparql-mapper', *args, **kwargs))


class kif_PubChemSPARQL_StoreTestCase(kif_SPARQL_MapperStoreTestCase):

    PUBCHEM: Final[Optional[str]] = os.getenv('PUBCHEM')

    @classmethod
    def setUpClass(cls):
        if not cls.PUBCHEM:
            raise unittest.SkipTest('PUBCHEM is not set')

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_MapperStore:
        from kif_lib.store.mapping import PubChemMapping
        return cast(SPARQL_MapperStore, super().new_Store(
            cls.PUBCHEM, PubChemMapping(), *args, **kwargs))
