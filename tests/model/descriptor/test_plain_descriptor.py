# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ItemDescriptor,
    LexemeDescriptor,
    PlainDescriptor,
    PropertyDescriptor,
    Text,
    TextSet,
)
from kif_lib.typing import assert_type

from ...tests import DescriptorTestCase


class Test(DescriptorTestCase):

    def test_check(self) -> None:
        assert_type(PlainDescriptor.check(ItemDescriptor()), PlainDescriptor)
        super()._test_check(
            PlainDescriptor,
            success=[
                (ItemDescriptor('x'), ItemDescriptor(Text('x'))),
                (PropertyDescriptor(None, ['x']),
                 PropertyDescriptor(None, TextSet('x'))),
            ],
            failure=[LexemeDescriptor()])


if __name__ == '__main__':
    Test.main()
