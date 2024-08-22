# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Deprecated, Item, Normal, NormalRank, Preferred, SnakSet
from kif_lib.typing import assert_type

from ....tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_check(self) -> None:
        assert_type(NormalRank.check(NormalRank()), NormalRank)
        self._test_check(
            NormalRank,
            success=[
                (Normal, NormalRank()),
                (NormalRank(), Normal),
            ],
            failure=[0, {}, Item('x'), SnakSet(), Deprecated, Preferred])

    def test__init__(self) -> None:
        assert_type(NormalRank(), NormalRank)
        self._test__init__(
            NormalRank,
            self.assert_normal_rank,
            success=[([], Normal)])


if __name__ == '__main__':
    Test.main()
