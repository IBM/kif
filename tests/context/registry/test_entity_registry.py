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

    def assert_unregister(
            self,
            r: EntityRegistry,
            entity: Entity,
            **kwargs: Any
    ) -> None:
        if isinstance(entity, Item):
            self.assertTrue(r.unregister(entity, **kwargs))
        elif isinstance(entity, Property):
            self.assertTrue(r.unregister(entity, **kwargs))
        elif isinstance(entity, Lexeme):
            self.assertTrue(r.unregister(entity, **kwargs))
        else:
            raise KIF_Object._should_not_get_here()

    def test__init__(self) -> None:
        r = EntityRegistry()
        assert_type(r, EntityRegistry)
        self.assertIsInstance(r, EntityRegistry)
        self.assertIsInstance(r, Registry)

    def test_describe(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'entity', 'cannot coerce IRI into Entity',
            r.describe, IRI('x'))
        self.assertIsNone(r.describe(Item('x')))
        self.assert_register(r, Item('x'), label='abc')
        self.assertEqual(r.describe(Item('x')), {
            'labels': {'en': Text('abc')},
        })

    def test_get_label(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'entity', 'cannot coerce IRI into Entity',
            r.get_label, IRI('x'))
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            r.get_label, Item('x'), 0)
        self.assertIsNone(r.get_label(Item('x')))
        self.assert_register(r, Item('x'), labels=['abc', Text('abc', 'pt')])
        self.assertEqual(r.get_label(Item('x')), Text('abc'))
        self.assertEqual(r.get_label(Item('x'), 'en'), Text('abc'))
        self.assertIsNone(r.get_label(Item('x'), 'fr'))
        self.assertEqual(r.get_label(Item('x'), 'pt'), Text('abc', 'pt'))

    def test_get_aliases(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'entity', 'cannot coerce IRI into Entity',
            r.get_aliases, IRI('x'))
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            r.get_aliases, Item('x'), 0)
        self.assertIsNone(r.get_aliases(Item('x')))
        self.assert_register(
            r, Item('x'), aliases=['abc', 'def', Text('abc', 'pt')])
        self.assertEqual(
            r.get_aliases(Item('x')), {Text('def'), Text('abc')})
        self.assertEqual(
            r.get_aliases(Item('x'), 'en'), {Text('def'), Text('abc')})
        self.assertIsNone(r.get_aliases(Item('x'), 'fr'))
        self.assertEqual(r.get_aliases(Item('x'), 'pt'), {Text('abc', 'pt')})

    def test_get_description(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'entity', 'cannot coerce IRI into Entity',
            r.get_description, IRI('x'))
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            r.get_description, Item('x'), 0)
        self.assertIsNone(r.get_description(Item('x')))
        self.assert_register(
            r, Item('x'), descriptions=['abc', Text('abc', 'pt')])
        self.assertEqual(r.get_description(Item('x')), Text('abc'))
        self.assertEqual(r.get_description(Item('x'), 'en'), Text('abc'))
        self.assertIsNone(r.get_description(Item('x'), 'fr'))
        self.assertEqual(r.get_description(Item('x'), 'pt'), Text('abc', 'pt'))

    def test_get_range(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'property', 'cannot coerce int into IRI',
            r.get_range, 0)
        self.assertIsNone(r.get_range(Property('x')))
        self.assert_register(r, Property('x', Item), range=Item)
        self.assertEqual(r.get_range(Property('x')), ItemDatatype())

    def test_get_inverse(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'property', 'cannot coerce int into IRI',
            r.get_inverse, 0)
        self.assertIsNone(r.get_inverse(Property('x')))
        self.assert_register(r, Property('x'), inverse=Property('y'))
        self.assertEqual(r.get_inverse(Property('x')), Property('y'))

    def test_get_lemma(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'lexeme', 'cannot coerce int into IRI',
            r.get_lemma, 0)
        self.assertIsNone(r.get_lemma(Lexeme('x')))
        self.assert_register(r, Lexeme('x'), lemma='abc')
        self.assertEqual(r.get_lemma(Lexeme('x')), Text('abc'))

    def test_get_category(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'lexeme', 'cannot coerce int into IRI',
            r.get_category, 0)
        self.assertIsNone(r.get_category(Lexeme('x')))
        self.assert_register(r, Lexeme('x'), category=Item('y'))
        self.assertEqual(r.get_category(Lexeme('x')), Item('y'))

    def test_get_language(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'lexeme', 'cannot coerce int into IRI',
            r.get_language, 0)
        self.assertIsNone(r.get_language(Lexeme('x')))
        self.assert_register(r, Lexeme('x'), language=Item('y'))
        self.assertEqual(r.get_language(Lexeme('x')), Item('y'))

    def test_register(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'entity', 'cannot coerce IRI into Entity',
            r.register, IRI('x'))

    def test_unregister(self) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'entity', 'cannot coerce IRI into Entity',
            r.unregister, IRI('x'))

    def test_register_item(self) -> None:
        r = EntityRegistry()
        assert_type(r.register(Item('x')), Item)
        self.assert_register(r, Item('x'))
        self._test_register_label(Item('x'))
        self._test_register_alias(Item('x'))
        self._test_register_description(Item('x'))

    def test_unregister_item(self) -> None:
        r = EntityRegistry()
        assert_type(r.unregister(Item('x')), bool)
        self._test_unregister_label(Item('x'))
        self._test_unregister_aliases(Item('x'))
        self._test_unregister_description(Item('x'))
        # all
        r = EntityRegistry()
        item = Property('x', Item)
        self.assert_register(
            r, item, label='abc', alias='def', description='ghi')
        self.assertIsNotNone(r.describe(item))
        self.assert_unregister(r, item, all=True)
        self.assertIsNone(r.describe(item))
        self.assertFalse(r.unregister(item, all=True))

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

    def test_unregister_property(self) -> None:
        r = EntityRegistry()
        assert_type(r.unregister(Property('x')), bool)
        self._test_unregister_label(Property('x'))
        self._test_unregister_aliases(Property('x'))
        self._test_unregister_description(Property('x'))
        # range
        r = EntityRegistry()
        prop = Property('x')
        self.assertFalse(r.unregister(prop, range=True))
        self.assertEqual(r.register(prop, range=Item), Property('x', Item))
        self.assertEqual(r.get_range(prop), ItemDatatype())
        self.assert_unregister(r, prop, range=True)
        self.assertIsNone(r.get_range(prop))
        self.assertFalse(r.unregister(prop, range=True))
        # inverse
        r = EntityRegistry()
        prop = Property('x')
        self.assertFalse(r.unregister(prop, inverse=True))
        self.assert_register(r, prop, inverse=Property('y'))
        self.assertEqual(r.get_inverse(prop), Property('y'))
        self.assert_unregister(r, prop, inverse=True)
        self.assertIsNone(r.get_inverse(prop))
        self.assertFalse(r.unregister(prop, inverse=True))
        # all
        r = EntityRegistry()
        prop = Property('x', Item)
        self.assert_register(
            r, prop, label='abc', alias='def', description='ghi',
            range=Item, inverse=Property('y'))
        self.assertIsNotNone(r.describe(prop))
        self.assert_unregister(r, prop, all=True)
        self.assertIsNone(r.describe(prop))
        self.assertFalse(r.unregister(prop, all=True))

    def _test_register_label(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            r.register, entity, label=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            r.register, entity, labels=['x', 0])
        # label
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
        # labels
        self.assert_register(r, entity, labels=[
            Text('def', 'pt'), Text('abc', 'fr')])
        self.assertEqual(r.get_label(entity), Text('def'))
        self.assertEqual(r.get_label(entity, 'en'), Text('def'))
        self.assertEqual(r.get_label(entity, 'pt'), Text('def', 'pt'))
        self.assertEqual(r.get_label(entity, 'fr'), Text('abc', 'fr'))

    def _test_unregister_label(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            r.unregister, entity, label=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'labels', 'cannot coerce int into Text',
            r.unregister, entity, labels=['x', 0])
        # label
        self.assertFalse(r.unregister(entity, label='abc'))
        self.assert_register(r, entity, labels=[
            Text('abc'), Text('def', 'pt'), Text('abc', 'fr')])
        self.assertFalse(r.unregister(entity, label=Text('abc', 'pt')))
        self.assertEqual(r.get_label(entity, 'fr'), Text('abc', 'fr'))
        self.assert_unregister(r, entity, label=Text('abc', 'fr'))
        self.assertIsNone(r.get_label(entity, 'fr'))
        self.assertEqual(r.get_label(entity, 'pt'), Text('def', 'pt'))
        # labels
        self.assertFalse(r.unregister(entity, labels=['xyz']))
        self.assert_register(r, entity, label=Text('def', 'fr'))
        self.assert_unregister(r, entity, labels=[
            Text('abc'), Text('abc', 'pt'), Text('def', 'fr')])
        self.assertIsNone(r.get_label(entity, 'en'))
        self.assertEqual(r.get_label(entity, 'pt'), Text('def', 'pt'))
        self.assertIsNone(r.get_label(entity, 'fr'))
        self.assert_unregister(r, entity, labels=[Text('def', 'pt')])
        self.assertIsNone(r.describe(entity))
        # label_language
        self.assertFalse(r.unregister(entity, label='jp'))
        self.assert_register(r, entity, labels=['abc', Text('def', 'pt')])
        self.assert_unregister(r, entity, label_language='pt')
        self.assertIsNone(r.get_label(entity, 'pt'))
        self.assertEqual(r.get_label(entity), Text('abc'))
        # all_labels
        self.assert_unregister(r, entity, all_labels=True)
        self.assertIsNone(r.get_label(entity))
        self.assertFalse(r.unregister(entity, all_labels=True))
        # all
        self.assert_register(r, entity, labels=[
            Text('abc'), Text('def', 'pt'), Text('abc', 'fr')])
        self.assert_unregister(r, entity, all=True)
        self.assertIsNone(r.get_label(entity, 'en'))
        self.assertIsNone(r.get_label(entity, 'pt'))
        self.assertIsNone(r.get_label(entity, 'fr'))
        self.assertFalse(r.unregister(entity, all=True))

    def _test_register_alias(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            r.register, entity, alias=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            r.register, entity, aliases=[0])
        # alias
        self.assertIsNone(r.get_aliases(entity))
        self.assert_register(r, entity, description='abc')
        self.assertIsNone(r.get_aliases(entity))
        self.assert_register(r, entity)
        self.assert_register(r, entity, alias='abc')
        self.assertEqual(r.get_aliases(entity), {Text('abc')})
        self.assert_register(r, entity, alias=Text('abc', 'pt'))
        self.assertEqual(r.get_aliases(entity, 'pt'), {Text('abc', 'pt')})
        # aliases
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

    def _test_unregister_aliases(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            r.unregister, entity, alias=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'aliases', 'cannot coerce int into Text',
            r.unregister, entity, aliases=['x', 0])
        # alias
        self.assertFalse(r.unregister(entity, alias='abc'))
        self.assert_register(r, entity, aliases=[
            Text('abc'), Text('def', 'pt'), Text('abc', 'fr'),
            Text('def'), Text('abc', 'pt'), Text('def', 'fr')])
        self.assert_unregister(r, entity, alias=Text('abc', 'pt'))
        self.assertEqual(r.get_aliases(entity, 'pt'), {Text('def', 'pt')})
        self.assertFalse(r.unregister(entity, alias=Text('abc', 'pt')))
        # aliases
        self.assertFalse(r.unregister(entity, aliases=['xyz']))
        self.assert_unregister(r, entity, aliases=[
            Text('def'), Text('def', 'pt'), Text('abc', 'fr')])
        self.assertEqual(r.get_aliases(entity, 'en'), {Text('abc', 'en')})
        self.assertIsNone(r.get_aliases(entity, 'pt'))
        self.assertEqual(r.get_aliases(entity, 'fr'), {Text('def', 'fr')})
        self.assertFalse(r.unregister(entity, alias=Text('abc', 'jp')))
        # alias_language
        self.assertFalse(r.unregister(entity, alias_language='jp'))
        self.assert_register(r, entity, alias=Text('abc', 'pt'))
        self.assert_unregister(r, entity, alias_language='pt')
        self.assertIsNone(r.get_aliases(entity, 'pt'))
        # all_aliases
        self.assert_unregister(r, entity, all_aliases=True)
        self.assertIsNone(r.get_aliases(entity, 'en'))
        self.assertIsNone(r.get_aliases(entity, 'fr'))
        self.assertFalse(r.unregister(entity, all_aliases=True))
        # all
        self.assert_register(r, entity, aliases=[
            Text('abc'), Text('def', 'pt'), Text('abc', 'fr'),
            Text('def'), Text('abc', 'pt'), Text('def', 'fr')])
        self.assert_unregister(r, entity, all=True)
        self.assertIsNone(r.get_aliases(entity, 'en'))
        self.assertIsNone(r.get_aliases(entity, 'fr'))
        self.assertIsNone(r.get_aliases(entity, 'pt'))
        self.assertFalse(r.unregister(entity, all=True))

    def _test_register_description(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            r.register, entity, description=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            r.register, entity, descriptions=['x', 0])
        # description
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
        # descriptions
        self.assert_register(r, entity, descriptions=[
            Text('def', 'pt'), Text('abc', 'fr')])
        self.assertEqual(r.get_description(entity), Text('def'))
        self.assertEqual(r.get_description(entity, 'en'), Text('def'))
        self.assertEqual(r.get_description(entity, 'pt'), Text('def', 'pt'))
        self.assertEqual(r.get_description(entity, 'fr'), Text('abc', 'fr'))

    def _test_unregister_description(self, entity: Item | Property) -> None:
        r = EntityRegistry()
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            r.unregister, entity, description=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'descriptions', 'cannot coerce int into Text',
            r.unregister, entity, descriptions=['x', 0])
        self.assert_register(r, entity, descriptions=[
            Text('abc'), Text('def', 'pt'), Text('abc', 'fr')])
        # description
        self.assertFalse(r.unregister(entity, description=Text('abc', 'pt')))
        self.assertEqual(r.get_description(entity, 'fr'), Text('abc', 'fr'))
        self.assert_unregister(r, entity, description=Text('abc', 'fr'))
        self.assertIsNone(r.get_description(entity, 'fr'))
        self.assertEqual(r.get_description(entity, 'pt'), Text('def', 'pt'))
        # descriptions
        self.assertFalse(r.unregister(entity, descriptions=['xyz']))
        self.assert_register(r, entity, description=Text('def', 'fr'))
        self.assert_unregister(r, entity, descriptions=[
            Text('abc'), Text('abc', 'pt'), Text('def', 'fr')])
        self.assertIsNone(r.get_description(entity, 'en'))
        self.assertEqual(r.get_description(entity, 'pt'), Text('def', 'pt'))
        self.assertIsNone(r.get_description(entity, 'fr'))
        # description_language
        self.assertFalse(r.unregister(entity, description_language='jp'))
        self.assert_register(r, entity, description='abc')
        self.assert_unregister(r, entity, description_language='pt')
        self.assertIsNone(r.get_description(entity, 'pt'))
        self.assertEqual(r.get_description(entity), Text('abc'))
        # all_descriptions
        self.assert_unregister(r, entity, all_descriptions=True)
        self.assertIsNone(r.get_description(entity))
        self.assertFalse(r.unregister(entity, all_descriptions=True))
        # all
        self.assert_register(r, entity, descriptions=[
            Text('abc'), Text('def', 'pt'), Text('abc', 'fr')])
        self.assert_unregister(r, entity, all=True)
        self.assertIsNone(r.get_description(entity, 'en'))
        self.assertIsNone(r.get_description(entity, 'pt'))
        self.assertIsNone(r.get_description(entity, 'fr'))
        self.assertFalse(r.unregister(entity, all=True))

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

    def test_unregister_lexeme(self) -> None:
        r = EntityRegistry()
        assert_type(r.unregister(Lexeme('x')), bool)
        # lemma
        r = EntityRegistry()
        lex = Lexeme('x')
        self.assertFalse(r.unregister(lex, lemma=True))
        self.assert_register(r, lex, lemma='abc')
        self.assertEqual(r.get_lemma(lex), Text('abc'))
        self.assert_unregister(r, lex, lemma=True)
        self.assertIsNone(r.get_lemma(lex))
        self.assertFalse(r.unregister(lex, lemma=True))
        # category
        r = EntityRegistry()
        lex = Lexeme('x')
        self.assertFalse(r.unregister(lex, category=True))
        self.assert_register(r, lex, category=Item('y'))
        self.assertEqual(r.get_category(lex), Item('y'))
        self.assert_unregister(r, lex, category=True)
        self.assertIsNone(r.get_category(lex))
        self.assertFalse(r.unregister(lex, category=True))
        # language
        r = EntityRegistry()
        lex = Lexeme('x')
        self.assertFalse(r.unregister(lex, language=True))
        self.assert_register(r, lex, language=Item('y'))
        self.assertEqual(r.get_language(lex), Item('y'))
        self.assert_unregister(r, lex, language=True)
        self.assertIsNone(r.get_language(lex))
        self.assertFalse(r.unregister(lex, language=True))
        # all
        r = EntityRegistry()
        lex = Lexeme('x')
        self.assert_register(
            r, lex, lemma='abc', category=Item('y'), language=Item('z'))
        self.assertIsNotNone(r.describe(lex))
        self.assert_unregister(r, lex, all=True)
        self.assertIsNone(r.describe(lex))
        self.assertFalse(r.unregister(lex, all=True))


if __name__ == '__main__':
    Test.main()
