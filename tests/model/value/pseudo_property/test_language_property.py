# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    IRI_Datatype,
    Item,
    LabelProperty,
    LanguageProperty,
    Lexeme,
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
            LanguageProperty.datatype_class, type[PropertyDatatype])
        self.assertIs(LanguageProperty.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(LanguageProperty.datatype, PropertyDatatype)
        self.assert_property_datatype(LanguageProperty.datatype)

    def test_template_class(self) -> None:
        assert_type(
            LanguageProperty.template_class, type[PropertyTemplate])
        self.assertIs(LanguageProperty.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(
            LanguageProperty.variable_class, type[PropertyVariable])
        self.assertIs(LanguageProperty.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(LanguageProperty.check(
            LanguageProperty()), LanguageProperty)
        self._test_check(
            LanguageProperty,
            success=[
                (LanguageProperty(), LanguageProperty()),
                (LanguageProperty.expected_iri, LanguageProperty()),
                (LanguageProperty.expected_iri.content,
                 LanguageProperty()),
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
            f'expected {LanguageProperty.expected_iri}, got {IRI("x")}',
            LanguageProperty, 'x')
        self.assert_raises_bad_argument(
            ValueError, 2, None,
            f'expected {LanguageProperty.expected_range}, '
            f'got {IRI_Datatype()}',
            LanguageProperty, None, IRI)
        self.assert_language_property(LanguageProperty())
        self.assert_language_property(
            LanguageProperty(LanguageProperty.expected_iri))
        self.assert_language_property(
            LanguageProperty(None, LanguageProperty.expected_range))


if __name__ == '__main__':
    Test.main()
