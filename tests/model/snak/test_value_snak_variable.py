# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    NoValueSnak,
    SomeValueSnak,
    Term,
    Theta,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import SnakVariableTestCase


class Test(SnakVariableTestCase):

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

    def test_instantiate_and_match(self) -> None:
        assert_type(ValueSnakVariable('x').instantiate({}), Optional[Term])
        assert_type(ValueSnakVariable('x').match(
            Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            ValueSnakVariable,
            success=[
                ValueSnak('x', 'y'),
                ValueSnakTemplate(Variable('x'), Variable('y')),
            ],
            failure=[
                NoValueSnak('x'),
                NoValueSnak(Variable('x')),
                SomeValueSnak('x'),
                SomeValueSnak(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
