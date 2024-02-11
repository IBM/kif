# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, ItemDescriptor, Text, TextSet

from .tests import kif_TestCase, main


class TestItemDescriptor(kif_TestCase):

    def test__init__(self):
        # bad arguments
        self.assertRaises(TypeError, ItemDescriptor, 0)
        self.assertRaises(TypeError, ItemDescriptor, 'x', 0)
        self.assertRaises(TypeError, ItemDescriptor, 'x', [], 0)
        self.assertRaises(TypeError, ItemDescriptor, 0, [], IRI('z'))
        # good arguments
        self.assert_item_descriptor(ItemDescriptor(), None, TextSet(), None)
        self.assert_item_descriptor(
            ItemDescriptor('x', ['a', 'b', 'c'], 'z'),
            Text('x'), list(map(Text, ['a', 'b', 'c'])), Text('z'))

    def test_get_label(self):
        self.assertEqual(ItemDescriptor('x').get_label(), Text('x'))
        self.assertEqual(ItemDescriptor().get_label(Text('x')), Text('x'))
        self.assertIsNone(ItemDescriptor().get_label())

    def test_get_aliases(self):
        self.assertEqual(ItemDescriptor('x').get_aliases(), TextSet())
        self.assertEqual(ItemDescriptor(
            None, ['x', 'y']).get_aliases(), TextSet(Text('x'), Text('y')))

    def test_get_description(self):
        self.assertEqual(
            ItemDescriptor(None, None, 'x').get_description(), Text('x'))
        self.assertEqual(
            ItemDescriptor().get_description(Text('x')), Text('x'))
        self.assertIsNone(ItemDescriptor().get_description())


if __name__ == '__main__':
    main()
