# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import Datatype, Item, ItemDescriptor, Store, Text, TextSet

from .data import ADAM_TTL, BENZENE_TTL, BRAZIL_TTL, INSTANCE_OF_TTL
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

    Brazil_en = (
        Text('Brazil'),
        TextSet(),
        Text('country in South America'))

    Brazil_pt_br = (
        Text('Brasil', 'pt-br'),
        TextSet(Text('🇧🇷', 'pt-br'), Text('pindorama', 'pt-br')),
        Text('país na América do Sul', 'pt-br'))

    instance_of_en = (
        Text('instance of'),
        TextSet(
            Text('is a'), Text('type'), Text('is of type'), Text('has type')),
        Text('that class of which this subject is a particular example '
             'and member; different from P279 (subclass of); for example: '
             'K2 is an instance of mountain; volcano is a subclass of '
             'mountain (and an instance of volcanic landform)'),
        Datatype.item)

    Latin_America_pt_br = (
        None,
        TextSet(),
        None)

# -- get_item_descriptor ---------------------------------------------------

    def test_get_item_descriptor_sanity(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self.sanity_check_get_item_descriptor(kb)

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

    def test_get_item_descriptor_mask_zero(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ds = list(kb.get_item_descriptor(
            [wd.Brazil, Item('x'), wd.Latin_America], None, 0))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assertEqual(ds[0][1], ItemDescriptor())
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Latin_America)
        self.assertEqual(ds[2][1], ItemDescriptor())

    def test_get_item_descriptor_mask_label(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ds = list(kb.get_item_descriptor(
            [wd.Brazil, Item('x'), wd.Latin_America],
            None, ItemDescriptor.LABEL))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assert_item_descriptor(ds[0][1], self.Brazil_en[0], [], None)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Latin_America)
        self.assert_item_descriptor(ds[2][1], Text('Latin America'), [], None)

    def test_get_item_descriptor_mask_aliases(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ds = list(kb.get_item_descriptor(
            [wd.Brazil, Item('x'), wd.Latin_America],
            'pt-br', ItemDescriptor.ALIASES))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assert_item_descriptor(
            ds[0][1], None, self.Brazil_pt_br[1], None)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Latin_America)
        self.assert_item_descriptor(
            ds[2][1], None, self.Latin_America_pt_br[1], None)

    def test_get_item_descriptor_description(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ds = list(kb.get_item_descriptor(
            [wd.Brazil, Item('x'), wd.Latin_America],
            'pt-br', ItemDescriptor.DESCRIPTION))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assert_item_descriptor(
            ds[0][1], None, [], self.Brazil_pt_br[2])
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Latin_America)
        self.assert_item_descriptor(
            ds[2][1], None, [], self.Latin_America_pt_br[2])

    def test_get_item_descriptor_many(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        ds = list(kb.get_item_descriptor(
            [wd.Brazil, Item('x'), wd.Latin_America],
            'pt-br', ItemDescriptor.LABEL | ItemDescriptor.DESCRIPTION))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Brazil)
        self.assert_item_descriptor(
            ds[0][1], self.Brazil_pt_br[0], [], self.Brazil_pt_br[2])
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Latin_America)
        self.assert_item_descriptor(
            ds[2][1], self.Latin_America_pt_br[0], [],
            self.Latin_America_pt_br[2])

    def test_get_item_descriptor_no_label(self):
        kb = self.parse(r'''
wd:Q_empty
    schema:version 0 ;
    #rdfs:label "lll"@en ;
    skos:altLabel "xxx"@en ;
    skos:altLabel "yyy"@en ;
    skos:altLabel "zzz"@fr ;
    schema:description "aaa"@en ;
    schema:description "bbb"@fr .
''')
        ((item, desc),) = list(kb.get_item_descriptor(wd.Q('_empty')))
        self.assertEqual(item, wd.Q('_empty'))
        self.assert_item_descriptor(
            desc, None, [Text('xxx'), Text('yyy')], Text('aaa'))

    def test_get_item_descriptor_no_aliases(self):
        kb = self.parse(r'''
wd:Q_empty
    schema:version 0 ;
    rdfs:label "lll"@en ;
    #skos:altLabel "xxx"@en ;
    #skos:altLabel "yyy"@en ;
    #skos:altLabel "zzz"@fr ;
    schema:description "aaa"@en ;
    schema:description "bbb"@fr .
''')
        ((item, desc),) = list(kb.get_item_descriptor(wd.Q('_empty')))
        self.assertEqual(item, wd.Q('_empty'))
        self.assert_item_descriptor(desc, Text('lll'), [], Text('aaa'))

    def test_get_item_descriptor_no_description(self):
        kb = self.parse(r'''
wd:Q_empty
    schema:version 0 ;
    rdfs:label "lll"@en ;
    skos:altLabel "xxx"@en ;
    skos:altLabel "yyy"@en ;
    skos:altLabel "zzz"@fr .
    #schema:description "aaa"@en ;
    #schema:description "bbb"@fr .
''')
        ((item, desc),) = list(kb.get_item_descriptor(wd.Q('_empty')))
        self.assertEqual(item, wd.Q('_empty'))
        self.assert_item_descriptor(
            desc, Text('lll'), [Text('xxx'), Text('yyy')], None)

    def test_get_item_descriptor_no_label_aliases_description(self):
        kb = self.parse('wd:Q_empty schema:version 0 .')
        ((item, desc),) = list(kb.get_item_descriptor(wd.Q('_empty')))
        self.assertEqual(item, wd.Q('_empty'))
        self.assertEqual(desc, ItemDescriptor())

# -- get_property_descriptor -----------------------------------------------

    def test_get_property_descriptor_sanity(self):
        kb = Store('rdf', INSTANCE_OF_TTL)
        self.sanity_check_get_property_descriptor(kb)

    def test_get_property_descriptor_single_item(self):
        kb = Store('rdf', BENZENE_TTL, INSTANCE_OF_TTL)
        ((item, desc),) = kb.get_property_descriptor(wd.instance_of)
        self.assertEqual(item, wd.instance_of)
        self.assert_property_descriptor(desc, *self.instance_of_en)

# -- get_lexeme_descriptor -------------------------------------------------

    def test_get_lexeme_descriptor_sanity(self):
        kb = Store('rdf', ADAM_TTL, BENZENE_TTL, BRAZIL_TTL)
        self.sanity_check_get_lexeme_descriptor(kb)


if __name__ == '__main__':
    main()
