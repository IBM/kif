# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    EntityVariable,
    IRI,
    IRI_Variable,
    Item,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnak,
    Quantity,
    SnakVariable,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(LexemeVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            LexemeVariable,
            success_auto=[
                Lexeme('x'),
                LexemeTemplate(Variable('x')),
            ],
            failure_auto=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Item('x'),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
            ])

    def test_match(self) -> None:
        assert_type(LexemeVariable('x').match(Variable('x')), Optional[Theta])
        self._test_match(
            LexemeVariable,
            success=[
                (LexemeVariable('x'),
                 Lexeme(Variable('x')),
                 {LexemeVariable('x'): Lexeme(IRI_Variable('x'))}),
                (LexemeVariable('x'),
                 LexemeVariable('y'),
                 {LexemeVariable('x'): LexemeVariable('y')}),
                (LexemeVariable('x'),
                 EntityVariable('y'),
                 {EntityVariable('y'): LexemeVariable('x')})
            ],
            failure=[
                (LexemeVariable('x'), IRI('y')),
                (LexemeVariable('x'), SnakVariable('y')),
                (LexemeVariable('x'), NoValueSnak(Variable('y'))),
            ])


if __name__ == '__main__':
    Test.main()
