# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    ItemDescriptor,
    LexemeDescriptor,
    PropertyDescriptor,
    String,
    Text,
    TextSet,
)
from kif_lib.typing import assert_type, Optional

from ...tests import DescriptorTestCase


class Test(DescriptorTestCase):

    def test_check(self) -> None:
        assert_type(ItemDescriptor.check(ItemDescriptor()), ItemDescriptor)
        self._test_check(
            ItemDescriptor,
            success=[
                (ItemDescriptor(), ItemDescriptor()),
                (ItemDescriptor('x'), ItemDescriptor(Text('x'))),
                (ItemDescriptor(None, ['x', 'y']),
                 ItemDescriptor(None, TextSet('x', 'y'))),
                (ItemDescriptor(None, None, 'z'),
                 ItemDescriptor(None, None, Text('z'))),
            ],
            failure=[LexemeDescriptor(), PropertyDescriptor()])

    def test__init__(self) -> None:
        assert_type(ItemDescriptor(), ItemDescriptor)
        self._test__init__(
            ItemDescriptor,
            self.assert_item_descriptor,
            success=[
                ([], ItemDescriptor()),
                ([ExternalId('x'), ['y', String('z')], Text('w')],
                 ItemDescriptor('x', ['y', 'z'], 'w')),
                ([Text('x', 'es'), None, Text('y', 'es')],
                 ItemDescriptor(Text('x', 'es'), None, Text('y', 'es'))),
            ])

    def test_get_label(self) -> None:
        assert_type(ItemDescriptor().label, Optional[Text])
        assert_type(ItemDescriptor().get_label(), Optional[Text])
        self.assertEqual(ItemDescriptor('x').get_label(), Text('x'))
        self.assertEqual(ItemDescriptor().get_label(Text('x')), Text('x'))
        self.assertIsNone(ItemDescriptor().get_label())

    def test_get_aliases(self) -> None:
        assert_type(ItemDescriptor().aliases, TextSet)
        assert_type(ItemDescriptor().get_aliases(), TextSet)
        self.assertEqual(ItemDescriptor('x').get_aliases(), TextSet())
        self.assertEqual(
            ItemDescriptor(None, TextSet('x', 'y')).get_aliases(),
            TextSet(Text('x'), Text('y')))

    def test_get_description(self) -> None:
        assert_type(ItemDescriptor().description, Optional[Text])
        assert_type(ItemDescriptor().get_description(), Optional[Text])
        self.assertEqual(
            ItemDescriptor(None, None, 'x').get_description(), Text('x'))
        self.assertEqual(
            ItemDescriptor().get_description(Text('x')), Text('x'))
        self.assertIsNone(ItemDescriptor().get_description())


if __name__ == '__main__':
    Test.main()
