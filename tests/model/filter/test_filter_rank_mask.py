# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import DeprecatedRank, Filter, NormalRank, PreferredRank, Rank
from kif_lib.typing import assert_type

from ...tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_check(self) -> None:
        assert_type(Filter.RankMask.check(Rank), Filter.RankMask)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Filter.RankMask.check, 'abc')
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Filter.RankMask.check, 8)
        self.assertEqual(Filter.RankMask.check(0), Filter.RankMask(0))
        self.assertEqual(
            Filter.RankMask.check(Rank), Filter.RankMask(Filter.RankMask.ALL))
        self.assertEqual(
            Filter.RankMask.check(PreferredRank),
            Filter.RankMask(Filter.RankMask.PREFERRED))
        self.assertEqual(
            Filter.RankMask.check(PreferredRank()),
            Filter.RankMask(Filter.RankMask.PREFERRED))
        self.assertEqual(
            Filter.RankMask.check(NormalRank),
            Filter.RankMask(Filter.RankMask.NORMAL))
        self.assertEqual(
            Filter.RankMask.check(NormalRank()),
            Filter.RankMask(Filter.RankMask.NORMAL))
        self.assertEqual(
            Filter.RankMask.check(DeprecatedRank),
            Filter.RankMask(Filter.RankMask.DEPRECATED))
        self.assertEqual(
            Filter.RankMask.check(DeprecatedRank()),
            Filter.RankMask(Filter.RankMask.DEPRECATED))
        self.assertEqual(
            Filter.RankMask.check_optional(None, Filter.RankMask.ALL),
            Filter.RankMask.ALL)
        self.assertIsNone(Filter.RankMask.check_optional(None))

    def test_match(self) -> None:
        assert_type(Filter.RankMask(0).match(NormalRank()), bool)
        m = Filter.RankMask.ALL
        self.assertTrue(m.match(PreferredRank))
        self.assertTrue(m.match(PreferredRank()))
        self.assertTrue(m.match(NormalRank))
        self.assertTrue(m.match(NormalRank()))
        self.assertTrue(m.match(DeprecatedRank))
        self.assertTrue(m.match(DeprecatedRank()))
        m = Filter.PREFERRED
        self.assertTrue(m.match(PreferredRank))
        self.assertTrue(m.match(PreferredRank()))
        self.assertFalse(m.match(NormalRank))
        self.assertFalse(m.match(NormalRank()))
        self.assertFalse(m.match(DeprecatedRank))
        self.assertFalse(m.match(DeprecatedRank()))
        m = Filter.NORMAL
        self.assertFalse(m.match(PreferredRank))
        self.assertFalse(m.match(PreferredRank()))
        self.assertTrue(m.match(NormalRank))
        self.assertTrue(m.match(NormalRank()))
        self.assertFalse(m.match(DeprecatedRank))
        self.assertFalse(m.match(DeprecatedRank()))
        m = Filter.DEPRECATED
        self.assertFalse(m.match(PreferredRank))
        self.assertFalse(m.match(PreferredRank()))
        self.assertFalse(m.match(NormalRank))
        self.assertFalse(m.match(NormalRank()))
        self.assertTrue(m.match(DeprecatedRank))
        self.assertTrue(m.match(DeprecatedRank()))
        m = Filter.RankMask.ALL & ~Filter.DEPRECATED
        self.assertTrue(m.match(PreferredRank))
        self.assertTrue(m.match(PreferredRank()))
        self.assertTrue(m.match(NormalRank))
        self.assertTrue(m.match(NormalRank()))
        self.assertFalse(m.match(DeprecatedRank))
        self.assertFalse(m.match(DeprecatedRank()))


if __name__ == '__main__':
    Test.main()
