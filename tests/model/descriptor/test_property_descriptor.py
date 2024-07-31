# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    ItemDescriptor,
    LexemeDescriptor,
    PropertyDescriptor,
    Quantity,
    QuantityDatatype,
    String,
    Text,
    TextSet,
)
from kif_lib.typing import assert_type

from ...tests import kif_DescriptorTestCase


class Test(kif_DescriptorTestCase):

    def test_check(self) -> None:
        assert_type(
            PropertyDescriptor.check(PropertyDescriptor()), PropertyDescriptor)
        self._test_check(
            PropertyDescriptor,
            success=[
                (PropertyDescriptor(), PropertyDescriptor()),
                (PropertyDescriptor('x'), PropertyDescriptor(Text('x'))),
                (PropertyDescriptor(None, ['x', 'y']),
                 PropertyDescriptor(None, TextSet('x', 'y'))),
                (PropertyDescriptor(None, None, 'z'),
                 PropertyDescriptor(None, None, Text('z'))),
                (PropertyDescriptor(None, None, None, Item),
                 PropertyDescriptor(None, None, None, ItemDatatype())),
                (PropertyDescriptor('x', ['y', 'z'], 'w', QuantityDatatype()),
                 PropertyDescriptor(
                     'x', TextSet('z', 'y'), Text('w'), Quantity)),
            ],
            failure=[ItemDescriptor(), LexemeDescriptor()])

    def test__init__(self) -> None:
        assert_type(PropertyDescriptor(), PropertyDescriptor)
        self._test__init__(
            PropertyDescriptor,
            self.assert_property_descriptor,
            success=[
                ([], PropertyDescriptor()),
                ([None, None, None, Item],
                 PropertyDescriptor(datatype=ItemDatatype())),
                ([ExternalId('x'), ['y', String('z')], Text('w')],
                 PropertyDescriptor('x', ['y', 'z'], 'w')),
                ([Text('x', 'es'), None, Text('y', 'es'), Quantity],
                 PropertyDescriptor(
                     Text('x', 'es'), None, Text('y', 'es'),
                     Quantity.datatype)),
            ])

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
    Test.main()
