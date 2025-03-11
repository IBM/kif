# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import unittest

from kif_lib import (
    AnnotatedStatement,
    Entity,
    Filter,
    Item,
    Items,
    itertools,
    Lexeme,
    Lexemes,
    NoValueSnak,
    Properties,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
    Snak,
    SomeValueSnak,
    Statement,
    Store,
    Text,
    Value,
    ValueSnak,
)
from kif_lib.error import ShouldNotGetHere
from kif_lib.model import (
    TEntity,
    TFingerprint,
    TProperty,
    TValue,
    VEntity,
    VProperty,
    VStatement,
    VValue,
)
from kif_lib.store import (
    EmptyStore,
    PubChemStore,
    RDF_Store,
    SPARQL_MapperStore,
    SPARQL_Store,
    SPARQL_Store2,
    WikidataStore,
)
from kif_lib.typing import cast, Final, Iterable, override, TypeAlias
from kif_lib.vocabulary import wd

from .tests import TestCase

TFingerprintPair: TypeAlias = tuple[TFingerprint, TFingerprint]

TEntityProperty: TypeAlias = tuple[TEntity, TProperty]
VEntityProperty: TypeAlias = tuple[VEntity, VProperty]

TEntityValue: TypeAlias = tuple[TEntity, TValue]
VEntityValue: TypeAlias = tuple[VEntity, VValue]


class StoreTestCase(TestCase):
    """Test case of :class:`Store`."""

    def _test_filter(
            self,
            empty: Iterable[Filter] = (),
            equals: Iterable[tuple[Filter, Statement]] = (),
            contains: Iterable[tuple[Filter, Iterable[Statement]]] = (),
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        kb = kb or self.new_Store()
        fr = (lambda x: kb.filter(filter=x, limit=limit))
        self.assert_it(
            empty=map(fr, empty),
            equals=map(lambda t: (fr(t[0]), t[1]), equals),
            contains=map(lambda t: (fr(t[0]), t[1]), contains))

    def _test_filter_matches(
            self,
            filter: Filter,
            pattern: VStatement,
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        kb = kb or self.new_Store()
        limit = limit if limit is not None else kb.page_size
        for stmt in kb.filter(filter=filter, limit=limit):
            self.assertIsNotNone(pattern.match(stmt), str(stmt))

    def _test_filter_with_fixed_subject(
            self,
            subject: Entity,
            empty: Iterable[TFingerprintPair] = (),
            equals: Iterable[tuple[TFingerprintPair, Snak]] = (),
            contains: Iterable[tuple[TFingerprintPair, Iterable[Snak]]] = (),
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        fr = (lambda p: Filter(subject, *p))
        st = (lambda s: Statement(subject, s))
        self._test_filter(
            empty=map(fr, empty),
            equals=map(lambda t: (fr(t[0]), st(t[1])), equals),
            contains=map(lambda t: (fr(t[0]), map(st, t[1])), contains),
            kb=kb,
            limit=limit)

    def _test_filter_with_fixed_property(
            self,
            property: Property,
            empty: Iterable[TFingerprintPair] = (),
            equals: Iterable[tuple[TFingerprintPair, TEntityValue]] = (),
            contains: Iterable[
                tuple[TFingerprintPair, Iterable[TEntityValue]]] = (),
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        fr = (lambda p: Filter(p[0], property, p[1]))
        st = (lambda t: Statement(t[0], property(t[1])))
        self._test_filter(
            empty=map(fr, empty),
            equals=map(lambda t: (fr(t[0]), st(t[1])), equals),
            contains=map(lambda t: (fr(t[0]), map(st, t[1])), contains),
            kb=kb,
            limit=limit)

    def _test_filter_with_fixed_value(
            self,
            value: Value,
            empty: Iterable[TFingerprintPair] = (),
            equals: Iterable[tuple[TFingerprintPair, TEntityProperty]] = (),
            contains: Iterable[
                tuple[TFingerprintPair, Iterable[TEntityProperty]]] = (),
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        fr = (lambda p: Filter(p[0], p[1], value))
        st = (lambda t: Statement(t[0], t[1](value)))
        self._test_filter(
            empty=map(fr, empty),
            equals=map(lambda t: (fr(t[0]), st(t[1])), equals),
            contains=map(lambda t: (fr(t[0]), map(st, t[1])), contains),
            kb=kb,
            limit=limit)

    def _test_filter_preset_empty(self) -> None:
        self._test_filter(
            empty=[
                Filter(0),
                Filter(None, 0),
                Filter(None, None, 0, snak_mask=Filter.SOME_VALUE_SNAK),
            ])

# -- Legacy ----------------------------------------------------------------

    @classmethod
    def new_Store(cls, *args, **kwargs):
        return Store('empty', *args, **kwargs)

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
            TypeError, 5, 'subject_mask', None,
            kb.count, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 6, 'property_mask', None,
            kb.count, None, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 7, 'value_mask', None,
            kb.count, None, None, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 8, 'rank_mask', None,
            kb.count, None, None, None, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 9, 'language', None,
            kb.count, None, None, None, None, None, None, None, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 11, 'snak', None,
            kb.count, None, None, None, None, None, None, None, None, None,
            None, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 12, 'filter', None,
            kb.count, None, None, None, None, None, None, None, None, None,
            None, None, Item('x'))

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
            TypeError, 5, 'subject_mask', None,
            kb.filter, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 6, 'property_mask', None,
            kb.filter, None, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 7, 'value_mask', None,
            kb.filter, None, None, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 8, 'rank_mask', None,
            kb.filter, None, None, None, None, None, None, None, {})
        self.assert_raises_bad_argument(
            TypeError, 9, 'language', None,
            kb.filter, None, None, None, None, None, None, None, None, 0)
        self.assert_raises_bad_argument(
            TypeError, 11, 'snak', None,
            kb.filter, None, None, None, None, None, None, None, None, None,
            None, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 12, 'filter', None,
            kb.filter, None, None, None, None, None, None, None, None, None,
            None, None, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 13, 'limit', None, kb.filter, limit=Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 14, 'distinct', None, kb.filter, distinct=Item('x'))

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
        for stmt in res_annotated:
            self.assertIsInstance(stmt, AnnotatedStatement)
            self.assertIn(Statement(*stmt.claim), set(stmts))
        for stmt in stmts:
            res_annotated_snak = list(kb.filter_annotated(
                stmt.subject, snak=stmt.snak))
            self.assertEqual(len(res_annotated_snak), 1)
            self.assertEqual(res_annotated_snak[0].claim, stmt.claim)
            self.assertIsInstance(res_annotated_snak[0], AnnotatedStatement)
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


class EmptyStoreTestCase(StoreTestCase):
    """Test case of :class:`EmptyStore`."""

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> EmptyStore:
        return cast(EmptyStore, Store('empty', *args, **kwargs))


class SPARQL_StoreTestCase(StoreTestCase):
    """Test case of :class:`SPARQL_Store`."""

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_Store:
        return cast(SPARQL_Store, Store('sparql', *args, **kwargs))


class RDF_StoreTestCase(StoreTestCase):
    """Test case of :class:`RDF_Store`."""

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> RDF_Store:
        return cast(RDF_Store, Store('rdf', *args, **kwargs))


class WikidataStoreTestCase(SPARQL_StoreTestCase):
    """Test case of :class:`WikidataStore`."""

    WIKIDATA: Final[str | None] = os.getenv('WIKIDATA')

    @classmethod
    def setUpClass(cls):
        if not cls.WIKIDATA:
            raise unittest.SkipTest('WIKIDATA is not set')

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> WikidataStore:
        assert cls.WIKIDATA is not None
        return cast(WikidataStore, Store(
            'wikidata', cls.WIKIDATA, *args, **kwargs))


class SPARQL_MapperStoreTestCase(SPARQL_StoreTestCase):
    """Test case of :class:`SPARQL_MapperStore`."""

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_MapperStore:
        return cast(SPARQL_MapperStore, Store(
            'sparql-mapper', *args, **kwargs))


class PubChemSPARQL_StoreTestCase(SPARQL_MapperStoreTestCase):
    """Test case of :class:`SPARQL_MapperStore` loaded with PubChem mapping."""

    PUBCHEM: Final[str | None] = os.getenv('PUBCHEM')

    @classmethod
    def setUpClass(cls):
        if not cls.PUBCHEM:
            raise unittest.SkipTest('PUBCHEM is not set')

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_MapperStore:
        from kif_lib.store.mapping import PubChemMapping
        assert cls.PUBCHEM is not None
        return cast(SPARQL_MapperStore, Store(
            'sparql-mapper', cls.PUBCHEM, PubChemMapping(), *args, **kwargs))


class SPARQL_Store2TestCase(SPARQL_StoreTestCase):
    """Test case of :class:`SPARQL_Store2`."""

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> SPARQL_Store2:
        return cast(SPARQL_Store2, Store('sparql2', *args, **kwargs))


class PubChemStoreTestCase(SPARQL_Store2TestCase):
    """Test case of :class:`PubChemStore`."""

    PUBCHEM: Final[str | None] = os.getenv('PUBCHEM')

    @classmethod
    def setUpClass(cls):
        if not cls.PUBCHEM:
            raise unittest.SkipTest('PUBCHEM is not set')

    @override
    @classmethod
    def new_Store(cls, *args, **kwargs) -> PubChemStore:
        assert cls.PUBCHEM is not None
        return cast(PubChemStore, Store(
            'pubchem', cls.PUBCHEM, *args, **kwargs))
