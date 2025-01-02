# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    Item,
    Lexeme,
    LexemeDatatype,
    Lexemes,
    LexemeTemplate,
    LexemeVariable,
    Property,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Iterable, Optional, Set

from ...tests import EntityTestCase


class Test(EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Lexeme.datatype_class, type[LexemeDatatype])
        self.assertIs(Lexeme.datatype_class, LexemeDatatype)

    def test_datatype(self) -> None:
        assert_type(Lexeme.datatype, LexemeDatatype)
        self.assert_lexeme_datatype(Lexeme.datatype)

    def test_template_class(self) -> None:
        assert_type(Lexeme.template_class, type[LexemeTemplate])
        self.assertIs(Lexeme.template_class, LexemeTemplate)

    def test_variable_class(self) -> None:
        assert_type(Lexeme.variable_class, type[LexemeVariable])
        self.assertIs(Lexeme.variable_class, LexemeVariable)

    def test_check(self) -> None:
        assert_type(Lexeme.check(Lexeme('x')), Lexeme)
        self._test_check(
            Lexeme,
            success=[
                ('x', Lexeme('x')),
                (ExternalId('x'), Lexeme('x')),
            ],
            failure=[
                Item('x'),
                LexemeTemplate(Variable('x')),
                Property('x'),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        assert_type(Lexeme('x'), Lexeme)
        self._test__init__(
            Lexeme,
            self.assert_lexeme,
            failure=[
                [Item('x')],
                [LexemeTemplate(Variable('x'))],
                [Property('x')],
                [Text('x')],
                [Variable('x', Text)],
            ])

    def test_variables(self) -> None:
        assert_type(Lexeme('x').variables, Set[Variable])
        self._test_variables(Lexeme)

    def test_instantiate(self) -> None:
        assert_type(Lexeme('x').instantiate({}), Term)
        self._test_instantiate(Lexeme)

    def test_match(self) -> None:
        assert_type(Lexeme('x').match(Variable('x')), Optional[Theta])
        self._test_match(Lexeme)

    def test_Lexemes(self) -> None:
        assert_type(Lexemes('a', 'b', 'c'), Iterable[Lexeme])
        self._test_Entities(
            Lexemes,
            self.assert_lexeme,
            failure=[
                Item('x'),
                Lexeme('x'),
                LexemeTemplate(Variable('x')),
                Property('x'),
                Text('x'),
                Variable('x', Text),
            ])


if __name__ == '__main__':
    Test.main()
