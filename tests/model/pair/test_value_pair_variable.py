# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    Property,
    Quantity,
    ReferenceRecordSet,
    Term,
    Theta,
    ValuePair,
    ValuePairVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(ValuePairVariable.object_class, type[ValuePair])
        self.assertIs(ValuePairVariable.object_class, ValuePair)

    def test_check(self) -> None:
        assert_type(
            ValuePairVariable.check(ValuePairVariable('x')),
            ValuePairVariable)
        assert_type(
            ValuePairVariable.check(Variable('x', ValuePair)),
            ValuePairVariable)
        self._test_check(ValuePairVariable)

    def test__init__(self) -> None:
        assert_type(ValuePairVariable('x'), ValuePairVariable)
        self._test__init__(
            ValuePairVariable, self.assert_value_pair_variable)

    def test_variables(self) -> None:
        assert_type(ValuePairVariable('x').variables, Set[Variable])
        self._test_variables(ValuePairVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(ValuePairVariable('x').instantiate({}), Optional[Term])
        assert_type(ValuePairVariable('x').match(
            ValuePair(Quantity(0), Quantity(0))), Optional[Theta])
        self._test_instantiate_and_match(
            ValuePairVariable,
            success=[
                ValuePair(Quantity(0), Quantity(0)),
                ValuePair(Quantity(0), Item('x')),
                ValuePairVariable('x'),
                ValuePair(Property('x'), Quantity(0)),
                ValuePair(Property('x'), Property('y')),
            ],
            failure=[
                Item('x'),
                Property('x')(Item('y')),
                Property('x').some_value(),
                ReferenceRecordSet(),
            ])


if __name__ == '__main__':
    Test.main()
