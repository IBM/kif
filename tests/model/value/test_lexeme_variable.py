# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    Property,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import EntityVariableTestCase


class Test(EntityVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(LexemeVariable.object_class, type[Lexeme])
        self.assertIs(LexemeVariable.object_class, Lexeme)

    def test_check(self) -> None:
        assert_type(
            LexemeVariable.check(LexemeVariable('x')), LexemeVariable)
        assert_type(
            LexemeVariable.check(Variable('x', Lexeme)), LexemeVariable)
        self._test_check(LexemeVariable)

    def test__init__(self) -> None:
        assert_type(LexemeVariable('x'), LexemeVariable)
        self._test__init__(LexemeVariable, self.assert_lexeme_variable)

    def test_variables(self) -> None:
        assert_type(LexemeVariable('x').variables, Set[Variable])
        self._test_variables(LexemeVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(LexemeVariable('x').instantiate({}), Optional[Term])
        assert_type(LexemeVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            LexemeVariable,
            success=[
                Lexeme('x'),
                LexemeTemplate(Variable('x')),
            ],
            failure=[
                Item('x'),
                Item(Variable('x')),
                Property('x'),
                Property(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
