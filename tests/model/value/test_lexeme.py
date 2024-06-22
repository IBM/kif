# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Item,
    Lexeme,
    LexemeDatatype,
    Lexemes,
    LexemeTemplate,
    LexemeVariable,
    Property,
    Text,
    Variable,
)
from kif_lib.typing import assert_type, Iterable

from ...tests import kif_EntityTestCase


class Test(kif_EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Lexeme.datatype_class, type[LexemeDatatype])

    def test_datatype(self) -> None:
        assert_type(Lexeme.datatype, LexemeDatatype)
        self.assertIsInstance(Lexeme.datatype, LexemeDatatype)

    def test_template_class(self) -> None:
        assert_type(Lexeme.template_class, type[LexemeTemplate])

    def test_variable_class(self) -> None:
        assert_type(Lexeme.variable_class, type[LexemeVariable])

    def test_check(self) -> None:
        assert_type(Lexeme.check(Lexeme('x')), Lexeme)
        self._test_check(
            Lexeme,
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
                Item('x'),
                LexemeTemplate(Variable('x')),
                Property('x'),
                Text('x'),
                Variable('x', Text),
            ])

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
