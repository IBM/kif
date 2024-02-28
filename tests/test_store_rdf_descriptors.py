# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import (
    Datatype,
    Descriptor,
    Item,
    ItemDescriptor,
    Lexeme,
    LexemeDescriptor,
    Property,
    PropertyDescriptor,
    Store,
    Text,
    TextSet,
)

from .data import (
    ADAM_TTL,
    ANDAR_TTL,
    BENZENE_TTL,
    BRAZIL_TTL,
    INSTANCE_OF_TTL,
    PAINT_TTL,
)
from .tests import kif_StoreTestCase, main


class TestStoreDescriptors(kif_StoreTestCase):

    Adam_en = (
        Text('Adam'),
        TextSet(),
        Text('first man according to the Abrahamic creation and '
             'religions such as Judaism, Christianity, and Islam'))

    Adam_pt_br = (
        Text('Adão', 'pt-br'),
        TextSet(),
        Text('figura bíblica do livro de Gênesis', 'pt-br'))

    andar_verb_pt = (
        Text('andar', 'pt'),
        wd.verb,
        wd.Portuguese)

    Brazil_en = (
        Text('Brazil'),
        TextSet(),
        Text('country in South America'))

    Brazil_pt_br = (
        Text('Brasil', 'pt-br'),
        TextSet(Text('🇧🇷', 'pt-br'), Text('pindorama', 'pt-br')),
        Text('país na América do Sul', 'pt-br'))

    InChIKey_en = (
        Text('InChIKey', 'en'),
        TextSet(),
        Text('A hashed version of the full standard InChI - '
             'designed to create an identifier that encodes structural '
             'information and can also be practically '
             'used in web searching.', 'en'),
        Datatype.external_id)

    InChIKey_es = (
        Text('InChIKey', 'es'),
        TextSet(),
        Text('código condensado para la identificación '
             'de un compuesto químico', 'es'),
        Datatype.external_id)

    instance_of_en = (
        Text('instance of'),
        TextSet(
            Text('is a'), Text('type'), Text('is of type'), Text('has type')),
        Text('that class of which this subject is a particular example '
             'and member; different from P279 (subclass of); for example: '
             'K2 is an instance of mountain; volcano is a subclass of '
             'mountain (and an instance of volcanic landform)'),
        Datatype.item)

    instance_of_es = (
        None,
        TextSet(),
        None,
        Datatype.item)

    Latin_America_en = (
        Text('Latin America', 'en'),
        TextSet(Text('LatAm', 'en')),
        Text('region of the Americas where Romance languages '
             'are primarily spoken', 'en'))

    Latin_America_pt_br = (
        None,
        TextSet(),
        None)

    paint_verb_en = (
        Text('paint', 'en'),
        wd.verb,
        wd.English)

# -- get_item_descriptor ---------------------------------------------------

    def test_get_item_descriptor_sanity(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self.sanity_check_get_item_descriptor(kb)
        it = kb.get_item_descriptor([Item('x'), Property('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_item_descriptor' "
            r'\(expected Item, got Property\)', list, it)

    def test_get_item_descriptor_single_item(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ((item, desc),) = kb.get_item_descriptor(wd.Adam)
        self.assertEqual(item, wd.Adam)
        self.assert_item_descriptor(desc, *self.Adam_en)

    def test_get_item_descriptor_multiple_items(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ds = list(kb.get_item_descriptor(
            [wd.Adam, Item('x'), wd.Brazil], 'pt-br'))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Adam)
        self.assert_item_descriptor(ds[0][1], *self.Adam_pt_br)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Brazil)
        self.assert_item_descriptor(ds[2][1], *self.Brazil_pt_br)

    def test_get_item_descriptor_mask(self):
        def test_case(kb, flags, desc01, desc21):
            ds = list(kb.get_item_descriptor(
                [wd.Brazil, Item('x'), wd.Latin_America], None, flags))
            self.assertEqual(len(ds), 3)
            self.assertEqual(ds[0][0], wd.Brazil)
            self.assertEqual(ds[0][1], desc01)
            self.assertEqual(ds[1][0], Item('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.Latin_America)
            self.assertEqual(ds[2][1], desc21)
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        test_case(
            kb, 0,
            ItemDescriptor(),
            ItemDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            ItemDescriptor(self.Brazil_en[0]),
            ItemDescriptor(self.Latin_America_en[0]))
        test_case(
            kb, Descriptor.ALIASES,
            ItemDescriptor(None, self.Brazil_en[1]),
            ItemDescriptor(None, self.Latin_America_en[1]))
        test_case(
            kb, Descriptor.DESCRIPTION,
            ItemDescriptor(None, None, self.Brazil_en[2]),
            ItemDescriptor(None, None, self.Latin_America_en[2]))
        test_case(
            kb, Descriptor.ALIASES | Descriptor.DESCRIPTION | Descriptor.LEMMA,
            ItemDescriptor(None, self.Brazil_en[1], self.Brazil_en[2]),
            ItemDescriptor(
                None, self.Latin_America_en[1], self.Latin_America_en[2]))
        # no early filter
        kb.unset_flags(kb.EARLY_FILTER)
        test_case(
            kb, 0,
            ItemDescriptor(),
            ItemDescriptor())
        # no late filter
        kb.unset_flags(kb.LATE_FILTER)
        test_case(
            kb, 0,
            ItemDescriptor(*self.Brazil_en),
            ItemDescriptor(*self.Latin_America_en))

    def test_get_item_descriptor_missing_attribute(self):
        def test_case(comments, desc):
            lines = [
                'schema:version 0',
                'rdfs:label "lll"@en',
                'skos:altLabel "xxx"@en',
                'skos:altLabel "yyy"@en',
                'skos:altLabel "zzz"@fr',
                'schema:description "aaa"@en',
                'schema:description "bbb"@fr'
            ]
            ttl = ('wd:Q_empty '
                   + ' ;\n'.join(filter(lambda s: all(map(
                       lambda c: not s.startswith(c), comments)), lines))
                   + ' .')
            kb = self.parse(ttl)
            pair = next(kb.get_item_descriptor(wd.Q('_empty')))
            self.assertEqual(pair[0], wd.Q('_empty'))
            self.assertEqual(pair[1], desc)
        test_case(
            ['rdfs:label'],
            ItemDescriptor(None, [Text('xxx'), Text('yyy')], Text('aaa')))
        test_case(
            ['skos:altLabel'],
            ItemDescriptor('lll', [], Text('aaa')))
        test_case(
            ['schema:description'],
            ItemDescriptor('lll', [Text('xxx'), Text('yyy')], None))

# -- get_property_descriptor -----------------------------------------------

    def test_get_property_descriptor_sanity(self):
        kb = Store('rdf', INSTANCE_OF_TTL)
        self.sanity_check_get_property_descriptor(kb)
        it = kb.get_property_descriptor([Property('x'), Item('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_property_descriptor' "
            r'\(expected Property, got Item\)', list, it)

    def test_get_property_descriptor_single_property(self):
        kb = Store('rdf', BENZENE_TTL, INSTANCE_OF_TTL)
        ((prop, desc),) = kb.get_property_descriptor(wd.instance_of)
        self.assertEqual(prop, wd.instance_of)
        self.assert_property_descriptor(desc, *self.instance_of_en)

    def test_get_property_descriptor_multiple_properties(self):
        kb = Store('rdf', BENZENE_TTL, INSTANCE_OF_TTL)
        ds = list(kb.get_property_descriptor(
            [wd.instance_of, Property('x'), wd.InChIKey], 'es'))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.instance_of)
        self.assert_property_descriptor(ds[0][1], *self.instance_of_es)
        self.assertEqual(ds[1][0], Property('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.InChIKey)
        self.assert_property_descriptor(ds[2][1], *self.InChIKey_es)

    def test_get_property_descriptor_mask(self):
        def test_case(kb, flags, desc01, desc21):
            ds = list(kb.get_property_descriptor(
                [wd.instance_of, Property('x'), wd.InChIKey], None, flags))
            self.assertEqual(len(ds), 3)
            self.assertEqual(ds[0][0], wd.instance_of)
            self.assertEqual(ds[0][1], desc01)
            self.assertEqual(ds[1][0], Property('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.InChIKey)
            self.assertEqual(ds[2][1], desc21)
        kb = Store('rdf', BENZENE_TTL, INSTANCE_OF_TTL)
        test_case(
            kb, 0,
            PropertyDescriptor(),
            PropertyDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            PropertyDescriptor(self.instance_of_en[0]),
            PropertyDescriptor(self.InChIKey_en[0]))
        test_case(
            kb, Descriptor.ALIASES,
            PropertyDescriptor(None, self.instance_of_en[1]),
            PropertyDescriptor(None, self.InChIKey_en[1]))
        test_case(
            kb, Descriptor.DESCRIPTION,
            PropertyDescriptor(None, None, self.instance_of_en[2]),
            PropertyDescriptor(None, None, self.InChIKey_en[2]))
        test_case(
            kb, Descriptor.DATATYPE,
            PropertyDescriptor(None, None, None, self.instance_of_en[3]),
            PropertyDescriptor(None, None, None, self.InChIKey_en[3]))
        # no early filter
        kb.unset_flags(kb.EARLY_FILTER)
        test_case(
            kb, 0,
            PropertyDescriptor(),
            PropertyDescriptor())
        # no late filter
        kb.unset_flags(kb.LATE_FILTER)
        test_case(
            kb, 0,
            PropertyDescriptor(*self.instance_of_en),
            PropertyDescriptor(*self.InChIKey_en))

    def test_get_property_descriptor_missing_attribute(self):
        def test_case(comments, desc):
            lines = [
                'schema:version 0',
                'wikibase:propertyType wikibase:WikibaseItem',
                'rdfs:label "lll"@en',
                'skos:altLabel "xxx"@en',
                'skos:altLabel "yyy"@en',
                'skos:altLabel "zzz"@fr',
                'schema:description "aaa"@en',
                'schema:description "bbb"@fr'
            ]
            ttl = ('wd:P_empty '
                   + ' ;\n'.join(filter(lambda s: all(map(
                       lambda c: not s.startswith(c), comments)), lines))
                   + ' .')
            kb = self.parse(ttl)
            pair = next(kb.get_property_descriptor(wd.P('_empty')))
            self.assertEqual(pair[0], wd.P('_empty'))
            self.assertEqual(pair[1], desc)
        test_case(
            ['rdfs:label'],
            PropertyDescriptor(
                None, [Text('xxx'), Text('yyy')], Text('aaa'), Datatype.item))
        test_case(
            ['skos:altLabel'],
            PropertyDescriptor('lll', [], Text('aaa'), Datatype.item))
        test_case(
            ['schema:description'],
            PropertyDescriptor(
                'lll', [Text('xxx'), Text('yyy')], None, Datatype.item))

# -- get_lexeme_descriptor -------------------------------------------------

    def test_get_lexeme_descriptor_sanity(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self.sanity_check_get_lexeme_descriptor(kb)
        it = kb.get_lexeme_descriptor([Lexeme('x'), Property('x')])
        self.assertRaisesRegex(
            TypeError, r"bad argument to 'Store\.get_lexeme_descriptor' "
            r'\(expected Lexeme, got Property\)', list, it)

    def test_get_lexeme_descriptor_single_lexeme(self):
        kb = Store('rdf', PAINT_TTL)
        ((lex, desc),) = kb.get_lexeme_descriptor(wd.L(96))
        self.assertEqual(lex, wd.L(96))
        self.assert_lexeme_descriptor(desc, *self.paint_verb_en)

    def test_get_lexeme_descriptor_multiple_lexemes(self):
        kb = Store('rdf', ANDAR_TTL, PAINT_TTL)
        ds = list(kb.get_lexeme_descriptor(
            [wd.L(46803), Lexeme('x'), wd.L(96)]))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.L(46803))
        self.assert_lexeme_descriptor(ds[0][1], *self.andar_verb_pt)
        self.assertEqual(ds[1][0], Lexeme('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.L(96))
        self.assert_lexeme_descriptor(ds[2][1], *self.paint_verb_en)

    def test_get_lexeme_descriptor_mask(self):
        def test_case(kb, flags, desc01, desc21):
            ds = list(kb.get_lexeme_descriptor(
                [wd.L(46803), Lexeme('x'), wd.L(96)], flags))
            self.assertEqual(len(ds), 3)
            self.assertEqual(ds[0][0], wd.L(46803))
            self.assertEqual(ds[0][1], desc01)
            self.assertEqual(ds[1][0], Lexeme('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.L(96))
            self.assertEqual(ds[2][1], desc21)
        kb = Store('rdf', ANDAR_TTL, PAINT_TTL)
        test_case(
            kb, 0,
            LexemeDescriptor(),
            LexemeDescriptor())
        test_case(
            kb, Descriptor.LEMMA,
            LexemeDescriptor(self.andar_verb_pt[0]),
            LexemeDescriptor(self.paint_verb_en[0]))
        test_case(
            kb, Descriptor.CATEGORY,
            LexemeDescriptor(None, self.andar_verb_pt[1]),
            LexemeDescriptor(None, self.paint_verb_en[1]))
        test_case(
            kb, Descriptor.LANGUAGE,
            LexemeDescriptor(None, None, self.andar_verb_pt[2]),
            LexemeDescriptor(None, None, self.paint_verb_en[2]))
        # no early filter
        kb.unset_flags(kb.EARLY_FILTER)
        test_case(
            kb, 0,
            LexemeDescriptor(),
            LexemeDescriptor())
        # no late filter
        kb.unset_flags(kb.LATE_FILTER)
        test_case(
            kb, 0,
            LexemeDescriptor(*self.andar_verb_pt),
            LexemeDescriptor(*self.paint_verb_en))


if __name__ == '__main__':
    main()
