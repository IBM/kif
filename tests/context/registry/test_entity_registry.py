# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Entity,
    IRI,
    Item,
    ItemDatatype,
    KIF_Object,
    Lexeme,
    Property,
    String,
    StringDatatype,
    Text,
)
from kif_lib.context.registry import EntityRegistry, Registry
from kif_lib.typing import Any, assert_type

from ...tests import TestCase


class Test(TestCase):

    def assert_register(
            self,
            r: EntityRegistry,
            entity: Entity,
            **kwargs: Any
    ) -> None:
        if isinstance(entity, Item):
            self.assertEqual(r.register(entity, **kwargs), entity)
        elif isinstance(entity, Property):
            self.assertEqual(r.register(entity, **kwargs), entity)
        elif isinstance(entity, Lexeme):
            self.assertEqual(r.register(entity, **kwargs), entity)
        else:
            raise KIF_Object._should_not_get_here()

    def test__init__(self) -> None:
        r = EntityRegistry()
        assert_type(r, EntityRegistry)
        self.assertIsInstance(r, EntityRegistry)
        self.assertIsInstance(r, Registry)

    def test_register(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'entity', 'cannot coerce IRI into Entity',
            r.register, IRI('x'))

    def test_register_item(self) -> None:
        r = EntityRegistry()
        assert_type(r.register(Item('x')), Item)
        self.assert_register(r, Item('x'))
        self._test_register_label(Item('x'))
        self._test_register_alias(Item('x'))
        self._test_register_description(Item('x'))

    def test_register_property(self) -> None:
        r = EntityRegistry()
        assert_type(r.register(Property('x')), Property)
        self.assert_register(r, Property('x'))
        self._test_register_label(Property('x'))
        self._test_register_alias(Property('x'))
        self._test_register_description(Property('x'))
        # range
        r = EntityRegistry()
        prop = Property('x')
        self.assert_raises_bad_argument(
            TypeError, None, 'range', 'cannot coerce int into Datatype',
            r.register, prop, range=0)
        self.assertIsNone(r.get_range(prop))
        self.assert_register(r, prop, description='abc')
        self.assertIsNone(r.get_range(prop))
        self.assert_register(r, prop)
        self.assertEqual(r.register(prop, range=Item), Property('x', Item))
        self.assertEqual(r.get_range(prop), ItemDatatype())
        self.assertEqual(
            r.register(Property('x', String), range=String),
            Property('x', String))
        self.assertEqual(r.get_range(Property('x')), StringDatatype())
        # inverse
        r = EntityRegistry()
        prop = Property('x')
        self.assert_raises_bad_argument(
            TypeError, None, 'inverse', 'cannot coerce int into IRI',
            r.register, Property('x'), inverse=0)
        self.assertIsNone(r.get_inverse(prop))
        self.assert_register(r, prop, description='abc')
        self.assertIsNone(r.get_inverse(prop))
        self.assert_register(r, prop)
        self.assert_register(r, prop, inverse=Property('y'))
        self.assertEqual(r.get_inverse(prop), Property('y'))
        self.assert_register(r, prop, inverse=Property('z'))
        self.assertEqual(r.get_inverse(prop), Property('z'))

    def _test_register_label(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            r.register, entity, label=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            r.register, entity, labels=['x', 0])
        self.assertIsNone(r.get_label(entity))
        self.assert_register(r, entity, description='abc')
        self.assertIsNone(r.get_label(entity))
        self.assert_register(r, entity)
        self.assert_register(r, entity, label='abc')
        self.assertEqual(r.get_label(entity), Text('abc'))
        self.assert_register(r, entity, label=Text('abc', 'pt'))
        self.assertEqual(r.get_label(entity, 'pt'), Text('abc', 'pt'))
        self.assert_register(r, entity, label=Text('def', 'en'))
        self.assertEqual(r.get_label(entity), Text('def'))
        self.assert_register(r, entity, labels=[
            Text('def', 'pt'), Text('abc', 'fr')])
        self.assertEqual(r.get_label(entity), Text('def'))
        self.assertEqual(r.get_label(entity, 'en'), Text('def'))
        self.assertEqual(r.get_label(entity, 'pt'), Text('def', 'pt'))
        self.assertEqual(r.get_label(entity, 'fr'), Text('abc', 'fr'))

    def _test_register_alias(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            r.register, entity, alias=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            r.register, entity, aliases=[0])
        self.assertIsNone(r.get_aliases(entity))
        self.assert_register(r, entity, description='abc')
        self.assertIsNone(r.get_aliases(entity))
        self.assert_register(r, entity)
        self.assert_register(r, entity, alias='abc')
        self.assertEqual(r.get_aliases(entity), {Text('abc')})
        self.assert_register(r, entity, alias=Text('abc', 'pt'))
        self.assertEqual(r.get_aliases(entity, 'pt'), {Text('abc', 'pt')})
        self.assert_register(
            r, entity, aliases=[Text('def'), Text('def', 'pt')])
        self.assertEqual(
            r.get_aliases(entity), {Text('abc'), Text('def')})
        self.assertEqual(
            r.get_aliases(entity, 'pt'),
            {Text('abc', 'pt'), Text('def', 'pt')})
        self.assertIsNone(r.get_aliases(entity, 'fr'))
        self.assert_register(r, entity, aliases=[
            Text('abc', 'pt'), Text('abc', 'fr'), Text('ghi', 'fr')])
        self.assertEqual(
            r.get_aliases(entity, 'pt'),
            {Text('abc', 'pt'), Text('def', 'pt')})
        self.assertEqual(
            r.get_aliases(entity, 'fr'),
            {Text('abc', 'fr'), Text('ghi', 'fr')})

    def _test_register_description(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            r.register, entity, description=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            r.register, entity, descriptions=['x', 0])
        self.assertIsNone(r.get_description(entity))
        self.assert_register(r, entity, label='abc')
        self.assertIsNone(r.get_description(entity))
        self.assert_register(r, entity)
        self.assert_register(r, entity, description='abc')
        self.assertEqual(r.get_description(entity), Text('abc'))
        self.assert_register(r, entity, description=Text('abc', 'pt'))
        self.assertEqual(r.get_description(entity, 'pt'), Text('abc', 'pt'))
        self.assert_register(r, entity, description=Text('def', 'en'))
        self.assertEqual(r.get_description(entity), Text('def'))
        self.assert_register(r, entity, descriptions=[
            Text('def', 'pt'), Text('abc', 'fr')])
        self.assertEqual(r.get_description(entity), Text('def'))
        self.assertEqual(r.get_description(entity, 'en'), Text('def'))
        self.assertEqual(r.get_description(entity, 'pt'), Text('def', 'pt'))
        self.assertEqual(r.get_description(entity, 'fr'), Text('abc', 'fr'))

    def test_register_lexeme(self) -> None:
        r = EntityRegistry()
        lex = Lexeme('x')
        assert_type(r.register(Lexeme('x')), Lexeme)
        self.assert_register(r, Lexeme('x'))
        # lemma
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'lemma', 'cannot coerce int into Text',
            r.register, lex, lemma=0)
        self.assertIsNone(r.get_lemma(lex))
        self.assert_register(r, lex, category=Item('y'))
        self.assertIsNone(r.get_lemma(lex))
        self.assert_register(r, lex)
        self.assert_register(r, lex, lemma='abc')
        self.assertEqual(r.get_lemma(lex), Text('abc'))
        self.assert_register(r, lex, lemma=Text('abc', 'pt'))
        self.assertEqual(r.get_lemma(lex), Text('abc', 'pt'))
        # category
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'category', 'cannot coerce int into IRI',
            r.register, lex, category=0)
        self.assertIsNone(r.get_category(lex))
        self.assert_register(r, lex, lemma='abc')
        self.assertIsNone(r.get_category(lex))
        self.assert_register(r, lex)
        self.assert_register(r, lex, category=Item('y'))
        self.assertEqual(r.get_category(lex), Item('y'))
        self.assert_register(r, lex, category=Item('z'))
        self.assertEqual(r.get_category(lex), Item('z'))
        # language
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into IRI',
            r.register, lex, language=0)
        self.assertIsNone(r.get_language(lex))
        self.assert_register(r, lex, lemma='abc')
        self.assertIsNone(r.get_language(lex))
        self.assert_register(r, lex)
        self.assert_register(r, lex, language=Item('y'))
        self.assertEqual(r.get_language(lex), Item('y'))
        self.assert_register(r, lex, language=Item('z'))
        self.assertEqual(r.get_language(lex), Item('z'))


if __name__ == '__main__':
    Test.main()
