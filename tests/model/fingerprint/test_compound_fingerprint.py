# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Item, NoValueSnak, String, Variable
from kif_lib.model import (
    AndFingerprint,
    CompoundFingerprint,
    ConverseSnakFingerprint,
    EmptyFingerprint,
    FullFingerprint,
    OrFingerprint,
    ValueFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import FingerprintTestCase


class Test(FingerprintTestCase):

    def test_check(self) -> None:
        assert_type(
            CompoundFingerprint.check(AndFingerprint(Item('x'))),
            CompoundFingerprint)
        super()._test_check(
            CompoundFingerprint,
            success=[
                (AndFingerprint('x', 'y'),
                 AndFingerprint(String('x'), String('y'))),
                (OrFingerprint('x', 'y'),
                 OrFingerprint(String('x'), String('y'))),
            ],
            failure=[
                ConverseSnakFingerprint(NoValueSnak('x')),
                EmptyFingerprint(),
                FullFingerprint(),
                Item(Variable('x')),
                ValueFingerprint(Item('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        self.assert_abstract_class(CompoundFingerprint)


if __name__ == '__main__':
    Test.main()
