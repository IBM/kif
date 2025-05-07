# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Fingerprint, IRI, Item, Lexeme, Property, Store
from kif_lib.typing import Final

from ...tests import TestCase

FP = Fingerprint.check


class Test(TestCase):

    F1: Final[Filter] = Filter(Item('x'))

    F2: Final[Filter] = Filter(
        Item('x'), Property('y'), Item('z') | Lexeme('w'),
        snak_mask=Filter.VALUE_SNAK,
        subject_mask=Filter.ITEM,
        property_mask=Filter.PROPERTY,
        value_mask=Filter.ENTITY,
        rank_mask=Filter.PREFERRED,
        language='fr',
        annotated=True)

    def test_base_filter(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.default_base_filter, Filter())

    def test__init__base_filter(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.base_filter, kb.default_base_filter)
        kb = Store('empty', base_filter=self.F1)
        self.assertEqual(kb.base_filter, self.F1)
        kb = Store('empty', base_filter=None)
        self.assertEqual(kb.base_filter, kb.default_base_filter)

    def test_get_base_filter(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.base_filter, kb.default_base_filter)
        self.assertEqual(kb.get_base_filter(), kb.default_base_filter)
        kb = Store('empty', base_filter=self.F2)
        self.assertEqual(kb.base_filter, self.F2)
        self.assertEqual(kb.get_base_filter(), self.F2)
        self.assertEqual(kb.get_base_filter(), self.F2)

    def test_set_base_filter(self) -> None:
        kb = Store('empty')
        self.assert_raises_bad_argument(
            TypeError, 1, 'base_filter',
            'cannot coerce int into Filter', kb.set_base_filter, 0)
        self.assertEqual(kb.get_base_filter(), kb.default_base_filter)
        kb.base_filter = self.F1
        self.assertEqual(kb.base_filter, self.F1)
        kb.base_filter = None   # type: ignore
        self.assertEqual(kb.get_base_filter(), kb.default_base_filter)
        kb.base_filter = self.F1
        self.assertEqual(kb.get_base_filter(), self.F1)
        kb.base_filter = Filter()
        self.assertEqual(kb.get_base_filter(), Filter())
        kb.base_filter = None  # type: ignore
        self.assertEqual(kb.get_base_filter(), kb.default_base_filter)
        self.assertEqual(kb.base_filter, kb.default_base_filter)

    def test_get_subject(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.subject, kb.base_filter.subject)
        kb.subject = FP(Item('x'))
        self.assertEqual(kb.subject, FP(Item('x')))

    def test_set_subject(self) -> None:
        kb = Store('empty', base_filter=self.F1)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into Value',
            (kb.set_subject, 'Filter'), {})
        self.assertEqual(kb.subject, self.F1.subject)
        self.assertEqual(kb.base_filter.subject, self.F1.subject)
        kb.set_subject(Item('y'))
        self.assertEqual(kb.subject, FP(Item('y')))
        self.assertEqual(kb.base_filter.subject, FP(Item('y')))

    def test_get_property(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.property, kb.base_filter.property)
        kb.property = FP(Property('x'))
        self.assertEqual(kb.property, FP(Property('x')))

    def test_set_property(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (kb.set_property, 'Filter'), {})
        self.assertEqual(kb.property, self.F2.property)
        self.assertEqual(kb.base_filter.property, self.F2.property)
        kb.set_property(Property('y'))
        self.assertEqual(kb.property, FP(Property('y')))
        self.assertEqual(kb.base_filter.property, FP(Property('y')))

    def test_get_value(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.value, kb.base_filter.value)
        kb.value = FP(IRI('x'))
        self.assertEqual(kb.value, FP(IRI('x')))

    def test_set_value(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'cannot coerce dict into Value',
            (kb.set_value, 'Filter'), {})
        self.assertEqual(kb.value, self.F2.value)
        self.assertEqual(kb.base_filter.value, self.F2.value)
        kb.set_value(IRI('y'))
        self.assertEqual(kb.value, FP(IRI('y')))
        self.assertEqual(kb.base_filter.value, FP(IRI('y')))

    def test_get_snak_mask(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.snak_mask, kb.base_filter.snak_mask)
        kb.snak_mask = Filter.VALUE_SNAK
        self.assertEqual(kb.snak_mask, Filter.VALUE_SNAK)

    def test_set_snak_mask(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            'cannot coerce dict into Snak',
            (kb.set_snak_mask, 'Filter'), {})
        self.assertEqual(kb.snak_mask, self.F2.snak_mask)
        self.assertEqual(kb.base_filter.snak_mask, self.F2.snak_mask)
        kb.set_snak_mask(Filter.NO_VALUE_SNAK)
        self.assertEqual(kb.snak_mask, Filter.NO_VALUE_SNAK)
        self.assertEqual(kb.base_filter.snak_mask, Filter.NO_VALUE_SNAK)

    def test_get_subject_mask(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.subject_mask, kb.base_filter.subject_mask)
        kb.subject_mask = Filter.ITEM
        self.assertEqual(kb.subject_mask, Filter.ITEM)

    def test_set_subject_mask(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 5, None,
            'cannot coerce dict into Datatype',
            (kb.set_subject_mask, 'Filter'), {})
        self.assertEqual(kb.subject_mask, self.F2.subject_mask)
        self.assertEqual(kb.base_filter.subject_mask, self.F2.subject_mask)
        kb.set_subject_mask(Filter.ITEM)
        self.assertEqual(kb.subject_mask, Filter.ITEM)
        self.assertEqual(kb.base_filter.subject_mask, Filter.ITEM)

    def test_get_property_mask(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.property_mask, kb.base_filter.property_mask)
        kb.property_mask = Filter.PROPERTY
        self.assertEqual(kb.property_mask, Filter.PROPERTY)

    def test_set_property_mask(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 6, None,
            'cannot coerce dict into Datatype',
            (kb.set_property_mask, 'Filter'), {})
        self.assertEqual(kb.property_mask, self.F2.property_mask)
        self.assertEqual(kb.base_filter.property_mask, self.F2.property_mask)
        kb.set_property_mask(Filter.PROPERTY)
        self.assertEqual(kb.property_mask, Filter.PROPERTY)
        self.assertEqual(kb.base_filter.property_mask, Filter.PROPERTY)

    def test_get_value_mask(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.value_mask, kb.base_filter.value_mask)
        kb.value_mask = Filter.QUANTITY
        self.assertEqual(kb.value_mask, Filter.QUANTITY)

    def test_set_value_mask(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 7, None,
            'cannot coerce dict into Datatype',
            (kb.set_value_mask, 'Filter'), {})
        self.assertEqual(kb.value_mask, self.F2.value_mask)
        self.assertEqual(kb.base_filter.value_mask, self.F2.value_mask)
        kb.set_value_mask(Filter.QUANTITY)
        self.assertEqual(kb.value_mask, Filter.QUANTITY)
        self.assertEqual(kb.base_filter.value_mask, Filter.QUANTITY)

    def test_get_rank_mask(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.rank_mask, kb.base_filter.rank_mask)
        kb.rank_mask = Filter.DEPRECATED
        self.assertEqual(kb.rank_mask, Filter.DEPRECATED)

    def test_set_rank_mask(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 8, None,
            'cannot coerce dict into Rank',
            (kb.set_rank_mask, 'Filter'), {})
        self.assertEqual(kb.rank_mask, self.F2.rank_mask)
        self.assertEqual(kb.base_filter.rank_mask, self.F2.rank_mask)
        kb.set_rank_mask(Filter.DEPRECATED)
        self.assertEqual(kb.rank_mask, Filter.DEPRECATED)
        self.assertEqual(kb.base_filter.rank_mask, Filter.DEPRECATED)

    def test_get_language(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.language, kb.base_filter.language)
        kb.language = 'pt'
        self.assertEqual(kb.language, 'pt')

    def test_set_language(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assert_raises_bad_argument(
            TypeError, 9, None,
            'cannot coerce dict into String',
            (kb.set_language, 'Filter'), {})
        self.assertEqual(kb.language, self.F2.language)
        self.assertEqual(kb.base_filter.language, self.F2.language)
        kb.set_language('pt')
        self.assertEqual(kb.language, 'pt')
        self.assertEqual(kb.base_filter.language, 'pt')

    def test_get_annotated(self) -> None:
        kb = Store('empty')
        self.assertEqual(kb.annotated, kb.base_filter.annotated)
        kb.annotated = True
        self.assertEqual(kb.annotated, True)

    def test_set_annotated(self) -> None:
        kb = Store('empty', base_filter=self.F2)
        self.assertEqual(kb.annotated, self.F2.annotated)
        self.assertEqual(kb.base_filter.annotated, self.F2.annotated)
        kb.set_annotated(False)
        self.assertEqual(kb.annotated, False)
        self.assertEqual(kb.base_filter.annotated, False)


if __name__ == '__main__':
    Test.main()
