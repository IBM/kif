# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AliasProperty,
    IRI,
    IRI_Datatype,
    Item,
    LabelProperty,
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
        assert_type(LabelProperty.datatype_class, type[PropertyDatatype])
        self.assertIs(LabelProperty.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(LabelProperty.datatype, PropertyDatatype)
        self.assert_property_datatype(LabelProperty.datatype)

    def test_template_class(self) -> None:
        assert_type(LabelProperty.template_class, type[PropertyTemplate])
        self.assertIs(LabelProperty.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(LabelProperty.variable_class, type[PropertyVariable])
        self.assertIs(LabelProperty.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(LabelProperty.check(LabelProperty()), LabelProperty)
        self._test_check(
            LabelProperty,
            success=[
                (LabelProperty(), LabelProperty()),
                (LabelProperty.expected_iri, LabelProperty()),
                (LabelProperty.expected_iri.content, LabelProperty()),
            ],
            failure=[
                AliasProperty(),
                AliasProperty.expected_iri,
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
            f'expected {LabelProperty.expected_iri}, got {IRI("x")}',
            LabelProperty, 'x')
        self.assert_raises_bad_argument(
            ValueError, 2, None,
            f'expected {LabelProperty.expected_range}, got {IRI_Datatype()}',
            LabelProperty, None, IRI)
        self.assert_label_property(LabelProperty())
        self.assert_label_property(LabelProperty(LabelProperty.expected_iri))
        self.assert_label_property(
            LabelProperty(None, LabelProperty.expected_range))


if __name__ == '__main__':
    Test.main()
