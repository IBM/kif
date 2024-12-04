# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import DeprecatedRank
from kif_lib.typing import assert_type

from ....tests import RankTestCase


class Test(RankTestCase):

    def test_instance(self) -> None:
        assert_type(DeprecatedRank.instance, DeprecatedRank)
        self.assertIs(DeprecatedRank.instance, DeprecatedRank())

    def test_check(self) -> None:
        assert_type(DeprecatedRank.check(DeprecatedRank()), DeprecatedRank)
        self._test_check(DeprecatedRank)

    def test__init__(self) -> None:
        assert_type(DeprecatedRank(), DeprecatedRank)
        self._test__init__(DeprecatedRank, self.assert_deprecated_rank)


if __name__ == '__main__':
    Test.main()
