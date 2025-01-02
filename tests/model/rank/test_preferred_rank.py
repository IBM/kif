# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import PreferredRank
from kif_lib.typing import assert_type

from ...tests import RankTestCase


class Test(RankTestCase):

    def test_instance(self) -> None:
        assert_type(PreferredRank.instance, PreferredRank)
        self.assertIs(PreferredRank.instance, PreferredRank())

    def test_check(self) -> None:
        assert_type(PreferredRank.check(PreferredRank()), PreferredRank)
        self._test_check(PreferredRank)

    def test__init__(self) -> None:
        assert_type(PreferredRank(), PreferredRank)
        self._test__init__(PreferredRank, self.assert_preferred_rank)


if __name__ == '__main__':
    Test.main()
