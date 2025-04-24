# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Context,
    ExternalId,
    IRI,
    Item,
    Lexeme,
    LexemeDatatype,
    Lexemes,
    LexemeTemplate,
    LexemeVariable,
    Property,
    Store,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import Any, assert_type, Iterable, Optional, Set

from ...tests import EntityTestCase


class Test(EntityTestCase):

    def assert_register(self, lexeme: Lexeme, **kwargs: Any) -> None:
        self.assertEqual(lexeme.register(**kwargs), lexeme)

    def assert_unregister(self, lexeme: Lexeme, **kwargs: Any) -> None:
        self.assertTrue(lexeme.unregister(**kwargs))

    def test_datatype_class(self) -> None:
        assert_type(Lexeme.datatype_class, type[LexemeDatatype])
        self.assertIs(Lexeme.datatype_class, LexemeDatatype)

    def test_datatype(self) -> None:
        assert_type(Lexeme.datatype, LexemeDatatype)
        self.assert_lexeme_datatype(Lexeme.datatype)

    def test_template_class(self) -> None:
        assert_type(Lexeme.template_class, type[LexemeTemplate])
        self.assertIs(Lexeme.template_class, LexemeTemplate)

    def test_variable_class(self) -> None:
        assert_type(Lexeme.variable_class, type[LexemeVariable])
        self.assertIs(Lexeme.variable_class, LexemeVariable)

    def test_check(self) -> None:
        assert_type(Lexeme.check(Lexeme('x')), Lexeme)
        self._test_check(
            Lexeme,
            success=[
                ('x', Lexeme('x')),
                (ExternalId('x'), Lexeme('x')),
            ],
            failure=[
                Item('x'),
                LexemeTemplate(Variable('x')),
                Property('x'),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        assert_type(Lexeme('x'), Lexeme)
        self._test__init__(
            Lexeme,
            self.assert_lexeme,
            failure=[
                [Item('x')],
                [LexemeTemplate(Variable('x'))],
                [Property('x')],
                [Text('x')],
                [Variable('x', Text)],
            ])

    def test_variables(self) -> None:
        assert_type(Lexeme('x').variables, Set[Variable])
        self._test_variables(Lexeme)

    def test_instantiate(self) -> None:
        assert_type(Lexeme('x').instantiate({}), Term)
        self._test_instantiate(Lexeme)

    def test_match(self) -> None:
        assert_type(Lexeme('x').match(Variable('x')), Optional[Theta])
        self._test_match(Lexeme)

    def test_display(self) -> None:
        with Context():
            assert_type(Item('x').display(), str)
            self.assertEqual(Lexeme('x').display(), 'x')
            self.assertEqual(Lexeme('x').display('pt'), 'x')

    def test_describe(self) -> None:
        with Context():
            assert_type(Lexeme('x').describe(), Optional[Lexeme.Descriptor])
            self.assertIsNone(Lexeme('x').describe())
            self.assert_register(
                Lexeme('x'), lemma='abc',
                category=Item('x'), language=Item('y'))
            self.assertEqual(
                Lexeme('x').describe(),
                {'lemma': Text('abc', 'en'),
                 'category': Item('x'),
                 'language': Item('y')})
        self.assertIsNone(Lexeme('x').describe())

    def test_get_lemma(self) -> None:
        with Context():
            assert_type(Lexeme('x').get_lemma(), Optional[Text])
            self.assertIsNone(Lexeme('x').get_lemma())
            self.assert_register(Lexeme('x'), lemma=Text('abc', 'pt'))
            self.assertEqual(Lexeme('x').get_lemma(), Text('abc', 'pt'))
            self.assert_register(Lexeme('x'), lemma='abc')
            self.assertEqual(Lexeme('x').lemma, Text('abc', 'en'))
        self.assertIsNone(Lexeme('x').lemma)

    def test_get_category(self) -> None:
        with Context():
            assert_type(Lexeme('x').get_category(), Optional[Item])
            self.assertIsNone(Lexeme('x').get_category())
            self.assert_register(Lexeme('x'), category=Item('y'))
            self.assertEqual(Lexeme('x').get_category(), Item('y'))
            self.assert_register(Lexeme('x'), category=Item('z'))
            self.assertEqual(Lexeme('x').category, Item('z'))
        self.assertIsNone(Lexeme('x').category)

    def test_get_language(self) -> None:
        with Context():
            assert_type(Lexeme('x').get_language(), Optional[Item])
            self.assertIsNone(Lexeme('x').get_language())
            self.assert_register(Lexeme('x'), language=Item('y'))
            self.assertEqual(Lexeme('x').get_language(), Item('y'))
            self.assert_register(Lexeme('x'), language=Item('z'))
            self.assertEqual(Lexeme('x').language, Item('z'))
        self.assertIsNone(Lexeme('x').language)

    def test_get_resolver(self) -> None:
        with Context():
            kb1, kb2 = Store('empty'), Store('empty')
            ns1, ns2 = IRI('http://x#'), IRI('http://y#')
            l1, l2 = Item('http://x#l1'), Item('http://y#l2')
            assert_type(l1.get_resolver(), Optional[Store])
            self.assertIsNone(l1.get_resolver())
            self.assertIsNone(l2.resolver)
            ns1.register(resolver=kb1)
            ns2.register(resolver=kb2)
            self.assertEqual(l1.get_resolver(), kb1)
            self.assertEqual(l2.resolver, kb2)
            ns1.unregister()
            self.assertIsNone(l1.resolver)
            self.assertEqual(l2.resolver, kb2)
            ns2.unregister()
            self.assertIsNone(l1.resolver)
            self.assertIsNone(l2.resolver)
        self.assertIsNone(Item('x').resolver)

    def test_register(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'lemma', 'cannot coerce int into Text',
            Lexeme('x').register, lemma=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'category', 'cannot coerce int into IRI',
            Lexeme('x').register, category=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into IRI',
            Lexeme('x').register, language=0)
        with Context():
            assert_type(Lexeme('x').register(), Lexeme)
            self.assertEqual(Lexeme('x').register(), Lexeme('x'))
            self.assertIsNone(Lexeme('x').describe())
            self.assert_register(
                Lexeme('x'),
                lemma=Text('abc'),
                category=Item('y'),
                language=Item('z'))
            self.assertEqual(Lexeme('x').describe(), {
                'lemma': Text('abc', 'en'),
                'category': Item('y'),
                'language': Item('z'),
            })
        self.assertIsNone(Lexeme('x').describe())

    def test_unregister(self) -> None:
        with Context():
            assert_type(Lexeme('x').unregister(), bool)
            self.assertIsNone(Lexeme('x').describe())
            self.assert_register(
                Lexeme('x'),
                lemma=Text('abc'),
                category=Item('y'),
                language=Item('z'))
            self.assert_unregister(Lexeme('x'), lemma=True)
            self.assertEqual(Lexeme('x').describe(), {
                'category': Item('y'),
                'language': Item('z')
            })
            self.assertTrue(Lexeme('x').unregister())
            self.assertIsNone(Lexeme('x').describe())
            self.assert_register(Lexeme('x').register(lemma='abc'))
            self.assertEqual(Lexeme('x').lemma, Text('abc'))
        self.assertIsNone(Lexeme('x').describe())

    def test_Lexemes(self) -> None:
        assert_type(Lexemes('a', 'b', 'c'), Iterable[Lexeme])
        self._test_Entities(
            Lexemes,
            self.assert_lexeme,
            failure=[
                Item('x'),
                Lexeme('x'),
                LexemeTemplate(Variable('x')),
                Property('x'),
                Text('x'),
                Variable('x', Text),
            ])


if __name__ == '__main__':
    Test.main()
