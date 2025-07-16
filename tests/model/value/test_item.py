# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import decimal

from kif_lib import (
    Context,
    ExternalId,
    IRI,
    Item,
    ItemDatatype,
    Items,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    Property,
    Quantity,
    QuantityTemplate,
    QuantityVariable,
    Store,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import Any, assert_type, Iterator, Optional, Set

from ...tests import EntityTestCase


class Test(EntityTestCase):

    def assert_register(self, item: Item, **kwargs: Any) -> None:
        self.assertEqual(item.register(**kwargs), item)

    def assert_unregister(self, item: Item, **kwargs: Any) -> None:
        self.assertTrue(item.unregister(**kwargs))

    def test_datatype_class(self) -> None:
        assert_type(Item.datatype_class, type[ItemDatatype])
        self.assertIs(Item.datatype_class, ItemDatatype)

    def test_datatype(self) -> None:
        assert_type(Item.datatype, ItemDatatype)
        self.assert_item_datatype(Item.datatype)

    def test_template_class(self) -> None:
        assert_type(Item.template_class, type[ItemTemplate])
        self.assertIs(Item.template_class, ItemTemplate)

    def test_variable_class(self) -> None:
        assert_type(Item.variable_class, type[ItemVariable])
        self.assertIs(Item.variable_class, ItemVariable)

    def test_check(self) -> None:
        assert_type(Item.check(Item('x')), Item)
        self._test_check(
            Item,
            success=[
                ('x', Item('x')),
                (ExternalId('x'), Item('x')),
            ],
            failure=[
                ItemTemplate(Variable('x')),
                Lexeme('x'),
                Property('x'),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        assert_type(Item('x'), Item)
        self._test__init__(
            Item,
            self.assert_item,
            failure=[
                [ItemTemplate(Variable('x'))],
                [Lexeme('x')],
                [Property('x')],
                [Text('x')],
                [Variable('x', Text)],
            ])

    def test__rmatmul__(self) -> None:
        assert_type(5@Item('x'), Quantity)
        assert_type(
            QuantityTemplate(Variable('x'))@Item('x'), QuantityTemplate)
        self.assert_raises_bad_argument(
            TypeError, None, None,
            'cannot coerce dict into Quantity',
            (Item('x').__rmatmul__, 'Quantity.check'), {})
        self.assert_raises_bad_argument(
            ValueError, None, None,
            'cannot coerce str into Quantity',
            (Item('x').__rmatmul__, 'Quantity.check'), 'abc')
        self.assert_quantity(5@Item('x'), decimal.Decimal(5), Item('x'))
        self.assert_quantity(
            Quantity(5, Item('x'), 4, 6)@Item('y'),
            decimal.Decimal(5), Item('y'),
            decimal.Decimal(4), decimal.Decimal(6))
        self.assert_quantity_template(
            Quantity(Variable('x'), None, 4)@Item('y'),
            QuantityVariable('x'), Item('y'), 4)

    def test_variables(self) -> None:
        assert_type(Item('x').variables, Set[Variable])
        self._test_variables(Item)

    def test_instantiate(self) -> None:
        assert_type(Item('x').instantiate({}), Term)
        self._test_instantiate(Item)

    def test_match(self) -> None:
        assert_type(Item('x').match(Variable('x')), Optional[Theta])
        self._test_match(Item)

    def test_display(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            (Item('x').display, 'Item.get_label'), 0)
        with Context():
            assert_type(Item('x').display(), str)
            self.assertEqual(Item('x').display(), 'x')
            self.assertEqual(Item('x').display('pt'), 'x')
            self.assert_register(
                Item('x'), labels=['abc@en', Text('abc@pt', 'pt')])
            self.assertEqual(Item('x').display(), 'abc@en')
            self.assertEqual(Item('x').display('en'), 'abc@en')
            self.assertEqual(Item('x').display('pt'), 'abc@pt')
            self.assertEqual(Item('x').display('fr'), 'x')

    def test_describe(self) -> None:
        with Context():
            assert_type(Item('x').describe(), Optional[Item.Descriptor])
            self.assertIsNone(Item('x').describe())
            self.assert_register(
                Item('x'), label='abc', alias=Text('abc', 'pt'),
                descriptions=[Text('def', 'fr'), Text('def', 'jp')])
            self.assertEqual(
                Item('x').describe(),
                {'labels': {'en': Text('abc')},
                 'aliases': {'pt': {Text('abc', 'pt')}},
                 'descriptions': {
                     'fr': Text('def', 'fr'), 'jp': Text('def', 'jp')}})
        self.assertIsNone(Item('x').describe())

    def test_get_label(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            Item('x').get_label, 0)
        with Context():
            assert_type(Item('x').get_label(), Optional[Text])
            self.assertIsNone(Item('x').get_label())
            self.assert_register(Item('x'), label='abc')
            self.assertEqual(Item('x').get_label('en'), Text('abc'))
            self.assertEqual(Item('x').get_label(), Text('abc'))
            self.assertEqual(Item('x').label, Text('abc'))
        self.assertIsNone(Item('x').label)

    def test_get_aliases(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            Item('x').get_aliases, 0)
        with Context():
            assert_type(Item('x').get_aliases(), Optional[Set[Text]])
            self.assertIsNone(Item('x').get_aliases())
            self.assert_register(Item('x'), alias='abc')
            self.assert_register(Item('x'), aliases=[
                'def', Text('abc', 'pt'), Text('def', 'fr')])
            self.assertEqual(Item('x').get_aliases('en'), {
                Text('abc'), Text('def')})
            self.assertEqual(
                Item('x').get_aliases('pt'), {Text('abc', 'pt')})
            self.assertEqual(Item('x').aliases, {Text('abc'), Text('def')})
            self.assertIsNone(Item('x').get_label('jp'))
        self.assertIsNone(Item('x').label)

    def test_get_description(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            Item('x').get_description, 0)
        with Context():
            assert_type(Item('x').get_description(), Optional[Text])
            self.assertIsNone(Item('x').get_description())
            self.assert_register(Item('x'), description='abc')
            self.assertEqual(Item('x').get_description('en'), Text('abc'))
            self.assertEqual(Item('x').get_description(), Text('abc'))
            self.assertEqual(Item('x').description, Text('abc'))
        self.assertIsNone(Item('x').description)

    def test_get_resolver(self) -> None:
        with Context():
            kb1, kb2 = Store('empty'), Store('empty')
            ns1, ns2 = IRI('http://x#'), IRI('http://y#')
            i1, i2 = Item('http://x#i1'), Item('http://y#i2')
            assert_type(i1.get_resolver(), Optional[Store])
            self.assertIsNone(i1.get_resolver())
            self.assertIsNone(i2.resolver)
            ns1.register(resolver=kb1)
            ns2.register(resolver=kb2)
            self.assertEqual(i1.get_resolver(), kb1)
            self.assertEqual(i2.resolver, kb2)
            ns1.unregister()
            self.assertIsNone(i1.resolver)
            self.assertEqual(i2.resolver, kb2)
            ns2.unregister()
            self.assertIsNone(i1.resolver)
            self.assertIsNone(i2.resolver)
        self.assertIsNone(Item('x').resolver)

    def test_register(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            Item('x').register, label=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            Item('x').register, labels=['x', 0])
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            Item('x').register, alias=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            Item('x').register, aliases=['x', 0])
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            Item('x').register, description=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            Item('x').register, descriptions=['x', 0])
        with Context():
            assert_type(Item('x').register(), Item)
            self.assertEqual(Item('x').register(), Item('x'))
            self.assertIsNone(Item('x').describe())
            self.assert_register(
                Item('x'),
                label=Text('abc'),
                labels=[Text('def'), Text('abc', 'pt')],
                alias=Text('abc', 'fr'),
                aliases=[Text('abc'), Text('abc', 'fr'), Text('def')],
                description='abc',
                descriptions=[Text('abc', 'pt'), Text('def', 'en')])
            self.assertEqual(Item('x').describe(), {
                'labels': {
                    'en': Text('def'),
                    'pt': Text('abc', 'pt'),
                },
                'aliases': {
                    'en': {Text('abc'), Text('def')},
                    'fr': {Text('abc', 'fr')},
                },
                'descriptions': {
                    'en': Text('def'),
                    'pt': Text('abc', 'pt'),
                },
            })
        self.assertIsNone(Item('x').describe())

    def test_unregister(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            Item('x').unregister, label=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            Item('x').unregister, labels=['x', 0])
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            Item('x').unregister, alias=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            Item('x').unregister, aliases=['x', 0])
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            Item('x').unregister, description=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            Item('x').unregister, descriptions=['x', 0])
        with Context():
            assert_type(Item('x').unregister(), bool)
            self.assertIsNone(Item('x').describe())
            self.assert_register(
                Item('x'),
                label=Text('abc'),
                labels=[Text('def'), Text('abc', 'pt')],
                alias=Text('abc', 'fr'),
                aliases=[Text('abc'), Text('abc', 'fr'), Text('def')],
                description='abc',
                descriptions=[Text('abc', 'pt'), Text('def', 'en')])
            self.assert_unregister(
                Item('x'), label=Text('def'), alias_language='fr',
                all_descriptions=True)
            self.assertEqual(Item('x').describe(), {
                'labels': {
                    'pt': Text('abc', 'pt'),
                },
                'aliases': {
                    'en': {Text('abc'), Text('def')},
                },
            })
            self.assertTrue(Item('x').unregister())
            self.assertIsNone(Item('x').describe())
            self.assert_register(Item('x').register(description=Text('abc')))
            self.assertFalse(Item('x').unregister(description_language='pt'))
        self.assertIsNone(Item('x').describe())

    def test_Items(self) -> None:
        assert_type(Items('a', 'b', 'c'), Iterator[Item])
        self._test_Entities(
            Items,
            self.assert_item,
            failure=[
                Item('x'),
                ItemTemplate(Variable('x')),
                Lexeme('x'),
                Property('x'),
                Text('x'),
                Variable('x', Text),
            ])


if __name__ == '__main__':
    Test.main()
