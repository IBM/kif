# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Deprecated, Item, Normal, Preferred, PreferredRank, SnakSet
from kif_lib.typing import assert_type

from ....tests import ObjectTestCase


class Test(ObjectTestCase):

    def test_check(self) -> None:
        assert_type(PreferredRank.check(PreferredRank()), PreferredRank)
        self._test_check(
            PreferredRank,
            success=[
                (Preferred, PreferredRank()),
                (PreferredRank(), Preferred),
            ],
            failure=[0, {}, Item('x'), SnakSet(), Deprecated, Normal])

    def test__init__(self) -> None:
        assert_type(PreferredRank(), PreferredRank)
        self._test__init__(
            PreferredRank,
            self.assert_preferred_rank,
            success=[([], Preferred)])


if __name__ == '__main__':
    Test.main()
