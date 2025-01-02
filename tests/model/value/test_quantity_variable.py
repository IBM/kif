# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Quantity, QuantityVariable, Term, Theta, Time, Variable
from kif_lib.typing import assert_type, Optional, Set

from ...tests import DeepDataValueVariableTestCase


class Test(DeepDataValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(QuantityVariable.object_class, type[Quantity])
        self.assertIs(QuantityVariable.object_class, Quantity)

    def test_check(self) -> None:
        assert_type(
            QuantityVariable.check(QuantityVariable('x')), QuantityVariable)
        assert_type(
            QuantityVariable.check(Variable('x', Quantity)), QuantityVariable)
        self._test_check(QuantityVariable)

    def test__init__(self) -> None:
        assert_type(QuantityVariable('x'), QuantityVariable)
        self._test__init__(QuantityVariable, self.assert_quantity_variable)

    def test_variables(self) -> None:
        assert_type(QuantityVariable('x').variables, Set[Variable])
        self._test_variables(QuantityVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(QuantityVariable('x').instantiate({}), Optional[Term])
        assert_type(QuantityVariable('x').match(
            Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            QuantityVariable,
            success=[
                Quantity(0),
                Quantity(0, None, None, Variable('x')),
                Quantity(0, None, Variable('x')),
                Quantity(0, Variable('x')),
                Quantity(0, Variable('x'), Variable('y')),
                Quantity(0, Variable('x'), None, Variable('y')),
            ],
            failure=[
                Time('2024-09-10'),
                Time(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
