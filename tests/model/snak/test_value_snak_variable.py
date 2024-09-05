# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    Property,
    Quantity,
    Term,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(ValueSnakVariable.object_class, type[ValueSnak])
        self.assertIs(ValueSnakVariable.object_class, ValueSnak)

    def test_check(self) -> None:
        assert_type(
            ValueSnakVariable.check(ValueSnakVariable('x')),
            ValueSnakVariable)
        assert_type(
            ValueSnakVariable.check(Variable('x', ValueSnak)),
            ValueSnakVariable)
        self._test_check(ValueSnakVariable)

    def test__init__(self) -> None:
        assert_type(ValueSnakVariable('x'), ValueSnakVariable)
        self._test__init__(ValueSnakVariable, self.assert_value_snak_variable)

    def test_variables(self) -> None:
        assert_type(ValueSnakVariable('x').variables, Set[Variable])
        self._test_variables(ValueSnakVariable)

    def test_instantiate(self) -> None:
        assert_type(
            ValueSnakVariable('x').instantiate({}),
            Optional[Term])
        self._test_instantiate(
            ValueSnakVariable,
            success_auto=[
                ValueSnak('x', 'y'),
                ValueSnakTemplate(Variable('x'), Variable('y')),
            ],
            failure_auto=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Property('x'),
                Property.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
