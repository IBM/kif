# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Descriptor,
    Item,
    ItemDescriptor,
    Lexeme,
    Property,
    Text,
    TextSet,
)
from kif_lib.store.mapping import PubChemMapping
from kif_lib.vocabulary import wd

from .tests import kif_PubChemSPARQL_StoreTestCase


class TestStoreMapperMappingPubChemDescriptors(
        kif_PubChemSPARQL_StoreTestCase):

    CID421 = PubChemMapping.compound('CID421')

    CID421_en = ItemDescriptor(
        Text('6,8-bis-sulfanyloctanoate', 'en'),
        TextSet(
            Text('516d485', 'en'),
            Text('6,8-bis(sulfanyl)octanoic acid', 'en'),
            Text('6,8-bis-sulfanyloctanoic acid', 'en'),
            Text('6,8-bismercaptooctanoic acid', 'en'),
            Text('6,8-dihydrothioctic acid', 'en'),
            Text('6,8-dimercapto octanoic acid', 'en'),
            Text('6,8-dimercapto-n-octanoic acid', 'en'),
            Text('6,8-dimercapto-octanoate', 'en'),
            Text('6,8-dimercapto-octanoic acid', 'en'),
            Text('6,8-dimercaptooctanoate', 'en'),
            Text('6,8-dimercaptooctanoic acid', 'en'),
            Text('6,8-disulfanyloctanoate', 'en'),
            Text('6,8-disulfanyloctanoic acid', 'en'),
            Text('bdbm16436', 'en'),
            Text('d,l-dihydrolipoate', 'en'),
            Text('d,l-dihydrolipoic acid', 'en'),
            Text('dhla', 'en'),
            Text('dihydro-a-lipoate', 'en'),
            Text('dihydro-a-lipoic acid', 'en'),
            Text('dihydro-alpha-lipoate', 'en'),
            Text('dihydro-alpha-lipoic acid', 'en'),
            Text('dihydro-dl-alpha-lipoate', 'en'),
            Text('dihydro-dl-alpha-lipoic acid', 'en'),
            Text('dihydro-lipoate', 'en'),
            Text('dihydro-lipoic acid', 'en'),
            Text('dihydro-thioctic acid', 'en'),
            Text('dihydro-thiocytic acid', 'en'),
            Text('dihydrolipoate', 'en'),
            Text('dihydrolipoic acid', 'en'),
            Text('dihydrolipoicacid', 'en'),
            Text('dihydrothioctic acid', 'en'),
            Text('dl-a-lipoic acid, dihydro-', 'en'),
            Text('dl-dihydro-a-6-thioctic acid', 'en'),
            Text('dl-dihydro-alpha-6-thioctic acid', 'en'),
            Text('ec 610-288-5', 'en'),
            Text('gamma-lipoic acid', 'en'),
            Text('gtpl6738', 'en'),
            Text('lipoic acid, dihydro-', 'en'),
            Text('lipoic acid, reduced, analytical standard', 'en'),
            Text('mfcd00166974', 'en'),
            Text('octanoic acid, 6,8-dimercapto-', 'en'),
            Text('reduced dl-6,8-thioctic acid', 'en'),
            Text('reduced lipoate', 'en'),
            Text('reduced lipoic acid', 'en'),
            Text('reduced thioctic acid', 'en'),
            Text('thioctic acid, dihydro-', 'en'),
            Text('usaf xr-12', 'en')),
        Text('A  thio-fatty acid that is reduced form of lipoic acid. '
             'A potent antioxidant shown to directly destroy superoxide, '
             'hydroperoxy and hydroxyl radicals; also has neuroprotective '
             'and anti-tumour effects.', 'en'))

    CID908 = PubChemMapping.compound('CID908')

    CID908_en = ItemDescriptor(
        None,
        TextSet(
            Text('2-(aminomethylideneamino)acetic acid', 'en'),
            Text('2-formimidamidoacetic acid', 'en'),
            Text('2-methanimidamidoacetic acid', 'en'),
            Text('[(iminomethyl)amino]acetic acid', 'en'),
            Text('formiminoglycine', 'en'),
            Text('glycine, n-(iminomethyl)-', 'en'),
            Text('n-(iminomethyl)glycine', 'en'),
            Text('n-formimidoylglycine', 'en'),
            Text('n-formiminoglycine', 'en')),
        Text('A glycine derivative that has formula C3H6N2O2.', 'en'))

    CID8822 = PubChemMapping.source('CID8822')

    CID8822_en = None           # not in PubChem

    AAA_Chemistry = PubChemMapping.source('AAA_Chemistry')

    AAA_Chemistry_en = ItemDescriptor(
        Text('AAA Chemistry', 'en'),
        TextSet(),
        None)

    ID15739 = PubChemMapping.source('ID15739')

    ID15739_en = ItemDescriptor(
        Text('15739', 'en'),
        TextSet(Text('DC Chemicals', 'en')),
        None)

    AR_017300_A1 = PubChemMapping.patent('AR-017300-A1')

    AR_017300_A1_en = ItemDescriptor(
        Text('A COMPOSITE DERIVED FROM 8-AZABICICLO [3.2.1] '
             'OCTAN-3-METHANAMINE, AND A MEDICINAL PRODUCT AND '
             'A PHARMACEUTICAL COMPOSITION THAT INCLUDES THAT '
             'DERIVATIVE.', 'en'),
        TextSet(),
        Text('A compound derived from 8-azabicyclo [3.2.1] '
             'octan-3-methanamine in the form of a pure geometric '
             'isomer or mixture of isomers, of general formula (I) '
             'in which U represents a group of general formula A) or B) '
             'in whose formulas V represents a hydrogen atom, a (C1-3) '
             'alkyl group or one or two (C1-3) alkoxy groups, W and X '
             'each represent, respectively, either two oxygen atoms or '
             'one oxygen atom and a CH2 group, or a CH2 group, and an '
             'oxygen atom and a CO group, represent the number 0 or 1, '
             'R represents either a propyl group when U represents a '
             'group of general formula (A), or an atom hydrogen or a '
             '(C1-3) alkyl group when U represents a group of general '
             'formula (B), Y represents one ovarian atoms or groups chosen '
             'from the following hydrogen, halogen, (C1-3) alkyl and (C1-3) '
             'alkoxy, Z represents two hydrogen atoms or an oxygen atom. '
             'A drug and a pharmaceutical composition comprising this '
             'derivative compound.The compounds can be used for the '
             'treatment of conditions and pathologies related to '
             'dysfunctions of the dopaminergic and serotonergic '
             'transmissions, in particular of the dopaminergic D2 and D3 '
             'and serotonergic receptors5-HT1A and 5- ht2. Therefore they '
             'can be used for the treatment of psychosis, particularly '
             'schizophrenia (deficit form and productive form) and acute '
             'or chronic extrapyramidal symptoms induced by neuroleptics, '
             'for the treatment of various forms of anxiety, panic attacks '
             ', of phobias of obsessive -compulsive disorders, '
             'for the treatment of different forms of depression, '
             'including psychotic depression, for the treatment of '
             'disorders due to alcohol abuse or withdrawal, sexual '
             'behavior disorders, food intake disorders, and for The '
             'treatment of migraine.', 'en'))

    DE_112011101181_T5 = PubChemMapping.patent('DE-112011101181-T5')

    DE_112011101181_T5_en = ItemDescriptor(
        Text('Control of Ferroelectricity in Dielectric Thin Films '
             'by Process Induced Monoaxial Voltages', 'en'),
        TextSet(),
        Text('A method of controlling the ferroelectric properties of '
             'the components of an integrated circuit device involves '
             'forming a ferroelectrically controllable dielectric layer '
             'on a substrate; and forming a stress applying structure '
             'near the ferroelectrically controllable dielectric layer '
             'such that a substantially monoaxial voltage is generated '
             'by the stressing structure in the ferroelectrically '
             'controllable dielectric layer; wherein the '
             'ferroelectrically-controllable dielectric layer '
             'comprises one or more of: a ferroelectric oxide layer '
             'and a layer of a normally non-ferroelectric material '
             'that has no ferroelectric properties in the absence of '
             'an applied voltage.', 'en'))

    def test_get_descriptor_sanity(self):
        kb = self.new_Store()
        self.sanity_check_get_descriptor(kb)

    def test_get_descriptor_single_entity(self):
        kb = self.new_Store()
        # item: compound
        ((item, desc),) = kb.get_descriptor(self.CID421)
        self.assertEqual(item, self.CID421)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *self.CID421_en)
        ((item, desc),) = kb.get_descriptor(self.CID421, 'pt')
        self.assertEqual(item, self.CID421)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *ItemDescriptor())
        ((item, desc),) = kb.get_descriptor(PubChemMapping.compound('CIDX'))
        self.assertEqual(item, PubChemMapping.compound('CIDX'))
        self.assertIsNone(desc)
        # item: patent
        ((item, desc),) = kb.get_descriptor(self.DE_112011101181_T5)
        self.assertEqual(item, self.DE_112011101181_T5)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *self.DE_112011101181_T5_en)
        ((item, desc),) = kb.get_descriptor(self.DE_112011101181_T5, 'pt')
        self.assertEqual(item, self.DE_112011101181_T5)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *ItemDescriptor())
        ((item, desc),) = kb.get_descriptor(PubChemMapping.patent('XXX'))
        self.assertEqual(item, PubChemMapping.patent('XXX'))
        self.assertIsNone(desc)
        # item: source
        ((item, desc),) = kb.get_descriptor(self.ID15739)
        self.assertEqual(item, self.ID15739)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *self.ID15739_en)
        ((item, desc),) = kb.get_descriptor(self.ID15739, 'pt')
        self.assertEqual(item, self.ID15739)
        self.assertIsNotNone(desc)
        assert desc is not None
        self.assert_item_descriptor(desc, *ItemDescriptor())
        ((item, desc),) = kb.get_descriptor(PubChemMapping.source('IDX'))
        self.assertEqual(item, PubChemMapping.source('IDX'))
        self.assertIsNone(desc)
        # property
        ((prop, desc),) = kb.get_descriptor(wd.instance_of)
        self.assertEqual(prop, wd.instance_of)
        self.assertIsNone(desc)
        # lexeme
        ((lexeme, desc),) = kb.get_descriptor(wd.L(96))
        self.assertEqual(lexeme, wd.L(96))
        self.assertIsNone(desc)

    def test_get_descriptor_multiple_entities(self):
        kb = self.new_Store()
        ds = list(kb.get_descriptor(
            [self.CID421,             # 0
             Item('x'),               # 1
             Property('p'),           # 2
             self.DE_112011101181_T5,  # 3
             Lexeme('l'),              # 4
             self.AAA_Chemistry,       # 5
             self.CID8822,             # 6
             self.CID908,              # 7
             self.AR_017300_A1,        # 8
             self.ID15739,             # 9
             self.CID421,              # 10
             Item('x')]))              # 11
        self.assertEqual(len(ds), 12)
        self.assertEqual(ds[0][0], self.CID421)
        self.assertIsNotNone(ds[0][1])
        assert ds[0][1] is not None
        self.assert_item_descriptor(ds[0][1], *self.CID421_en)
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], Property('p'))
        self.assertIsNone(ds[2][1])
        self.assertEqual(ds[3][0], self.DE_112011101181_T5)
        self.assertIsNotNone(ds[3][1])
        assert ds[3][1] is not None
        self.assert_item_descriptor(ds[3][1], *self.DE_112011101181_T5_en)
        self.assertEqual(ds[4][0], Lexeme('l'))
        self.assertIsNone(ds[4][1])
        self.assertEqual(ds[5][0], self.AAA_Chemistry)
        self.assertIsNotNone(ds[5][1])
        assert ds[5][1] is not None
        self.assert_item_descriptor(ds[5][1], *self.AAA_Chemistry_en)
        self.assertEqual(ds[6][0], self.CID8822)
        self.assertIsNone(ds[6][1])
        self.assertEqual(ds[7][0], self.CID908)
        self.assertIsNotNone(ds[7][1])
        assert ds[7][1] is not None
        self.assert_item_descriptor(ds[7][1], *self.CID908_en)
        self.assertEqual(ds[8][0], self.AR_017300_A1)
        self.assertIsNotNone(ds[8][1])
        assert ds[8][1] is not None
        self.assert_item_descriptor(ds[8][1], *self.AR_017300_A1_en)
        self.assertEqual(ds[9][0], self.ID15739)
        self.assertIsNotNone(ds[9][1])
        assert ds[9][1] is not None
        self.assert_item_descriptor(ds[9][1], *self.ID15739_en)
        self.assertEqual(ds[10][0], self.CID421)
        self.assertIsNotNone(ds[10][1])
        assert ds[10][1] is not None
        self.assert_item_descriptor(ds[10][1], *self.CID421_en)
        self.assertEqual(ds[11][0], Item('x'))
        self.assertIsNone(ds[11][1])

    def test_get_descriptor_mask(self):
        def test_case(kb, mask, desc01, desc11, desc21):
            ds = list(kb.get_descriptor(
                [self.CID421,                # 0
                 self.DE_112011101181_T5,    # 1
                 self.ID15739,               # 2
                 self.CID8822], None, mask))  # 3
            self.assertEqual(len(ds), 4)
            self.assertEqual(ds[0][0], self.CID421)
            self.assertEqual(ds[0][1], desc01)
            self.assertEqual(ds[1][0], self.DE_112011101181_T5)
            self.assertEqual(ds[1][1], desc11)
            self.assertEqual(ds[2][0], self.ID15739)
            self.assertEqual(ds[2][1], desc21)
            self.assertEqual(ds[3][0], self.CID8822)
            self.assertIsNone(ds[3][1])
        kb = self.new_Store()
        test_case(
            kb, 0,
            ItemDescriptor(),
            ItemDescriptor(),
            ItemDescriptor())
        test_case(
            kb, Descriptor.LABEL | Descriptor.LEMMA,
            ItemDescriptor(self.CID421_en[0]),
            ItemDescriptor(self.DE_112011101181_T5_en[0]),
            ItemDescriptor(self.ID15739_en[0]))
        test_case(
            kb, Descriptor.ALIASES | Descriptor.CATEGORY,
            ItemDescriptor(None, self.CID421_en[1]),
            ItemDescriptor(None, self.DE_112011101181_T5_en[1]),
            ItemDescriptor(None, self.ID15739_en[1]))
        test_case(
            kb, Descriptor.DESCRIPTION,
            ItemDescriptor(None, None, self.CID421_en[2]),
            ItemDescriptor(None, None, self.DE_112011101181_T5_en[2]),
            ItemDescriptor(None, None, self.ID15739_en[2]))
        test_case(
            kb, Descriptor.ALIASES | Descriptor.LABEL,
            ItemDescriptor(*self.CID421_en[:2]),
            ItemDescriptor(*self.DE_112011101181_T5_en[:2]),
            ItemDescriptor(*self.ID15739_en[:2]))


if __name__ == '__main__':
    TestStoreMapperMappingPubChemDescriptors.main()
