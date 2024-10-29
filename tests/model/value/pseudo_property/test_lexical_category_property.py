# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    IRI_Datatype,
    Item,
    LabelProperty,
    Lexeme,
    LexicalCategoryProperty,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    Text,
    Variable,
)
from kif_lib.typing import assert_type

from ....tests import EntityTestCase


class Test(EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(
            LexicalCategoryProperty.datatype_class, type[PropertyDatatype])
        self.assertIs(LexicalCategoryProperty.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(LexicalCategoryProperty.datatype, PropertyDatatype)
        self.assert_property_datatype(LexicalCategoryProperty.datatype)

    def test_template_class(self) -> None:
        assert_type(
            LexicalCategoryProperty.template_class, type[PropertyTemplate])
        self.assertIs(LexicalCategoryProperty.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(
            LexicalCategoryProperty.variable_class, type[PropertyVariable])
        self.assertIs(LexicalCategoryProperty.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(LexicalCategoryProperty.check(
            LexicalCategoryProperty()), LexicalCategoryProperty)
        self._test_check(
            LexicalCategoryProperty,
            success=[
                (LexicalCategoryProperty(), LexicalCategoryProperty()),
                (LexicalCategoryProperty.expected_iri,
                 LexicalCategoryProperty()),
                (LexicalCategoryProperty.expected_iri.content,
                 LexicalCategoryProperty()),
            ],
            failure=[
                LabelProperty(),
                LabelProperty.expected_iri,
                Item('x'),
                Lexeme('x'),
                Property('x'),
                PropertyTemplate(Variable('x')),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        self.assert_raises_bad_argument(
            ValueError, 1, None,
            f'expected {LexicalCategoryProperty.expected_iri}, got {IRI("x")}',
            LexicalCategoryProperty, 'x')
        self.assert_raises_bad_argument(
            ValueError, 2, None,
            f'expected {LexicalCategoryProperty.expected_range}, '
            f'got {IRI_Datatype()}',
            LexicalCategoryProperty, None, IRI)
        self.assert_lexical_category_property(LexicalCategoryProperty())
        self.assert_lexical_category_property(
            LexicalCategoryProperty(LexicalCategoryProperty.expected_iri))
        self.assert_lexical_category_property(
            LexicalCategoryProperty(
                None, LexicalCategoryProperty.expected_range))


if __name__ == '__main__':
    Test.main()
