# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    Item,
    Quantity,
    String,
    Term,
    Theta,
    Time,
    Value,
    ValueVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ValueVariableTestCase


class Test(ValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(ValueVariable.object_class, type[Value])
        self.assertIs(ValueVariable.object_class, Value)

    def test_check(self) -> None:
        assert_type(ValueVariable.check(ValueVariable('x')), ValueVariable)
        assert_type(ValueVariable.check(Variable('x', Value)), ValueVariable)
        self._test_check(ValueVariable)

    def test__init__(self) -> None:
        assert_type(ValueVariable('x'), ValueVariable)
        self._test__init__(ValueVariable, self.assert_value_variable)

    def test_variables(self) -> None:
        assert_type(ValueVariable('x').variables, Set[Variable])
        self._test_variables(ValueVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(ValueVariable('x').instantiate({}), Optional[Term])
        assert_type(ValueVariable('x').match(Item('x')), Optional[Theta])
        self._test_instantiate_and_match(
            ValueVariable,
            success=[
                IRI(Variable('x')),
                Item(Variable('x')),
                Quantity(0),
                Quantity(Variable('x')),
                String('x'),
                Time('2024-06-26'),
                Time(Variable('x')),
                ValueVariable('y'),
            ])


if __name__ == '__main__':
    Test.main()
