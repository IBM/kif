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
        assert_type(AliasProperty.datatype_class, type[PropertyDatatype])
        self.assertIs(AliasProperty.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(AliasProperty.datatype, PropertyDatatype)
        self.assert_property_datatype(AliasProperty.datatype)

    def test_template_class(self) -> None:
        assert_type(AliasProperty.template_class, type[PropertyTemplate])
        self.assertIs(AliasProperty.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(AliasProperty.variable_class, type[PropertyVariable])
        self.assertIs(AliasProperty.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(AliasProperty.check(AliasProperty()), AliasProperty)
        self._test_check(
            AliasProperty,
            success=[
                (AliasProperty(), AliasProperty()),
                (AliasProperty.expected_iri, AliasProperty()),
                (AliasProperty.expected_iri.content, AliasProperty()),
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
            f'expected {AliasProperty.expected_iri}, got {IRI("x")}',
            AliasProperty, 'x')
        self.assert_raises_bad_argument(
            ValueError, 2, None,
            f'expected {AliasProperty.expected_range}, got {IRI_Datatype()}',
            AliasProperty, None, IRI)
        self.assert_alias_property(AliasProperty())
        self.assert_alias_property(AliasProperty(AliasProperty.expected_iri))
        self.assert_alias_property(
            AliasProperty(None, AliasProperty.expected_range))


if __name__ == '__main__':
    Test.main()
