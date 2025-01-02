# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    NoValueSnak,
    NoValueSnakVariable,
    SomeValueSnak,
    Term,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import SnakVariableTestCase


class Test(SnakVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(NoValueSnakVariable.object_class, type[NoValueSnak])
        self.assertIs(NoValueSnakVariable.object_class, NoValueSnak)

    def test_check(self) -> None:
        assert_type(
            NoValueSnakVariable.check(NoValueSnakVariable('x')),
            NoValueSnakVariable)
        assert_type(
            NoValueSnakVariable.check(Variable('x', NoValueSnak)),
            NoValueSnakVariable)
        self._test_check(NoValueSnakVariable)

    def test__init__(self) -> None:
        assert_type(NoValueSnakVariable('x'), NoValueSnakVariable)
        self._test__init__(
            NoValueSnakVariable, self.assert_no_value_snak_variable)

    def test_variables(self) -> None:
        assert_type(NoValueSnakVariable('x').variables, Set[Variable])
        self._test_variables(NoValueSnakVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(NoValueSnakVariable('x').instantiate({}), Optional[Term])
        assert_type(NoValueSnakVariable('x').match(
            Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            NoValueSnakVariable,
            success=[
                NoValueSnak('x'),
                NoValueSnak(Variable('x')),
            ],
            failure=[
                SomeValueSnak('x'),
                SomeValueSnak(Variable('x')),
                ValueSnak('x', 'y'),
                ValueSnak(Variable('x'), Variable('y')),
            ])


if __name__ == '__main__':
    Test.main()
