# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Descriptor,
    Item,
    ItemDatatype,
    ItemDescriptor,
    Lexeme,
    LexemeDescriptor,
    Nil,
    Property,
    PropertyDescriptor,
    Store,
    Text,
    TextSet,
)
from kif_lib.vocabulary import wd

from .data import (
    ADAM_TTL,
    ANDAR_TTL,
    BENZENE_TTL,
    BRAZIL_TTL,
    INSTANCE_OF_TTL,
    PAINT_TTL,
)
from .tests import kif_StoreTestCase


class TestStoreMixerDescriptors(kif_StoreTestCase):

    kb_adam = Store('rdf', ADAM_TTL)
    kb_andar = Store('rdf', ANDAR_TTL)
    kb_benzene = Store('rdf', BENZENE_TTL)
    kb_brazil = Store('rdf', BRAZIL_TTL)
    kb_instance_of = Store('rdf', INSTANCE_OF_TTL)
    kb_paint = Store('rdf', PAINT_TTL)

    kb_extra = kif_StoreTestCase.parse('''
# andar - verb - portuguese
wd:L46803
    schema:version "0"^^xsd:integer ;
    wikibase:lemma "andar"@pt ;
    wikibase:lexicalCategory wd:Q24905 ;
    dct:language wd:Q5146 .

# benzene
wd:Q2270
    schema:version "0"^^xsd:integer ;
    rdfs:label "benzene"@en ;
    rdfs:label "benzeno"@pt-br ;
    skos:altLabel "C6H6"@en ;
    skos:altLabel "benzol"@pt-br ;
    skos:altLabel "ciclo-hexa-1,3,5-trieno"@pt-br ;
    schema:description "hydrocarbon compound consisting of a 6-sided ring"@en ;
    schema:description "substância química"@pt-br .

# Brazil
wd:Q155
    schema:version "0"^^xsd:integer ;
    rdfs:label "Brazil"@en ;
    rdfs:label "Brasil"@pt-br ;
    skos:altLabel "🇧🇷"@en ;
    skos:altLabel "BRA"@pt-br .

# instance of
wd:P31
    schema:version "0"^^xsd:integer ;
    wikibase:propertyType wikibase:WikibaseItem ;
    rdfs:label "instancia de"@es ;
    skos:altLabel "∈"@en ;
    skos:altLabel "rdf:type"@en ;
    skos:altLabel "∈"@es .
''')

    extra_benzene_en = ItemDescriptor(
        'benzene', [Text('C6H6')],
        'hydrocarbon compound consisting of a 6-sided ring')

    extra_benzene_pt_br = ItemDescriptor(
        Text('benzeno', 'pt-br'),
        TextSet(
            Text('benzol', 'pt-br'),
            Text('ciclo-hexa-1,3,5-trieno', 'pt-br')),
        Text('substância química', 'pt-br'))

    extra_Brazil_en = ItemDescriptor(
        Text('Brazil'), [Text('🇧🇷')])

    extra_Brazil_pt_br = ItemDescriptor(
        Text('Brasil', 'pt-br'), [Text('BRA', 'pt-br')])

    extra_instance_of_en = PropertyDescriptor(
        None, [Text('∈'), Text('rdf:type')], None, ItemDatatype())

    extra_instance_of_es = PropertyDescriptor(
        Text('instancia de', 'es'), [Text('∈', 'es')], None, ItemDatatype())

# -- get_descriptor --------------------------------------------------------

    def test_get_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_descriptor(kb)

    def test_get_descriptor_single_entity(self):
        kb = Store(
            'mixer', [self.kb_instance_of, self.kb_paint, self.kb_brazil])
        ds = list(kb.get_item_descriptor(wd.Brazil))
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(ds[0][1], *BRAZIL_TTL.Brazil_en)

    def test_get_descriptor_single_entity_with_merges(self):
        kb = Store(
            'mixer', [self.kb_extra, self.kb_instance_of,
                      self.kb_paint, self.kb_brazil])
        ds = list(kb.get_descriptor(wd.Brazil, 'pt-br'))
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(
            ds[0][1], BRAZIL_TTL.Brazil_pt_br[0],
            TextSet(*self.extra_Brazil_pt_br[1], *BRAZIL_TTL.Brazil_pt_br[1]),
            BRAZIL_TTL.Brazil_pt_br[2])

    def test_get_descriptor_multiple_entities(self):
        kb = Store(
            'mixer', [self.kb_instance_of, self.kb_paint, self.kb_brazil])
        ds = list(kb.get_descriptor([
            wd.Brazil, Property('x'),
            wd.L(96), Item('x'), wd.instance_of]))
        self.assertEqual(len(ds), 5)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(ds[0][1], *BRAZIL_TTL.Brazil_en)
        self.assertEqual(ds[1][0], Property('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.L(96))
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_lexeme_descriptor(ds[2][1], *PAINT_TTL.paint_verb_en)
        self.assertEqual(ds[3][0], Item('x'))
        self.assertIsNone(ds[3][1])
        self.assertEqual(ds[4][0], wd.instance_of)
        self.assertIsNotNone(ds[4][1])
        assert ds[4][1] is not None
        self.assert_property_descriptor(
            ds[4][1], *INSTANCE_OF_TTL.instance_of_en)

    def test_get_descriptor_multiple_entities_with_merges(self):
        kb = Store(
            'mixer', [self.kb_instance_of, self.kb_paint,
                      self.kb_extra, self.kb_brazil])
        ds = list(kb.get_descriptor([
            wd.Brazil, Property('x'),
            wd.L(96), Item('x'), wd.instance_of]))
        self.assertEqual(len(ds), 5)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(
            ds[0][1], BRAZIL_TTL.Brazil_en[0], TextSet(
                *BRAZIL_TTL.Brazil_en[1], *self.extra_Brazil_en[1]),
            BRAZIL_TTL.Brazil_en[2])
        self.assertEqual(ds[1][0], Property('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.L(96))
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_lexeme_descriptor(ds[2][1], *PAINT_TTL.paint_verb_en)
        self.assertEqual(ds[3][0], Item('x'))
        self.assertIsNone(ds[3][1])
        self.assertEqual(ds[4][0], wd.instance_of)
        self.assertIsNotNone(ds[4][1])
        assert ds[4][1] is not None
        self.assert_property_descriptor(
            ds[4][1], INSTANCE_OF_TTL.instance_of_en[0], TextSet(
                *INSTANCE_OF_TTL.instance_of_en[1],
                *self.extra_instance_of_en[1]),
            *INSTANCE_OF_TTL.instance_of_en[2:])

    def test_get_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21, desc41):
            ds = list(kb.get_descriptor([
                wd.Brazil, Property('x'),
                wd.L(96), Item('x'), wd.instance_of], None, mask))
            self.assertEqual(len(ds), 5)
            self.assertEqual(ds[0][0], wd.Brazil)
            self.assert_item_descriptor(ds[0][1], *desc01)
            self.assertEqual(ds[1][0], Property('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.L(96))
            self.assert_lexeme_descriptor(ds[2][1], *desc21)
            self.assertEqual(ds[3][0], Item('x'))
            self.assertIsNone(ds[3][1])
            self.assertEqual(ds[4][0], wd.instance_of)
            self.assert_property_descriptor(ds[4][1], *desc41)
        kb = Store(
            'mixer', [self.kb_instance_of, self.kb_paint,
                      self.kb_extra, self.kb_brazil])
        test_case(
            kb, 0,
            ItemDescriptor(),
            LexemeDescriptor(),
            PropertyDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            ItemDescriptor(BRAZIL_TTL.Brazil_en[0]),
            LexemeDescriptor(),
            PropertyDescriptor(INSTANCE_OF_TTL.instance_of_en[0]))
        test_case(
            kb, Descriptor.ALIASES | Descriptor.LANGUAGE,
            ItemDescriptor(None, TextSet(
                *self.extra_Brazil_en[1],
                *BRAZIL_TTL.Brazil_en[1])),
            LexemeDescriptor(None, None, PAINT_TTL.paint_verb_en[2]),
            PropertyDescriptor(None, TextSet(
                *self.extra_instance_of_en[1],
                *INSTANCE_OF_TTL.instance_of_en[1])))
        # no early filter
        kb.unset_flags(kb.EARLY_FILTER)
        test_case(
            kb, 0,
            ItemDescriptor(),
            LexemeDescriptor(),
            PropertyDescriptor())
        # no late filter
        kb.unset_flags(kb.LATE_FILTER)
        test_case(
            kb, 0,
            ItemDescriptor(BRAZIL_TTL.Brazil_en[0], TextSet(
                *self.extra_Brazil_en[1],
                *BRAZIL_TTL.Brazil_en[1]),
                BRAZIL_TTL.Brazil_en[2]),
            LexemeDescriptor(*PAINT_TTL.paint_verb_en),
            PropertyDescriptor(INSTANCE_OF_TTL.instance_of_en[0], TextSet(
                *self.extra_instance_of_en[1],
                *INSTANCE_OF_TTL.instance_of_en[1]),
                *INSTANCE_OF_TTL.instance_of_en[2:]))
        # reset
        kb.set_flags(kb.EARLY_FILTER | kb.LATE_FILTER)

# -- get_item_descriptor ---------------------------------------------------

    def test_get_item_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_item_descriptor(kb)

    def test_get_item_descriptor_single_item(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene])
        ds = list(kb.get_item_descriptor(wd.benzene))
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0][0], wd.benzene)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(ds[0][1], *BENZENE_TTL.benzene_en)

    def test_get_item_descriptor_single_item_with_merges(self):
        kb = Store('mixer', [self.kb_extra, self.kb_benzene])
        ds = list(kb.get_item_descriptor(wd.benzene))
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0][0], wd.benzene)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(
            ds[0][1],
            BENZENE_TTL.benzene_en[0],
            TextSet(Text('C6H6'), *BENZENE_TTL.benzene_en[1]),
            self.extra_benzene_en.description)

    def test_get_item_descriptor_multiple_items(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        ds = list(kb.get_item_descriptor(
            [wd.Adam, Item('x'), wd.Brazil], 'pt-br'))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Adam)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(ds[0][1], *ADAM_TTL.Adam_pt_br)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Brazil)
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_item_descriptor(ds[2][1], *BRAZIL_TTL.Brazil_pt_br)

    def test_get_item_descriptor_multiple_items_with_merges(self):
        kb = Store('mixer', [
            self.kb_adam, self.kb_benzene, self.kb_extra, self.kb_brazil])
        ds = list(kb.get_item_descriptor(
            [wd.Adam, Item('x'), wd.Brazil, wd.benzene], 'pt-br'))
        self.assertEqual(len(ds), 4)
        self.assertEqual(ds[0][0], wd.Adam)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(ds[0][1], *ADAM_TTL.Adam_pt_br)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Brazil)
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_item_descriptor(
            ds[2][1], BRAZIL_TTL.Brazil_pt_br[0],
            TextSet(
                *self.extra_Brazil_pt_br[1],
                *BRAZIL_TTL.Brazil_pt_br[1]),
            BRAZIL_TTL.Brazil_pt_br[2])
        self.assertEqual(ds[3][0], wd.benzene)
        self.assertIsNotNone(ds[3][1])
        assert ds[3][1] is not None
        self.assert_item_descriptor(ds[3][1], *self.extra_benzene_pt_br)

    def test_get_item_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21, desc31):
            ds = list(kb.get_item_descriptor(
                [wd.Adam, Item('x'), wd.Brazil, wd.benzene], 'pt-br', mask))
            self.assertEqual(len(ds), 4)
            self.assertEqual(ds[0][0], wd.Adam)
            self.assert_item_descriptor(ds[0][1], *desc01)
            self.assertEqual(ds[1][0], Item('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.Brazil)
            self.assert_item_descriptor(ds[2][1], *desc21)
            self.assertEqual(ds[3][0], wd.benzene)
            self.assert_item_descriptor(ds[3][1], *desc31)
        kb = Store('mixer', [
            self.kb_adam, self.kb_benzene, self.kb_extra, self.kb_brazil])
        test_case(
            kb, 0,
            ItemDescriptor(),
            ItemDescriptor(),
            ItemDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            ItemDescriptor(ADAM_TTL.Adam_pt_br[0]),
            ItemDescriptor(BRAZIL_TTL.Brazil_pt_br[0]),
            ItemDescriptor(self.extra_benzene_pt_br[0]))
        test_case(
            kb, Descriptor.ALIASES,
            ItemDescriptor(None, ADAM_TTL.Adam_pt_br[1]),
            ItemDescriptor(
                None, TextSet(*self.extra_Brazil_pt_br[1],
                              *BRAZIL_TTL.Brazil_pt_br[1])),
            ItemDescriptor(None, self.extra_benzene_pt_br[1]))
        test_case(
            kb, Descriptor.DESCRIPTION,
            ItemDescriptor(None, None, ADAM_TTL.Adam_pt_br[2]),
            ItemDescriptor(None, None, BRAZIL_TTL.Brazil_pt_br[2]),
            ItemDescriptor(None, None, self.extra_benzene_pt_br[2]))
        test_case(
            kb, Descriptor.LABEL | Descriptor.ALIASES,
            ADAM_TTL.Adam_pt_br.replace(None, None, Nil),
            BRAZIL_TTL.Brazil_pt_br.replace(
                None,
                TextSet(*self.extra_Brazil_pt_br[1],
                        *BRAZIL_TTL.Brazil_pt_br[1]), Nil),
            ItemDescriptor(*self.extra_benzene_pt_br[0:2]))
        # no early filter
        kb.unset_flags(kb.EARLY_FILTER)
        test_case(
            kb, 0,
            ItemDescriptor(),
            ItemDescriptor(),
            ItemDescriptor())
        # no late filter
        kb.unset_flags(kb.LATE_FILTER)
        test_case(
            kb, 0,
            ADAM_TTL.Adam_pt_br,
            BRAZIL_TTL.Brazil_pt_br.replace(
                None,
                TextSet(*self.extra_Brazil_pt_br[1],
                        *BRAZIL_TTL.Brazil_pt_br[1])),
            self.extra_benzene_pt_br)
        # reset
        kb.set_flags(kb.EARLY_FILTER | kb.LATE_FILTER)

# -- get_property_descriptor -----------------------------------------------

    def test_get_property_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_property_descriptor(kb)

    def test_get_property_descriptor_single_property(self):
        kb = Store('mixer', [self.kb_benzene, self.kb_instance_of])
        ds = list(kb.get_property_descriptor(wd.instance_of))
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0][0], wd.instance_of)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_property_descriptor(
            ds[0][1], *INSTANCE_OF_TTL.instance_of_en)

    def test_get_property_descriptor_single_property_with_merges(self):
        kb = Store('mixer', [self.kb_extra, self.kb_instance_of])
        ds = list(kb.get_property_descriptor(wd.instance_of))
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0][0], wd.instance_of)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_property_descriptor(
            ds[0][1],
            INSTANCE_OF_TTL.instance_of_en[0],
            TextSet(*INSTANCE_OF_TTL.instance_of_en[1],
                    *self.extra_instance_of_en[1]),
            INSTANCE_OF_TTL.instance_of_en[2],
            INSTANCE_OF_TTL.instance_of_en[3])

    def test_get_property_descriptor_multiple_properties(self):
        kb = Store('mixer', [self.kb_benzene, self.kb_instance_of])
        ds = list(kb.get_property_descriptor(
            [wd.instance_of, Property('x'), wd.InChIKey]))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.instance_of)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_property_descriptor(
            ds[0][1], *INSTANCE_OF_TTL.instance_of_en)
        self.assertEqual(ds[1][0], Property('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.InChIKey)
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_property_descriptor(ds[2][1], *BENZENE_TTL.InChIKey_en)

    def test_get_property_descriptor_multiple_properties_with_merges(self):
        kb = Store(
            'mixer', [self.kb_extra, self.kb_benzene, self.kb_instance_of])
        ds = list(kb.get_property_descriptor(
            [wd.instance_of, Property('x'), wd.InChIKey]))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.instance_of)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_property_descriptor(
            ds[0][1],
            INSTANCE_OF_TTL.instance_of_en[0],
            TextSet(*INSTANCE_OF_TTL.instance_of_en[1],
                    *self.extra_instance_of_en[1]),
            *INSTANCE_OF_TTL.instance_of_en[2:])
        self.assertEqual(ds[1][0], Property('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.InChIKey)
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_property_descriptor(ds[2][1], *BENZENE_TTL.InChIKey_en)

    def test_get_property_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21):
            ds = list(kb.get_property_descriptor(
                [wd.instance_of, Property('x'),
                 wd.InChIKey, wd.instance_of], 'es', mask))
            self.assertEqual(len(ds), 4)
            self.assertEqual(ds[0][0], wd.instance_of)
            self.assert_property_descriptor(ds[0][1], *desc01)
            self.assertEqual(ds[1][0], Property('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.InChIKey)
            self.assert_property_descriptor(ds[2][1], *desc21)
            self.assertEqual(ds[3][0], wd.instance_of)
            self.assert_property_descriptor(ds[3][1], *desc01)
        kb = Store(
            'mixer', [self.kb_extra, self.kb_benzene, self.kb_instance_of])
        test_case(
            kb, 0,
            PropertyDescriptor(),
            PropertyDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            PropertyDescriptor(self.extra_instance_of_es[0]),
            PropertyDescriptor(BENZENE_TTL.InChIKey_es[0]))
        test_case(
            kb, Descriptor.ALIASES,
            PropertyDescriptor(None, TextSet(
                *self.extra_instance_of_es[1],
                *INSTANCE_OF_TTL.instance_of_es[1])),
            PropertyDescriptor(None, BENZENE_TTL.InChIKey_es[1]))
        test_case(
            kb, Descriptor.DESCRIPTION,
            PropertyDescriptor(
                None, None, INSTANCE_OF_TTL.instance_of_es[2]),
            PropertyDescriptor(
                None, None, BENZENE_TTL.InChIKey_es[2]))
        test_case(
            kb, Descriptor.LABEL | Descriptor.ALIASES,
            PropertyDescriptor(self.extra_instance_of_es[0], TextSet(
                *self.extra_instance_of_es[1],
                *INSTANCE_OF_TTL.instance_of_es[1])),
            PropertyDescriptor(
                BENZENE_TTL.InChIKey_es[0], BENZENE_TTL.InChIKey_es[1]))
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
            PropertyDescriptor(
                self.extra_instance_of_es[0], TextSet(
                    *self.extra_instance_of_es[1],
                    *INSTANCE_OF_TTL.instance_of_es[1]),
                *self.extra_instance_of_es[2:]),
            PropertyDescriptor(*BENZENE_TTL.InChIKey_es))
        # reset
        kb.set_flags(kb.EARLY_FILTER | kb.LATE_FILTER)

# -- get_lexeme_descriptor -----------------------------------------------

    def test_get_lexeme_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_lexeme_descriptor(kb)

    def test_get_lexeme_descriptor_single_lexeme(self):
        kb = Store('mixer', [self.kb_andar, self.kb_paint])
        ds = list(kb.get_lexeme_descriptor(wd.L(96)))
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0][0], wd.L(96))
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_lexeme_descriptor(ds[0][1], *PAINT_TTL.paint_verb_en)

    def test_get_lexeme_descriptor_multiple_lexemes(self):
        kb = Store('mixer', [self.kb_andar, self.kb_extra, self.kb_paint])
        ds = list(kb.get_lexeme_descriptor(
            [wd.L(96), Lexeme('x'), wd.L(46803)]))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.L(96))
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_lexeme_descriptor(ds[0][1], *PAINT_TTL.paint_verb_en)
        self.assertEqual(ds[1][0], Lexeme('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.L(46803))
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_lexeme_descriptor(ds[2][1], *ANDAR_TTL.andar_verb_pt)

    def test_get_lexeme_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21):
            ds = list(kb.get_lexeme_descriptor(
                [wd.L(96), Lexeme('x'), wd.L(46803)], mask))
            self.assertEqual(len(ds), 3)
            self.assertEqual(ds[0][0], wd.L(96))
            self.assert_lexeme_descriptor(ds[0][1], *desc01)
            self.assertEqual(ds[1][0], Lexeme('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.L(46803))
            self.assert_lexeme_descriptor(ds[2][1], *desc21)
        kb = Store('mixer', [self.kb_andar, self.kb_paint])
        test_case(
            kb, 0,
            LexemeDescriptor(),
            LexemeDescriptor())
        test_case(
            kb, Descriptor.LEMMA,
            LexemeDescriptor(PAINT_TTL.paint_verb_en[0]),
            LexemeDescriptor(ANDAR_TTL.andar_verb_pt[0]))
        test_case(
            kb, Descriptor.CATEGORY,
            LexemeDescriptor(None, PAINT_TTL.paint_verb_en[1]),
            LexemeDescriptor(None, ANDAR_TTL.andar_verb_pt[1]))
        test_case(
            kb, Descriptor.LANGUAGE,
            LexemeDescriptor(None, None, PAINT_TTL.paint_verb_en[2]),
            LexemeDescriptor(None, None, ANDAR_TTL.andar_verb_pt[2]))
        test_case(
            kb, Descriptor.LEMMA,
            LexemeDescriptor(PAINT_TTL.paint_verb_en[0]),
            LexemeDescriptor(ANDAR_TTL.andar_verb_pt[0]))
        test_case(
            kb, Descriptor.LEMMA | Descriptor.LANGUAGE,
            LexemeDescriptor(
                PAINT_TTL.paint_verb_en[0], None, PAINT_TTL.paint_verb_en[2]),
            LexemeDescriptor(
                ANDAR_TTL.andar_verb_pt[0], None, ANDAR_TTL.andar_verb_pt[2]))
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
            LexemeDescriptor(*PAINT_TTL.paint_verb_en),
            LexemeDescriptor(*ANDAR_TTL.andar_verb_pt))
        # reset
        kb.set_flags(kb.EARLY_FILTER | kb.LATE_FILTER)


if __name__ == '__main__':
    TestStoreMixerDescriptors.main()
