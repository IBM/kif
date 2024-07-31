# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, Quantity, String, ValueSnak, Variable
from kif_lib.model import (
    AtomicFingerprint,
    EmptyFingerprint,
    FullFingerprint,
    OrFingerprint,
    SnakFingerprint,
    ValueFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import kif_FingerprintTestCase


class Test(kif_FingerprintTestCase):

    def test_check(self) -> None:
        assert_type(AtomicFingerprint.check(Item('x')), AtomicFingerprint)
        super()._test_check(
            AtomicFingerprint,
            success=[
                (('x', 'y'), SnakFingerprint(ValueSnak('x', 'y'))),
                (ValueFingerprint(Item('x')), ValueFingerprint(Item('x'))),
                ('x', ValueFingerprint(String('x'))),
                (0, ValueFingerprint(Quantity(0))),
                (None, FullFingerprint()),
                (True, FullFingerprint()),
                (False, EmptyFingerprint()),
            ],
            failure=[
                Item(Variable('x')),
                OrFingerprint(),
                Variable('x'),
                {},
            ])

    def test__init__(self):
        self.assert_abstract_class(AtomicFingerprint)


if __name__ == '__main__':
    Test.main()
