# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Descriptor,
    Item,
    ItemDescriptor,
    LexemeDescriptor,
    PropertyDescriptor,
    Text,
    TextSet,
)
from kif_lib.typing import assert_type

from ...tests import DescriptorTestCase


class Test(DescriptorTestCase):

    def test_attribute_mask_check(self) -> None:
        self.assertRaisesRegex(
            TypeError, 'cannot coerce',
            Descriptor.AttributeMask.check, 'abc')
        self.assertRaisesRegex(
            ValueError, 'cannot coerce',
            Descriptor.AttributeMask.check, 777)
        self.assertEqual(
            Descriptor.AttributeMask.check(0),
            Descriptor.AttributeMask(0))
        self.assertEqual(
            Descriptor.AttributeMask.check(Descriptor.LABEL),
            Descriptor.AttributeMask.LABEL)
        self.assertEqual(
            Descriptor.AttributeMask.check_optional(
                None, Descriptor.AttributeMask.ALL),
            Descriptor.ALL)
        self.assertIsNone(Descriptor.AttributeMask.check_optional(None))

    def test_check(self) -> None:
        assert_type(Descriptor.check(LexemeDescriptor()), Descriptor)
        super()._test_check(
            Descriptor,
            success=[
                (ItemDescriptor('x'), ItemDescriptor(Text('x'))),
                (PropertyDescriptor(None, ['x']),
                 PropertyDescriptor(None, TextSet('x'))),
                (LexemeDescriptor('x', 'y'),
                 LexemeDescriptor(Text('x'), Item('y'))),
            ])


if __name__ == '__main__':
    Test.main()
