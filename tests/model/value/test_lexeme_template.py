# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    Lexeme,
    LexemeTemplate,
    Property,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import EntityTemplateTestCase


class Test(EntityTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(LexemeTemplate.object_class, type[Lexeme])
        self.assertIs(LexemeTemplate.object_class, Lexeme)

    def test_check(self) -> None:
        assert_type(
            LexemeTemplate.check(LexemeTemplate(Variable('x'))),
            LexemeTemplate)
        self._test_check(LexemeTemplate)

    def test__init__(self) -> None:
        assert_type(LexemeTemplate(Variable('x')), LexemeTemplate)
        self._test__init__(
            LexemeTemplate,
            self.assert_lexeme_template,
            failure=[
                [Item('x')],
                [Property('x')],
            ])

    def test_variables(self) -> None:
        assert_type(LexemeTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(LexemeTemplate)

    def test_instantiate(self) -> None:
        assert_type(LexemeTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(LexemeTemplate)

    def test_match(self) -> None:
        assert_type(
            LexemeTemplate(Variable('x')).match(Lexeme('x')), Optional[Theta])
        self._test_match(LexemeTemplate)

    def test_unify(self) -> None:
        assert_type(
            LexemeTemplate(Variable('x')).unify(Variable('x')),
            Optional[Theta])
        self._test_unify(LexemeTemplate)


if __name__ == '__main__':
    Test.main()
