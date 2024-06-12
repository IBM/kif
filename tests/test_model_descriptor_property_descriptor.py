# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    IRI_Datatype,
    PropertyDescriptor,
    Text,
    TextDatatype,
    TextSet,
)

from .tests import kif_TestCase


class TestModelDescriptorPropertyDescriptor(kif_TestCase):

    def test__init__(self):
        # bad arguments
        self.assertRaises(TypeError, PropertyDescriptor, 0)
        self.assertRaises(TypeError, PropertyDescriptor, 'x', 0)
        self.assertRaises(TypeError, PropertyDescriptor, None, 0)
        self.assertRaises(TypeError, PropertyDescriptor, 'x', [], 0)
        self.assertRaises(TypeError, PropertyDescriptor, 'x', None, 0)
        self.assertRaises(
            TypeError, PropertyDescriptor, 0, [], TextDatatype())
        self.assertRaises(TypeError, PropertyDescriptor, 0, [], None, 0)
        self.assertRaises(
            TypeError, PropertyDescriptor, None, None, None, 'x')
        # good arguments
        self.assert_property_descriptor(
            PropertyDescriptor(), None, TextSet(), None, None)
        self.assert_property_descriptor(
            PropertyDescriptor(
                'x', TextSet('a', 'b', 'c'), 'z', Text.datatype),
            Text('x'), TextSet(Text('a'), Text('b'), Text('c')),
            Text('z'), TextDatatype())

    def test_get_label(self):
        self.assertEqual(PropertyDescriptor('x').get_label(), Text('x'))
        self.assertEqual(PropertyDescriptor().get_label(Text('x')), Text('x'))
        self.assertIsNone(PropertyDescriptor().get_label())

    def test_get_aliases(self):
        self.assertEqual(PropertyDescriptor('x').get_aliases(), TextSet())
        self.assertEqual(
            PropertyDescriptor(None, TextSet('x', 'y')).get_aliases(),
            TextSet(Text('x'), Text('y')))

    def test_get_description(self):
        self.assertEqual(
            PropertyDescriptor(None, None, 'x').get_description(), Text('x'))
        self.assertEqual(
            PropertyDescriptor().get_description(Text('x')), Text('x'))
        self.assertIsNone(PropertyDescriptor().get_description())

    def test_get_datatype(self):
        self.assertEqual(
            PropertyDescriptor(
                None, None, None, IRI_Datatype()).get_datatype(),
            IRI_Datatype())
        self.assertEqual(
            PropertyDescriptor(
                None, None, None, IRI.datatype).get_datatype(),
            IRI_Datatype())
        self.assertEqual(
            PropertyDescriptor().get_datatype(IRI_Datatype()),
            IRI_Datatype())
        self.assertIsNone(PropertyDescriptor().get_datatype())


if __name__ == '__main__':
    TestModelDescriptorPropertyDescriptor.main()
