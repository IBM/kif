# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Item,
    KIF_Object,
    Lexeme,
    LexemeTemplate,
    Property,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_EntityTemplateTestCase


class Test(kif_EntityTemplateTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(LexemeTemplate(Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(LexemeTemplate)


if __name__ == '__main__':
    Test.main()
