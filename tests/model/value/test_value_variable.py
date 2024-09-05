# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    Item,
    Property,
    Quantity,
    Snak,
    Statement,
    String,
    Term,
    Time,
    Value,
    ValueSnak,
    ValueVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(ValueVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            ValueVariable,
            success_auto=[
                IRI.template_class(Variable('x')),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity(Variable('x')),
                String('x'),
                Time('2024-06-26'),
                Time(Variable('x')),
                Value.variable_class('x'),
            ],
            failure_auto=[
                Statement(Item('x'), ValueSnak(Property('y'), Item('z'))),
                Snak.variable_class('x'),
            ])


if __name__ == '__main__':
    Test.main()
