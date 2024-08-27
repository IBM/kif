# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    ItemDescriptor,
    Lexeme,
    LexemeDescriptor,
    Property,
    PropertyDescriptor,
    Text,
)
from kif_lib.vocabulary import wd

from .tests import WikidataSPARQL_StoreTestCase


class TestStoreSPARQL_SPARQL_StoreDescriptors(WikidataSPARQL_StoreTestCase):

    def test_get_descriptor_sanity(self) -> None:
        kb = self.new_Store()
        self.sanity_check_get_descriptor(kb)

    def test_get_descriptor_single_entity(self) -> None:
        kb = self.new_Store()
        ds = list(kb.get_descriptor(wd.IBM))
        self.assertEqual(len(ds), 1)
        ((item, desc),) = ds
        self.assertEqual(item, wd.IBM)
        self.assertIsNotNone(desc)
        self.assertIsInstance(desc, ItemDescriptor)
        assert isinstance(desc, ItemDescriptor)
        self.assertEqual(desc.label, Text('IBM'))
        self.assertIn(Text('I.B.M.'), desc.aliases)
        self.assertEqual(
            desc.description,
            Text('American multinational technology corporation'))

    def test_get_descriptor_multiple_entities(self) -> None:
        kb = self.new_Store()
        ds = list(kb.get_descriptor([
            wd.IBM, Item('x'),
            wd.L(4471), Lexeme('x'),
            wd.mass, Property('x')]))
        self.assertEqual(len(ds), 6)
        self.assertEqual(ds[0][0], wd.IBM)
        self.assertIsInstance(ds[0][1], ItemDescriptor)
        assert isinstance(ds[0][1], ItemDescriptor)
        self.assertEqual(ds[0][1].label, Text('IBM'))
        self.assertIn(Text('I.B.M.'), ds[0][1].aliases)
        self.assertEqual(ds[0][1].description, Text(
            'American multinational technology corporation'))
        self.assertEqual(ds[1][0], Item('x'))
        self.assertIsNone(ds[1][1])
        self.assertEqual(ds[2][0], wd.L(4471))
        self.assertIsInstance(ds[2][1], LexemeDescriptor)
        assert isinstance(ds[2][1], LexemeDescriptor)
        self.assertEqual(ds[2][1].lemma, Text('love'))
        self.assertEqual(ds[2][1].category, wd.verb)
        self.assertEqual(ds[2][1].language, wd.English)
        self.assertEqual(ds[3][0], Lexeme('x'))
        self.assertIsNone(ds[3][1])
        self.assertEqual(ds[4][0], wd.mass)
        self.assertIsInstance(ds[4][1], PropertyDescriptor)
        assert isinstance(ds[4][1], PropertyDescriptor)
        self.assertEqual(ds[4][1].label, Text('mass'))
        self.assertIn(Text('molecular weight'), ds[4][1].aliases)
        self.assertEqual(ds[4][1].description, Text(
            'mass (in colloquial usage also known as weight) of the item'))
        self.assertEqual(ds[5][0], Property('x'))
        self.assertIsNone(ds[5][1])


if __name__ == '__main__':
    TestStoreSPARQL_SPARQL_StoreDescriptors.main()
