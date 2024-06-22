# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    KIF_Object,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    String,
    StringVariable,
    TextTemplate,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_TemplateTestCase


class Test(kif_TemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(LexemeTemplate.object_class, type[Lexeme])

    def test_check(self) -> None:
        assert_type(
            LexemeTemplate.check(LexemeTemplate(Variable('x'))),
            LexemeTemplate)
        self._test_check(
            LexemeTemplate,
            success=[
                LexemeTemplate(Variable('x')),
            ],
            failure=[
                Lexeme('x'),
                LexemeTemplate('x'),
                TextTemplate(Variable('x')),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(LexemeTemplate(Variable('x')), LexemeTemplate)
        self._test__init__(
            LexemeTemplate,
            lambda x, *y: self.assert_lexeme_template(x, *y),
            success=[
                [IRI_Template(Variable('x'))],
                [IRI_Variable('x')],
                [Variable('x', IRI)],
            ],
            normalize=[
                [IRI('x')],
                [Lexeme(IRI('x'))],
                [String('x')],
            ],
            failure=[
                [Lexeme(IRI(Variable('x')))],
                [LexemeTemplate(Variable('x'))],
                [LexemeVariable('x')],
                [Item('x')],
                [TextTemplate(Variable('x'))],
            ])

    def test_instantiate(self) -> None:
        assert_type(LexemeTemplate(Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(
            LexemeTemplate,
            success=[
                (LexemeTemplate(Variable('x')),
                 Lexeme('x'),
                 {IRI_Variable('x'): IRI('x')}),
                (LexemeTemplate(Variable('x')),
                 LexemeTemplate(Variable('y')),
                 {IRI_Variable('x'): IRI_Variable('y')}),
            ],
            failure=[
                (LexemeTemplate(Variable('x')),
                 {IRI_Variable('x'): Lexeme('x')}),
                (LexemeTemplate(Variable('x')),
                 {IRI_Variable('x'): String('x')}),
                (LexemeTemplate(Variable('x')),
                 {IRI_Variable('x'): StringVariable('x')}),
            ])


if __name__ == '__main__':
    Test.main()
