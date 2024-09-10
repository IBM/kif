# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Quantity, Term, Theta, Time, TimeVariable, Variable
from kif_lib.typing import assert_type, Optional, Set

from ...tests import DeepDataValueVariableTestCase


class Test(DeepDataValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(TimeVariable.object_class, type[Time])
        self.assertIs(TimeVariable.object_class, Time)

    def test_check(self) -> None:
        assert_type(TimeVariable.check(TimeVariable('x')), TimeVariable)
        assert_type(TimeVariable.check(Variable('x', Time)), TimeVariable)
        self._test_check(TimeVariable)

    def test__init__(self) -> None:
        assert_type(TimeVariable('x'), TimeVariable)
        self._test__init__(TimeVariable, self.assert_time_variable)

    def test_variables(self) -> None:
        assert_type(TimeVariable('x').variables, Set[Variable])
        self._test_variables(TimeVariable)

    def test_instantiate(self) -> None:
        assert_type(TimeVariable('2024-06-26').instantiate({}), Optional[Term])
        assert_type(TimeVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            TimeVariable,
            success=[
                Time('2024-06-26'),
                Time('2024-06-26', None, None, Variable('x')),
                Time(Variable('x'), None, Variable('y')),
                Time(Variable('y'), Variable('x')),
            ],
            failure=[
                Quantity(0),
                Quantity(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
