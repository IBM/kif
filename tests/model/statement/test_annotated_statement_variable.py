# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AnnotatedStatement,
    AnnotatedStatementVariable,
    Item,
    NoValueSnak,
    SomeValueSnak,
    Statement,
    Term,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import StatementVariableTestCase


class Test(StatementVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(
            AnnotatedStatementVariable.object_class, type[AnnotatedStatement])
        self.assertIs(
            AnnotatedStatementVariable.object_class, AnnotatedStatement)

    def test_check(self) -> None:
        assert_type(
            AnnotatedStatementVariable.check(AnnotatedStatementVariable('x')),
            AnnotatedStatementVariable)
        assert_type(
            AnnotatedStatementVariable.check(
                Variable('x', AnnotatedStatement)),
            AnnotatedStatementVariable)
        self._test_check(AnnotatedStatementVariable)

    def test__init__(self) -> None:
        assert_type(
            AnnotatedStatementVariable('x'), AnnotatedStatementVariable)
        self._test__init__(
            AnnotatedStatementVariable,
            self.assert_annotated_statement_variable)

    def test_variables(self) -> None:
        assert_type(AnnotatedStatementVariable('x').variables, Set[Variable])
        self._test_variables(AnnotatedStatementVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(
            AnnotatedStatementVariable('x').instantiate({}), Optional[Term])
        assert_type(AnnotatedStatementVariable('x').match(
            AnnotatedStatement(Item('x'), NoValueSnak('y'))), Optional[Theta])
        self._test_instantiate_and_match(
            AnnotatedStatementVariable,
            success=[
                Statement(Item('x'), ValueSnak('y', 'z')).annotate(),
                Statement(Item('x'), SomeValueSnak('y'))@{  # pyright: ignore
                    'qualifiers': Variable('z'),
                    'rank': Variable('w'),
                },
                AnnotatedStatement(Item('x'), NoValueSnak('y')),
                Statement(Variable('x'), Variable('y')).annotate(),
            ])


if __name__ == '__main__':
    Test.main()
