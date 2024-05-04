# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    Variable,
    Variables,
)
from kif_lib.model import (
    ExternalIdTemplate,
    IRI_Template,
    ItemTemplate,
    LexemeTemplate,
    PropertyTemplate,
    StringTemplate,
    Template,
    TextTemplate,
)

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test__check_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._check_arg_template_class, 0)
        self.assertRaises(
            TypeError, Template._check_arg_template_class, int)
        self.assertRaises(
            ValueError, Template._check_arg_template_class, KIF_Object)
        self.assertIs(
            Template._check_arg_template_class(Template), Template)
        self.assertIs(
            Template._check_arg_template_class(ItemTemplate), ItemTemplate)
        self.assertIs(
            Template._check_arg_template_class(Item), ItemTemplate)

    def test__check_optional_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._check_optional_arg_template_class, 0)
        self.assertIsNone(
            Template._check_optional_arg_template_class(None))
        self.assertIs(
            Template._check_optional_arg_template_class(None, Template),
            Template)
        self.assertIs(
            Template._check_optional_arg_template_class(
                Item, PropertyTemplate), ItemTemplate)

    def test__preprocess_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._preprocess_arg_template_class, 0, 1)
        self.assertRaises(
            TypeError, Template._preprocess_arg_template_class, int, 1)
        self.assertIs(
            Template._preprocess_arg_template_class(ItemTemplate, 1),
            ItemTemplate)
        self.assertIs(
            Template._preprocess_arg_template_class(Item, 1),
            ItemTemplate)

    def test__preprocess_optional_arg_template_class(self):
        self.assertRaises(
            TypeError,
            Template._preprocess_optional_arg_template_class, 0, 1)
        self.assertRaises(
            TypeError,
            Template._preprocess_optional_arg_template_class, int, 1)
        self.assertIsNone(
            Template._preprocess_optional_arg_template_class(None, 1))
        self.assertEqual(
            Template._preprocess_optional_arg_template_class(
                None, 1, ItemTemplate), ItemTemplate)
        self.assertEqual(
            Template._preprocess_optional_arg_template_class(
                Item, 1, PropertyTemplate), ItemTemplate)

    def test___new__(self):
        w, x, y, z = Variables('w', 'x', 'y', 'z')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or String or URIRef or str, got int',
            (ItemTemplate, 'Item'), 0)
        self.assert_item_template(ItemTemplate(x), Variable('x', IRI))
        self.assert_item_template(Item(x), Variable('x', IRI))
        self.assert_item_template(ItemTemplate(IRI(x)), IRI(x))
        self.assert_item_template(Item(IRI(x)), IRI(x))
        self.assert_item(ItemTemplate(IRI('x')), IRI('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or String or URIRef or str, got int',
            (PropertyTemplate, 'Property'), 0)
        self.assert_property_template(PropertyTemplate(x), Variable('x', IRI))
        self.assert_property_template(Property(x), Variable('x', IRI))
        self.assert_property_template(PropertyTemplate(IRI(x)), IRI(x))
        self.assert_property_template(Property(IRI(x)), IRI(x))
        self.assert_property(PropertyTemplate(IRI('x')), IRI('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or String or URIRef or str, got int',
            (LexemeTemplate, 'Lexeme'), 0)
        self.assert_lexeme_template(LexemeTemplate(x), Variable('x', IRI))
        self.assert_lexeme_template(Lexeme(x), Variable('x', IRI))
        self.assert_lexeme_template(LexemeTemplate(IRI(x)), IRI(x))
        self.assert_lexeme_template(Lexeme(IRI(x)), IRI(x))
        self.assert_lexeme(LexemeTemplate(IRI('x')), IRI('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (IRI_Template, 'IRI'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (TextTemplate, 'Text'), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'expected str, got int',
            (TextTemplate, 'Text'), 'x', 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (StringTemplate, 'String'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (ExternalIdTemplate, 'ExternalId'), 0)

    def test__init__(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce ItemVariable into IRI_Variable',
            ItemTemplate, Variable('x', Item))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI_Template, got ItemTemplate',
            ItemTemplate, ItemTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce PropertyVariable into IRI_Variable',
            PropertyTemplate, Variable('x', Property))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI_Template, got PropertyTemplate',
            PropertyTemplate, PropertyTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce LexemeVariable into IRI_Variable',
            LexemeTemplate, Variable('x', Lexeme))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI_Template, got LexemeTemplate',
            LexemeTemplate, LexemeTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI_Variable into StringVariable',
            IRI_Template, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected StringTemplate, got IRI_Template',
            IRI_Template, IRI_Template(Variable('x')))


if __name__ == '__main__':
    Test.main()
