# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Filter,
    NoValueSnak,
    Property,
    Snak,
    SomeValueSnak,
    ValueSnak,
)
from kif_lib.typing import assert_type

from ...tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_check(self) -> None:
        assert_type(Filter.SnakMask.check(Snak), Filter.SnakMask)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Filter.SnakMask.check, 'abc')
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Filter.SnakMask.check, 8)
        self.assertEqual(Filter.SnakMask.check(0), Filter.SnakMask(0))
        self.assertEqual(
            Filter.SnakMask.check(Snak), Filter.SnakMask(Filter.SnakMask.ALL))
        self.assertEqual(
            Filter.SnakMask.check(ValueSnak),
            Filter.SnakMask(Filter.SnakMask.VALUE_SNAK))
        self.assertEqual(
            Filter.SnakMask.check(('x', 'y')),
            Filter.SnakMask(Filter.SnakMask.VALUE_SNAK))
        self.assertEqual(
            Filter.SnakMask.check(SomeValueSnak('x')),
            Filter.SnakMask(Filter.SnakMask.SOME_VALUE_SNAK))
        self.assertEqual(
            Filter.SnakMask.check(SomeValueSnak),
            Filter.SnakMask(Filter.SnakMask.SOME_VALUE_SNAK))
        self.assertEqual(
            Filter.SnakMask.check(NoValueSnak('x')),
            Filter.SnakMask(Filter.SnakMask.NO_VALUE_SNAK))
        self.assertEqual(
            Filter.SnakMask.check(NoValueSnak),
            Filter.SnakMask(Filter.SnakMask.NO_VALUE_SNAK))
        self.assertEqual(
            Filter.SnakMask.check(Filter.VALUE_SNAK),
            Filter.VALUE_SNAK)
        self.assertEqual(
            Filter.SnakMask.check_optional(None, Filter.SnakMask.ALL),
            Filter.SnakMask.ALL)
        self.assertIsNone(Filter.SnakMask.check_optional(None))

    def test_match(self) -> None:
        assert_type(Filter.SnakMask(0).match(('x', 'y')), bool)
        m = Filter.SnakMask.ALL
        self.assertTrue(m.match(('x', 'y')))
        self.assertTrue(m.match(Property('x')('y')))
        self.assertTrue(m.match(SomeValueSnak('x')))
        self.assertTrue(m.match(NoValueSnak('x')))
        m = Filter.VALUE_SNAK
        self.assertTrue(m.match(('x', 'y')))
        self.assertTrue(m.match(Property('x')('y')))
        self.assertFalse(m.match(SomeValueSnak('x')))
        self.assertFalse(m.match(NoValueSnak('x')))
        m = Filter.SOME_VALUE_SNAK
        self.assertFalse(m.match(('x', 'y')))
        self.assertFalse(m.match(Property('x')('y')))
        self.assertTrue(m.match(SomeValueSnak('x')))
        self.assertFalse(m.match(NoValueSnak('x')))
        m = Filter.NO_VALUE_SNAK
        self.assertFalse(m.match(('x', 'y')))
        self.assertFalse(m.match(Property('x')('y')))
        self.assertFalse(m.match(SomeValueSnak('x')))
        self.assertTrue(m.match(NoValueSnak('x')))
        m = Filter.SOME_VALUE_SNAK | Filter.NO_VALUE_SNAK
        self.assertFalse(m.match(('x', 'y')))
        self.assertFalse(m.match(Property('x')('y')))
        self.assertTrue(m.match(SomeValueSnak('x')))
        self.assertTrue(m.match(NoValueSnak('x')))
        m = Filter.SnakMask.ALL & ~Filter.NO_VALUE_SNAK
        self.assertTrue(m.match(('x', 'y')))
        self.assertTrue(m.match(Property('x')('y')))
        self.assertTrue(m.match(SomeValueSnak('x')))
        self.assertFalse(m.match(NoValueSnak('x')))


if __name__ == '__main__':
    Test.main()
