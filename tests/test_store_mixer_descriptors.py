# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.vocabulary as wd
from kif_lib import Descriptor, Item, ItemDescriptor, Nil, Store, Text, TextSet

from .data import ADAM_TTL, BENZENE_TTL, BRAZIL_TTL, INSTANCE_OF_TTL
from .tests import kif_StoreTestCase, main


class TestStoreMixer_Descriptors(kif_StoreTestCase):

    kb_adam = Store('rdf', ADAM_TTL)
    kb_benzene = Store('rdf', BENZENE_TTL)
    kb_brazil = Store('rdf', BRAZIL_TTL)
    kb_instance_of = Store('rdf', INSTANCE_OF_TTL)

    kb_extra = kif_StoreTestCase.parse('''
# benzene
wd:Q2270

    # description
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

    # description
    schema:version "0"^^xsd:integer ;
    rdfs:label "Brazil"@en ;
    rdfs:label "Brasil"@pt-br ;
    skos:altLabel "🇧🇷"@en ;
    skos:altLabel "BRA"@pt-br .
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

    extra_Brazil_pt_br = ItemDescriptor(
        Text('Brasil', 'pt-br'), [Text('BRA', 'pt-br')])

# -- get_descriptor --------------------------------------------------------

    def test_get_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_descriptor(kb)

# -- get_item_descriptor ---------------------------------------------------

    def test_get_item_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_item_descriptor(kb)

    def test_get_item_descriptor_single_item(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene])
        res = list(kb.get_item_descriptor(wd.benzene))
        self.assertEqual(len(res), 1)
        item, desc = res[0]
        self.assertEqual(item, wd.benzene)
        self.assert_item_descriptor(desc, *BENZENE_TTL.benzene_en)

    def test_get_item_descriptor_single_item_with_merges(self):
        kb = Store('mixer', [self.kb_extra, self.kb_benzene])
        res = list(kb.get_item_descriptor(wd.benzene))
        self.assertEqual(len(res), 1)
        item, desc = res[0]
        self.assertEqual(item, wd.benzene)
        self.assert_item_descriptor(
            desc,
            BENZENE_TTL.benzene_en[0],
            [Text('C6H6'), *BENZENE_TTL.benzene_en[1]],
            self.extra_benzene_en.description)

    def test_get_item_descriptor_multiple_items(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        ds = list(kb.get_item_descriptor(
            [wd.Adam, Item('x'), wd.Brazil], 'pt-br'))
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds[0][0], wd.Adam)
        self.assert_item_descriptor(ds[0][1], *ADAM_TTL.Adam_pt_br)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Brazil)
        self.assert_item_descriptor(ds[2][1], *BRAZIL_TTL.Brazil_pt_br)

    def test_get_item_descriptor_multiple_items_with_merges(self):
        kb = Store('mixer', [
            self.kb_adam, self.kb_benzene, self.kb_extra, self.kb_brazil])
        ds = list(kb.get_item_descriptor(
            [wd.Adam, Item('x'), wd.Brazil, wd.benzene], 'pt-br'))
        self.assertEqual(len(ds), 4)
        self.assertEqual(ds[0][0], wd.Adam)
        self.assert_item_descriptor(ds[0][1], *ADAM_TTL.Adam_pt_br)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.Brazil)
        self.assert_item_descriptor(
            ds[2][1], BRAZIL_TTL.Brazil_pt_br[0],
            [*self.extra_Brazil_pt_br[1], *BRAZIL_TTL.Brazil_pt_br[1]],
            BRAZIL_TTL.Brazil_pt_br[2])
        self.assertEqual(ds[3][0], wd.benzene)
        self.assert_item_descriptor(ds[3][1], *self.extra_benzene_pt_br)

    def test_get_item_descriptor_mask(self):
        def test_case(kb, flags, desc01, desc21, desc31):
            ds = list(kb.get_item_descriptor(
                [wd.Adam, Item('x'), wd.Brazil, wd.benzene], 'pt-br', flags))
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

# -- get_property_descriptor -----------------------------------------------

    def test_get_property_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_property_descriptor(kb)

    def test_get_property_descriptor_single_item(self):
        kb = Store('mixer', [self.kb_benzene, self.kb_instance_of])
        res = list(kb.get_property_descriptor(wd.instance_of))
        self.assertEqual(len(res), 1)
        item, desc = res[0]
        self.assertEqual(item, wd.instance_of)
        self.assert_property_descriptor(
            desc, *INSTANCE_OF_TTL.instance_of_en)

# -- get_lexeme_descriptor -----------------------------------------------

    def test_get_lexeme_descriptor_sanity(self):
        kb = Store('mixer', [self.kb_adam, self.kb_benzene, self.kb_brazil])
        self.sanity_check_get_lexeme_descriptor(kb)


if __name__ == '__main__':
    main()
