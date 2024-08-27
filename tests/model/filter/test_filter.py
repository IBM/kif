# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    Filter,
    IRI,
    Item,
    Items,
    ItemTemplate,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    Snak,
    SnakSet,
    SomeValueSnak,
    Statement,
    Text,
    Time,
    Variable,
)
from kif_lib.model import ValueFingerprint
from kif_lib.typing import assert_type

from ...tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_from_snak(self) -> None:
        # snak is none
        pat = Filter.from_snak(Item('x'), None)
        self.assert_filter(
            pat, ValueFingerprint(Item('x')), None, None, Filter.SnakMask.ALL)
        # value snak
        snak: Snak = Property('p')(Item('x'))
        pat = Filter.from_snak(Item('x'), snak)
        self.assert_filter(
            pat,
            ValueFingerprint(Item('x')),
            ValueFingerprint(Property('p', Item)),
            ValueFingerprint(Item('x')),
            Filter.VALUE_SNAK)
        # some value snak
        snak = SomeValueSnak(Property('p'))
        pat = Filter.from_snak(Item('x'), snak)
        self.assert_filter(
            pat,
            ValueFingerprint(Item('x')),
            ValueFingerprint(Property('p')),
            None,
            Filter.SOME_VALUE_SNAK)
        # no value snak
        snak = NoValueSnak(Property('p'))
        pat = Filter.from_snak(Item('x'), snak)
        self.assert_filter(
            pat,
            ValueFingerprint(Item('x')),
            ValueFingerprint(Property('p')),
            None,
            Filter.NO_VALUE_SNAK)

    def test_from_statement(self) -> None:
        # value snak
        stmt = Property('p')(Item('x'), IRI('y'))
        pat = Filter.from_statement(stmt)
        self.assert_filter(
            pat,
            ValueFingerprint(Item('x')),
            ValueFingerprint(Property('p', IRI)),
            ValueFingerprint(IRI('y')),
            Filter.VALUE_SNAK)
        # some value snak
        stmt = Statement(Item('x'), SomeValueSnak(Property('p')))
        pat = Filter.from_statement(stmt)
        self.assert_filter(
            pat,
            ValueFingerprint(Item('x')),
            ValueFingerprint(Property('p')),
            None,
            Filter.SOME_VALUE_SNAK)
        # no value snak
        stmt = Statement(Item('x'), NoValueSnak(Property('p')))
        pat = Filter.from_statement(stmt)
        self.assert_filter(
            pat,
            ValueFingerprint(Item('x')),
            ValueFingerprint(Property('p')),
            None,
            Filter.NO_VALUE_SNAK)

    def test_check(self) -> None:
        assert_type(Filter.check(Filter()), Filter)
        self._test_check(
            Filter,
            success=[
                (Filter(), Filter()),
                (Filter(Item('x')), Filter(Item('x')))
            ],
            failure=[
                0,
                Item('x'),
                ItemTemplate(Variable('x')),
                Lexeme('x'),
                Property('x'),
                Text('x'),
                Variable('x', Text),
                {},
            ])

    def test__init__(self) -> None:
        self.assertRaises(TypeError, Filter, {})
        self.assert_filter(Filter())

    def test_is_empty(self) -> None:
        assert_type(Filter().is_empty(), bool)
        self.assertFalse(Filter().is_empty())
        self.assertTrue(Filter().is_nonempty())
        self.assertTrue(Filter().is_full())
        self.assertTrue(Filter(None, None, None, 0).is_empty())
        self.assertFalse(Filter(None, None, None, 0).is_nonempty())
        pat = Filter(
            None, None, IRI('x'), Filter.SOME_VALUE_SNAK)
        self.assertTrue(pat.is_empty())
        self.assertFalse(pat.is_nonempty())
        pat = Filter(None, None, IRI('x'), Filter.NO_VALUE_SNAK)
        self.assertTrue(pat.is_empty())
        self.assertFalse(pat.is_nonempty())

    def test_is_nonempty(self) -> None:
        assert_type(Filter().is_nonempty(), bool)
        self.assertTrue(Filter().is_nonempty())
        self.assertFalse(Filter(snak_mask=0).is_nonempty())

    def test_is_full(self) -> None:
        assert_type(Filter().is_full(), bool)
        self.assertTrue(Filter().is_full())
        self.assertFalse(Filter().is_nonfull())

    def test_is_nonfull(self) -> None:
        assert_type(Filter().is_nonfull(), bool)
        self.assertTrue(Filter(Item('x')).is_nonfull())
        self.assertFalse(Filter().is_nonfull())

    def test_match(self) -> None:
        assert_type(Filter().match((Item('x'), 'y', 'z')), bool)
        self.assert_raises_bad_argument(
            TypeError, 1, 'stmt',
            'cannot coerce int into Statement', Filter().match, 0)
        x, y = Items('x', 'y')
        p = Property('p')
        self.assertFalse(
            Filter(snak_mask=Filter.NO_VALUE_SNAK).match(p(x, 'y')))
        self.assertFalse(Filter(Item('y')).match(p(x, 'y')))
        self.assertTrue(Filter(property=p).match(p(x, x)))
        self.assertTrue(Filter(property=p).match(
            p.replace(p.KEEP, Item)(x, x)))
        self.assertTrue(Filter(property=p.replace(p.KEEP, Item)).match(
            Statement(x, NoValueSnak(p))))
        self.assertFalse(Filter(property=p.replace(p.KEEP, Property)).match(
            p.replace(p.KEEP, Item)(x, x)))
        self.assertFalse(Filter(snak_mask=Filter.SOME_VALUE_SNAK).match(
            p(x, x)))
        self.assertFalse(Filter(value=x).match((x, SomeValueSnak(p))))
        self.assertFalse(Filter(value=x).match((x, p, p)))
        self.assertFalse(Filter(value=Quantity(0)).match((x, p, x)))
        self.assertFalse(Filter(value=x).match((x, p, Quantity(0))))
        self.assertFalse(Filter(subject=x).match((y, p, Quantity(0))))
        self.assertFalse(Filter(value=x).match((x, p, y)))
        self.assertTrue(Filter(value=Quantity(0)).match((x, p, Quantity(0))))
        self.assertTrue(Filter(
            value=Quantity(0)).match((x, p, Quantity(0, y))))
        self.assertFalse(Filter(
            value=Quantity(0, y)).match((x, p, Quantity(0))))
        self.assertTrue(Filter(
            value=Quantity(0)).match((x, p, Quantity(0, y, 1))))
        self.assertFalse(Filter(
            value=Quantity(0, None, 1)).match((x, p, Quantity(0))))
        self.assertTrue(Filter(
            value=Quantity(0)).match((x, p, Quantity(0, y, 1, 2))))
        self.assertFalse(Filter(
            value=Quantity(0, None, None, 2)).match((x, p, Quantity(0))))
        self.assertTrue(Filter(
            value=Time('2024-07-11')).match((x, p, Time('2024-07-11'))))
        self.assertTrue(Filter(
            value=Time('2024-07-11', 0)).match((x, p, Time('2024-07-11', 0))))
        self.assertFalse(Filter(
            value=Time('2024-07-11', 0)).match((x, p, Time('2024-07-11', 1))))
        self.assertTrue(Filter(
            value=Time(datetime.datetime(2024, 7, 11), None, 1)).match(
                (x, p, Time('2024-07-11', 0, 1))))
        self.assertTrue(Filter(
            value=Time('2024-07-11', None, 1)).match(
                (x, p, Time('2024-07-11', 0, 1))))
        self.assertFalse(Filter(
            value=Time('2024-07-11', None, 0)).match(
                (x, p, Time('2024-07-11'))))
        self.assertTrue(Filter(
            value=Time('2024-07-11', None, 1, Item('x'))).match(
                (x, p, Time('2024-07-11', 0, 1, x))))
        self.assertFalse(Filter(
            value=Time('2024-07-11', None, 0, Item('x'))).match(
                (x, p, Time('2024-07-11', None, None, y))))

    def test_combine(self) -> None:
        # bad argument
        pat = Filter(Item('x'))
        self.assertRaises(TypeError, pat.combine, 0)
        # good arguments
        pat1 = Filter(Item('x'))
        pat2 = Filter(SnakSet())
        self.assertEqual(
            pat1.combine(pat2), Filter(Item('x') & SnakSet()).normalize())
        pat1 = Filter(None, SnakSet(NoValueSnak(Property('x'))))
        pat2 = Filter(None, Property('p'))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(None, SnakSet(NoValueSnak(Property('x')))
                   & Property('p')).normalize())
        pat1 = Filter(None, None, SnakSet(NoValueSnak(Property('x'))))
        pat2 = Filter(None, None, Property('p'))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(None, None, SnakSet(NoValueSnak(Property('x')))
                   & Property('p')).normalize())
        self.assertEqual(Filter().combine(), Filter())
        self.assertEqual(
            Filter().combine(Filter()), Filter())
        # subject
        pat1 = Filter(Item('x'))
        pat2 = Filter(None, Property('p'))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(Item('x'), Property('p'), subject_mask=Filter.ITEM))
        pat1 = Filter(SnakSet(SomeValueSnak(Property('p'))))
        pat2 = Filter(SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            Filter([
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]).normalize())
        # property
        pat1 = Filter(None, Property('p'))
        pat2 = Filter(Item('x'))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(Item('x'), Property('p'), subject_mask=Filter.ITEM))
        pat1 = Filter(None, SnakSet(SomeValueSnak(Property('p'))))
        pat2 = Filter(None, SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(None, [
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]).normalize())
        # value
        pat1 = Filter(None, Property('p'), IRI('x'))
        pat2 = Filter(Item('x'), None, None)
        self.assertEqual(
            pat1.combine(pat2),
            Filter(Item('x'), Property('p'), IRI('x'),
                   snak_mask=Filter.VALUE_SNAK,
                   subject_mask=Filter.ITEM,
                   value_mask=Filter.IRI))
        pat1 = Filter(
            None, None, SnakSet(SomeValueSnak(Property('p'))))
        pat2 = Filter(
            None, None, SnakSet(NoValueSnak(Property('q'))))
        self.assertEqual(
            pat1.combine(pat2),
            Filter(None, None, [
                SomeValueSnak(Property('p')),
                NoValueSnak(Property('q'))]).normalize())
        # snak mask
        self.assertEqual(
            Filter(None, None, None, Filter.SnakMask.ALL).combine(
                Filter(None, None, None, Filter.VALUE_SNAK)),
            Filter(None, None, None, Filter.VALUE_SNAK))


if __name__ == '__main__':
    Test.main()
