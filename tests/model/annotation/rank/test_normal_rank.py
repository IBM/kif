# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import NormalRank
from kif_lib.typing import assert_type

from ....tests import RankTestCase


class Test(RankTestCase):

    def test_check(self) -> None:
        assert_type(NormalRank.check(NormalRank()), NormalRank)
        self._test_check(NormalRank)

    def test__init__(self) -> None:
        assert_type(NormalRank(), NormalRank)
        self._test__init__(NormalRank, self.assert_normal_rank)


if __name__ == '__main__':
    Test.main()
