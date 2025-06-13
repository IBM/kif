# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    IRI,
    Item,
    Property,
    Quantity,
    String,
    Time,
    Value,
    ValuePair,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import ClosedTermPairTestCase


class Test(ClosedTermPairTestCase):

    def test_children_class(self) -> None:
        assert_type(ValuePair.left_class, type[Value])
        self.assertIs(ValuePair.left_class, Value)
        assert_type(ValuePair.right_class, type[Value])
        self.assertIs(ValuePair.right_class, Value)

    def test_check(self) -> None:
        assert_type(
            ValuePair[Quantity, Quantity].check([0, 1]),
            ValuePair[Quantity, Quantity])
        super()._test_check(
            ValuePair,
            success=[
                (ValuePair(Quantity(0), Quantity(1)),
                 ValuePair(Quantity(0), Quantity(1))),
                ([Quantity(0), String('x')],
                 ValuePair(Quantity(0), String('x'))),
                ((Item('x'), datetime.datetime(
                    2025, 6, 13, tzinfo=datetime.timezone.utc)),
                 ValuePair(Item('x'), Time('2025-06-13'))),
            ],
            failure=[
                0,
                [0],
                [Quantity(0)],
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                Variable('x'),
            ])


if __name__ == '__main__':
    Test.main()
