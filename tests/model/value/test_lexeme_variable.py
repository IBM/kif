# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    Quantity,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(LexemeVariable('x').instantiate({}), Optional[KIF_Object])
        self._test_instantiate(
            LexemeVariable,
            success=[
                Lexeme('x'),
                LexemeTemplate(Variable('x')),
            ],
            failure=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Item('x'),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
