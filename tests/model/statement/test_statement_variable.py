# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    NoValueSnak,
    SomeValueSnak,
    Statement,
    StatementVariable,
    Term,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import StatementVariableTestCase


class Test(StatementVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(StatementVariable.object_class, type[Statement])
        self.assertIs(StatementVariable.object_class, Statement)

    def test_check(self) -> None:
        assert_type(
            StatementVariable.check(StatementVariable('x')),
            StatementVariable)
        assert_type(
            StatementVariable.check(Variable('x', Statement)),
            StatementVariable)
        self._test_check(StatementVariable)

    def test__init__(self) -> None:
        assert_type(StatementVariable('x'), StatementVariable)
        self._test__init__(StatementVariable, self.assert_statement_variable)

    def test_variables(self) -> None:
        assert_type(StatementVariable('x').variables, Set[Variable])
        self._test_variables(StatementVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(StatementVariable('x').instantiate({}), Optional[Term])
        assert_type(StatementVariable('x').match(
            Statement(Item('x'), NoValueSnak('y'))), Optional[Theta])
        self._test_instantiate_and_match(
            StatementVariable,
            success=[
                Statement(Item('x'), ValueSnak('y', 'z')),
                Statement(Item('x'), SomeValueSnak('y')),
                Statement(Item('x'), NoValueSnak('y')),
                Statement(Variable('x'), Variable('y')),
            ])


if __name__ == '__main__':
    Test.main()
