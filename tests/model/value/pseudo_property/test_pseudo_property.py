# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AliasProperty,
    DescriptionProperty,
    IRI,
    Item,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexicalCategoryProperty,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    PseudoProperty,
    Text,
    Variable,
)
from kif_lib.namespace import DCT, RDFS, SCHEMA, SKOS, WIKIBASE
from kif_lib.typing import assert_type

from ....tests import EntityTestCase


class Test(EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(PseudoProperty.datatype_class, type[PropertyDatatype])
        self.assertIs(PseudoProperty.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(PseudoProperty.datatype, PropertyDatatype)
        self.assert_property_datatype(PseudoProperty.datatype)

    def test_template_class(self) -> None:
        assert_type(PseudoProperty.template_class, type[PropertyTemplate])
        self.assertIs(PseudoProperty.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(PseudoProperty.variable_class, type[PropertyVariable])
        self.assertIs(PseudoProperty.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(PseudoProperty.check(LabelProperty()), PseudoProperty)
        self._test_check(
            PseudoProperty,
            success=[
                # label
                (LabelProperty(), LabelProperty()),
                (IRI(RDFS.label), LabelProperty()),
                (RDFS.label, LabelProperty()),
                # alias
                (AliasProperty(), AliasProperty()),
                (IRI(SKOS.altLabel), AliasProperty()),
                (SKOS.altLabel, AliasProperty()),
                # description
                (DescriptionProperty(), DescriptionProperty()),
                (IRI(SCHEMA.description), DescriptionProperty()),
                (SCHEMA.description, DescriptionProperty()),
                # lemma
                (LemmaProperty(), LemmaProperty()),
                (IRI(WIKIBASE.lemma), LemmaProperty()),
                (WIKIBASE.lemma, LemmaProperty()),
                # lexical category
                (LexicalCategoryProperty(), LexicalCategoryProperty()),
                (IRI(WIKIBASE.lexicalCategory), LexicalCategoryProperty()),
                (WIKIBASE.lexicalCategory, LexicalCategoryProperty()),
                # language
                (LanguageProperty(), LanguageProperty()),
                (IRI(DCT.language), LanguageProperty()),
                (DCT.language, LanguageProperty()),
            ],
            failure=[
                Item('x'),
                Lexeme('x'),
                Property('x'),
                PropertyTemplate(Variable('x')),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        self.assert_abstract_class(PseudoProperty)


if __name__ == '__main__':
    Test.main()
