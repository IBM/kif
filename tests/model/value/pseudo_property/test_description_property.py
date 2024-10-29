# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DescriptionProperty,
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
        assert_type(
            DescriptionProperty.datatype_class, type[PropertyDatatype])
        self.assertIs(DescriptionProperty.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(DescriptionProperty.datatype, PropertyDatatype)
        self.assert_property_datatype(DescriptionProperty.datatype)

    def test_template_class(self) -> None:
        assert_type(
            DescriptionProperty.template_class, type[PropertyTemplate])
        self.assertIs(DescriptionProperty.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(
            DescriptionProperty.variable_class, type[PropertyVariable])
        self.assertIs(DescriptionProperty.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(DescriptionProperty.check(
            DescriptionProperty()), DescriptionProperty)
        self._test_check(
            DescriptionProperty,
            success=[
                (DescriptionProperty(), DescriptionProperty()),
                (DescriptionProperty.expected_iri, DescriptionProperty()),
                (DescriptionProperty.expected_iri.content,
                 DescriptionProperty()),
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
            f'expected {DescriptionProperty.expected_iri}, got {IRI("x")}',
            DescriptionProperty, 'x')
        self.assert_raises_bad_argument(
            ValueError, 2, None,
            f'expected {DescriptionProperty.expected_range}, '
            f'got {IRI_Datatype()}',
            DescriptionProperty, None, IRI)
        self.assert_description_property(DescriptionProperty())
        self.assert_description_property(
            DescriptionProperty(DescriptionProperty.expected_iri))
        self.assert_description_property(
            DescriptionProperty(None, DescriptionProperty.expected_range))


if __name__ == '__main__':
    Test.main()
