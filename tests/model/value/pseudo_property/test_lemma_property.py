# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    IRI_Datatype,
    Item,
    LabelProperty,
    LemmaProperty,
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
            LemmaProperty.datatype_class, type[PropertyDatatype])
        self.assertIs(LemmaProperty.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(LemmaProperty.datatype, PropertyDatatype)
        self.assert_property_datatype(LemmaProperty.datatype)

    def test_template_class(self) -> None:
        assert_type(
            LemmaProperty.template_class, type[PropertyTemplate])
        self.assertIs(LemmaProperty.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(
            LemmaProperty.variable_class, type[PropertyVariable])
        self.assertIs(LemmaProperty.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(LemmaProperty.check(
            LemmaProperty()), LemmaProperty)
        self._test_check(
            LemmaProperty,
            success=[
                (LemmaProperty(), LemmaProperty()),
                (LemmaProperty.expected_iri, LemmaProperty()),
                (LemmaProperty.expected_iri.content,
                 LemmaProperty()),
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
            f'expected {LemmaProperty.expected_iri}, got {IRI("x")}',
            LemmaProperty, 'x')
        self.assert_raises_bad_argument(
            ValueError, 2, None,
            f'expected {LemmaProperty.expected_range}, '
            f'got {IRI_Datatype()}',
            LemmaProperty, None, IRI)
        self.assert_lemma_property(LemmaProperty())
        self.assert_lemma_property(
            LemmaProperty(LemmaProperty.expected_iri))
        self.assert_lemma_property(
            LemmaProperty(None, LemmaProperty.expected_range))


if __name__ == '__main__':
    Test.main()
