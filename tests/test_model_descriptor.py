# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import Descriptor, IRI, Text, TextSet

from .tests import kif_TestCase, main


class TestModelDescriptor(kif_TestCase):

    def test__init__(self):
        # bad arguments
        self.assertRaises(TypeError, Descriptor, 0)
        self.assertRaises(TypeError, Descriptor, 'x', 0)
        self.assertRaises(TypeError, Descriptor, 'x', [], 0)
        self.assertRaises(TypeError, Descriptor, 0, [], IRI('z'))
        # good arguments
        self.assert_descriptor(Descriptor(), None, TextSet(), None)
        self.assert_descriptor(
            Descriptor('x', ['a', 'b', 'c'], 'z'),
            Text('x'), list(map(Text, ['a', 'b', 'c'])), Text('z'))

    def test_get_label(self):
        self.assertEqual(Descriptor('x').get_label(), Text('x'))
        self.assertEqual(Descriptor().get_label(Text('x')), Text('x'))
        self.assertIsNone(Descriptor().get_label())

    def test_get_aliases(self):
        self.assertEqual(Descriptor('x').get_aliases(), TextSet())
        self.assertEqual(Descriptor(
            None, ['x', 'y']).get_aliases(), TextSet(Text('x'), Text('y')))

    def test_get_description(self):
        self.assertEqual(
            Descriptor(None, None, 'x').get_description(), Text('x'))
        self.assertEqual(Descriptor().get_description(Text('x')), Text('x'))
        self.assertIsNone(Descriptor().get_description())


if __name__ == '__main__':
    main()
