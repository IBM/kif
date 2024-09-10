# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    NoValueSnak,
    Property,
    Quantity,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    Term,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import SnakVariableTestCase


class Test(SnakVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(SomeValueSnakVariable.object_class, type[SomeValueSnak])
        self.assertIs(SomeValueSnakVariable.object_class, SomeValueSnak)

    def test_check(self) -> None:
        assert_type(
            SomeValueSnakVariable.check(SomeValueSnakVariable('x')),
            SomeValueSnakVariable)
        assert_type(
            SomeValueSnakVariable.check(Variable('x', SomeValueSnak)),
            SomeValueSnakVariable)
        self._test_check(SomeValueSnakVariable)

    def test__init__(self) -> None:
        assert_type(SomeValueSnakVariable('x'), SomeValueSnakVariable)
        self._test__init__(
            SomeValueSnakVariable, self.assert_some_value_snak_variable)

    def test_variables(self) -> None:
        assert_type(SomeValueSnakVariable('x').variables, Set[Variable])
        self._test_variables(SomeValueSnakVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(SomeValueSnakVariable('x').instantiate({}), Optional[Term])
        assert_type(SomeValueSnakVariable('x').match(
            Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            SomeValueSnakVariable,
            success=[
                SomeValueSnak('x'),
                SomeValueSnak(Variable('x')),
            ],
            failure=[
                NoValueSnak('x'),
                NoValueSnak(Variable('x')),
                ValueSnak('x', 'y'),
                ValueSnak(Variable('x'), Variable('y')),
            ])


if __name__ == '__main__':
    Test.main()
