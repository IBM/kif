# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Deprecated,
    DeprecatedRank,
    Item,
    Normal,
    Preferred,
    SnakSet,
)
from kif_lib.typing import assert_type

from ....tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_check(self) -> None:
        assert_type(DeprecatedRank.check(DeprecatedRank()), DeprecatedRank)
        self._test_check(
            DeprecatedRank,
            success=[
                (Deprecated, DeprecatedRank()),
                (DeprecatedRank(), Deprecated),
            ],
            failure=[0, {}, Item('x'), SnakSet(), Normal, Preferred])

    def test__init__(self) -> None:
        assert_type(DeprecatedRank(), DeprecatedRank)
        self._test__init__(
            DeprecatedRank,
            self.assert_deprecated_rank,
            success=[([], Deprecated)])


if __name__ == '__main__':
    Test.main()
