# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Descriptor,
    Item,
    ItemDatatype,
    ItemDescriptor,
    Lexeme,
    LexemeDescriptor,
    Property,
    PropertyDescriptor,
    Text,
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
from .tests import kif_RDF_StoreTestCase


class TestStoreRDF_Descriptors(kif_RDF_StoreTestCase):

    def test_get_descriptor_sanity(self):
        kb = self.new_Store(BENZENE_TTL, INSTANCE_OF_TTL, PAINT_TTL)
        self.sanity_check_get_descriptor(kb)

    def test_get_descriptor_single_entity(self):
        kb = self.new_Store(ADAM_TTL, INSTANCE_OF_TTL, PAINT_TTL)
        ((item, desc),) = kb.get_descriptor(wd.Adam)
        self.assertEqual(item, wd.Adam)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *ADAM_TTL.Adam_en)
        ((prop, desc),) = kb.get_descriptor(wd.instance_of)
        self.assertEqual(prop, wd.instance_of)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_property_descriptor(desc, *INSTANCE_OF_TTL.instance_of_en)
        ((lexeme, desc),) = kb.get_descriptor(wd.L(96))
        self.assertEqual(lexeme, wd.L(96))
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_lexeme_descriptor(desc, *PAINT_TTL.paint_verb_en)

    def test_get_descriptor_multiple_entities(self):
        kb = self.new_Store(ADAM_TTL, INSTANCE_OF_TTL, PAINT_TTL)
        ds = list(kb.get_descriptor(
            [wd.Adam,
             Item('x'),
             wd.instance_of,
             Property('y'),
             wd.L(96),
             wd.L('z')], 'es'))
        self.assertEqual(len(ds), 6)
        self.assertEqual(ds[0][0], wd.Adam)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(ds[0][1], *ADAM_TTL.Adam_es)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.instance_of)
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_property_descriptor(
            ds[2][1], *INSTANCE_OF_TTL.instance_of_es)
        self.assertEqual(ds[3][0], Property('y'))
        self.assertIsNone(ds[3][1])
        self.assertEqual(ds[4][0], wd.L(96))
        self.assertIsNotNone(ds[4][1])
        assert ds[4][1] is not None
        self.assert_lexeme_descriptor(ds[4][1], *PAINT_TTL.paint_verb_en)
        self.assertEqual(ds[5][0], wd.L('z'))
        self.assertIsNone(ds[5][1])

    def test_get_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21, desc41):
            ds = list(kb.get_descriptor(
                [wd.Adam,
                 Item('x'),
                 wd.instance_of,
                 Property('y'),
                 wd.L(96),
                 wd.L('z')], None, mask))
            self.assertEqual(len(ds), 6)
            self.assertEqual(ds[0][0], wd.Adam)
            self.assert_item_descriptor(ds[0][1], *desc01)
            self.assertEqual(ds[1][0], Item('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.instance_of)
            self.assert_property_descriptor(ds[2][1], *desc21)
            self.assertEqual(ds[3][0], Property('y'))
            self.assertIsNone(ds[3][1])
            self.assertEqual(ds[4][0], wd.L(96))
            self.assert_lexeme_descriptor(ds[4][1], *desc41)
            self.assertEqual(ds[5][0], wd.L('z'))
            self.assertIsNone(ds[5][1])
        kb = self.new_Store(ADAM_TTL, INSTANCE_OF_TTL, PAINT_TTL)
        test_case(
            kb, 0,
            ItemDescriptor(),
            PropertyDescriptor(),
            LexemeDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            ItemDescriptor(ADAM_TTL.Adam_en[0]),
            PropertyDescriptor(INSTANCE_OF_TTL.instance_of_en[0]),
            LexemeDescriptor())
        test_case(
            kb, Descriptor.ALIASES | Descriptor.LEMMA,
            ItemDescriptor(None, ADAM_TTL.Adam_en[1]),
            PropertyDescriptor(None, INSTANCE_OF_TTL.instance_of_en[1]),
            LexemeDescriptor(PAINT_TTL.paint_verb_en[0]))
        test_case(
            kb,
            Descriptor.DESCRIPTION | Descriptor.CATEGORY | Descriptor.LANGUAGE,
            ItemDescriptor(None, None, ADAM_TTL.Adam_en[2]),
            PropertyDescriptor(None, None, INSTANCE_OF_TTL.instance_of_en[2]),
            LexemeDescriptor(
                None, PAINT_TTL.paint_verb_en[1], PAINT_TTL.paint_verb_en[2]))
        test_case(
            kb, Descriptor.ALIASES | Descriptor.LEMMA,
            ItemDescriptor(None, ADAM_TTL.Adam_en[1]),
            PropertyDescriptor(None, INSTANCE_OF_TTL.instance_of_en[1]),
            LexemeDescriptor(PAINT_TTL.paint_verb_en[0]))
        # no early filter
        kb.unset_flags(kb.EARLY_FILTER)
        test_case(
            kb, 0,
            ItemDescriptor(),
            PropertyDescriptor(),
            LexemeDescriptor())
        # no late filter
        kb.unset_flags(kb.LATE_FILTER)
        test_case(
            kb, 0,
            ItemDescriptor(*ADAM_TTL.Adam_en),
            PropertyDescriptor(*INSTANCE_OF_TTL.instance_of_en),
            LexemeDescriptor(*PAINT_TTL.paint_verb_en))

# -- get_item_descriptor ---------------------------------------------------

    def test_get_item_descriptor_sanity(self):
        kb = self.new_Store(ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self.sanity_check_get_item_descriptor(kb)

    def test_get_item_descriptor_single_item(self):
        kb = self.new_Store(ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ((item, desc),) = kb.get_item_descriptor(wd.Adam)
        self.assertEqual(item, wd.Adam)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *ADAM_TTL.Adam_en)

    def test_get_item_descriptor_multiple_items(self):
        kb = self.new_Store(ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
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

    def test_get_item_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21):
            ds = list(kb.get_item_descriptor(
                [wd.Brazil, Item('x'), wd.Latin_America], None, mask))
            self.assertEqual(len(ds), 3)
            self.assertEqual(ds[0][0], wd.Brazil)
            self.assertEqual(ds[0][1], desc01)
            self.assertEqual(ds[1][0], Item('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.Latin_America)
            self.assertEqual(ds[2][1], desc21)
        kb = self.new_Store(ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        test_case(
            kb, 0,
            ItemDescriptor(),
            ItemDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            ItemDescriptor(BRAZIL_TTL.Brazil_en[0]),
            ItemDescriptor(BRAZIL_TTL.Latin_America_en[0]))
        test_case(
            kb, Descriptor.ALIASES,
            ItemDescriptor(None, BRAZIL_TTL.Brazil_en[1]),
            ItemDescriptor(None, BRAZIL_TTL.Latin_America_en[1]))
        test_case(
            kb, Descriptor.DESCRIPTION,
            ItemDescriptor(None, None, BRAZIL_TTL.Brazil_en[2]),
            ItemDescriptor(None, None, BRAZIL_TTL.Latin_America_en[2]))
        test_case(
            kb, Descriptor.ALIASES | Descriptor.DESCRIPTION | Descriptor.LEMMA,
            ItemDescriptor(
                None, BRAZIL_TTL.Brazil_en[1], BRAZIL_TTL.Brazil_en[2]),
            ItemDescriptor(
                None, BRAZIL_TTL.Latin_America_en[1],
                BRAZIL_TTL.Latin_America_en[2]))
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
            ItemDescriptor(*BRAZIL_TTL.Brazil_en),
            ItemDescriptor(*BRAZIL_TTL.Latin_America_en))

    def test_get_item_descriptor_missing_attribute(self):
        def test_case(comments, desc):
            lines = [
                'wikibase:sitelinks []',
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
        kb = self.new_Store(INSTANCE_OF_TTL)
        self.sanity_check_get_property_descriptor(kb)

    def test_get_property_descriptor_single_property(self):
        kb = self.new_Store(BENZENE_TTL, INSTANCE_OF_TTL)
        ((prop, desc),) = kb.get_property_descriptor(wd.instance_of)
        self.assertEqual(prop, wd.instance_of)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_property_descriptor(desc, *INSTANCE_OF_TTL.instance_of_en)

    def test_get_property_descriptor_multiple_properties(self):
        kb = self.new_Store(BENZENE_TTL, INSTANCE_OF_TTL)
        ds = list(kb.get_property_descriptor(
            [wd.instance_of, Property('x'), wd.InChIKey], 'es'))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.instance_of)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_property_descriptor(
            ds[0][1], *INSTANCE_OF_TTL.instance_of_es)
        self.assertEqual(ds[1][0], Property('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.InChIKey)
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_property_descriptor(ds[2][1], *BENZENE_TTL.InChIKey_es)

    def test_get_property_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21):
            ds = list(kb.get_property_descriptor(
                [wd.instance_of, Property('x'), wd.InChIKey], None, mask))
            self.assertEqual(len(ds), 3)
            self.assertEqual(ds[0][0], wd.instance_of)
            self.assertEqual(ds[0][1], desc01)
            self.assertEqual(ds[1][0], Property('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.InChIKey)
            self.assertEqual(ds[2][1], desc21)
        kb = self.new_Store(BENZENE_TTL, INSTANCE_OF_TTL)
        test_case(
            kb, 0,
            PropertyDescriptor(),
            PropertyDescriptor())
        test_case(
            kb, Descriptor.LABEL,
            PropertyDescriptor(INSTANCE_OF_TTL.instance_of_en[0]),
            PropertyDescriptor(BENZENE_TTL.InChIKey_en[0]))
        test_case(
            kb, Descriptor.ALIASES,
            PropertyDescriptor(None, INSTANCE_OF_TTL.instance_of_en[1]),
            PropertyDescriptor(None, BENZENE_TTL.InChIKey_en[1]))
        test_case(
            kb, Descriptor.DESCRIPTION,
            PropertyDescriptor(None, None, INSTANCE_OF_TTL.instance_of_en[2]),
            PropertyDescriptor(None, None, BENZENE_TTL.InChIKey_en[2]))
        test_case(
            kb, Descriptor.DATATYPE,
            PropertyDescriptor(
                None, None, None, INSTANCE_OF_TTL.instance_of_en[3]),
            PropertyDescriptor(None, None, None, BENZENE_TTL.InChIKey_en[3]))
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
            PropertyDescriptor(*INSTANCE_OF_TTL.instance_of_en),
            PropertyDescriptor(*BENZENE_TTL.InChIKey_en))

    def test_get_property_descriptor_missing_attribute(self):
        def test_case(comments, desc):
            lines = [
                'a wikibase:Property',
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
                None, [Text('xxx'), Text('yyy')], Text('aaa'), ItemDatatype()))
        test_case(
            ['skos:altLabel'],
            PropertyDescriptor('lll', [], Text('aaa'), ItemDatatype()))
        test_case(
            ['schema:description'],
            PropertyDescriptor(
                'lll', [Text('xxx'), Text('yyy')], None, ItemDatatype()))

# -- get_lexeme_descriptor -------------------------------------------------

    def test_get_lexeme_descriptor_sanity(self):
        kb = self.new_Store(ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self.sanity_check_get_lexeme_descriptor(kb)

    def test_get_lexeme_descriptor_single_lexeme(self):
        kb = self.new_Store(PAINT_TTL)
        ((lex, desc),) = kb.get_lexeme_descriptor(wd.L(96))
        self.assertEqual(lex, wd.L(96))
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_lexeme_descriptor(desc, *PAINT_TTL.paint_verb_en)

    def test_get_lexeme_descriptor_multiple_lexemes(self):
        kb = self.new_Store(ANDAR_TTL, PAINT_TTL)
        ds = list(kb.get_lexeme_descriptor(
            [wd.L(46803), Lexeme('x'), wd.L(96)]))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.L(46803))
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_lexeme_descriptor(ds[0][1], *ANDAR_TTL.andar_verb_pt)
        self.assertEqual(ds[1][0], Lexeme('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.L(96))
        self.assertIsNotNone(ds[2][1])
        assert ds[2][1] is not None
        self.assert_lexeme_descriptor(ds[2][1], *PAINT_TTL.paint_verb_en)

    def test_get_lexeme_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc21):
            ds = list(kb.get_lexeme_descriptor(
                [wd.L(46803), Lexeme('x'), wd.L(96)], mask))
            self.assertEqual(len(ds), 3)
            self.assertEqual(ds[0][0], wd.L(46803))
            self.assertEqual(ds[0][1], desc01)
            self.assertEqual(ds[1][0], Lexeme('x'))
            self.assertIsNone(ds[1][1])
            self.assertEqual(ds[2][0], wd.L(96))
            self.assertEqual(ds[2][1], desc21)
        kb = self.new_Store(ANDAR_TTL, PAINT_TTL)
        test_case(
            kb, 0,
            LexemeDescriptor(),
            LexemeDescriptor())
        test_case(
            kb, Descriptor.LEMMA,
            LexemeDescriptor(ANDAR_TTL.andar_verb_pt[0]),
            LexemeDescriptor(PAINT_TTL.paint_verb_en[0]))
        test_case(
            kb, Descriptor.CATEGORY,
            LexemeDescriptor(None, ANDAR_TTL.andar_verb_pt[1]),
            LexemeDescriptor(None, PAINT_TTL.paint_verb_en[1]))
        test_case(
            kb, Descriptor.LANGUAGE,
            LexemeDescriptor(None, None, ANDAR_TTL.andar_verb_pt[2]),
            LexemeDescriptor(None, None, PAINT_TTL.paint_verb_en[2]))
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
            LexemeDescriptor(*ANDAR_TTL.andar_verb_pt),
            LexemeDescriptor(*PAINT_TTL.paint_verb_en))


if __name__ == '__main__':
    TestStoreRDF_Descriptors.main()
