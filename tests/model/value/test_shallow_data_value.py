# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Item,
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    String,
)
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_template_class(self) -> None:
        assert_type(
            ShallowDataValue.template_class, type[ShallowDataValueTemplate])

    def test_variable_class(self) -> None:
        assert_type(
            ShallowDataValue.variable_class, type[ShallowDataValueVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            ShallowDataValue, 0, ShallowDataValue.check)
        self.assert_raises_check_error(
            ShallowDataValue, {}, ShallowDataValue.check)
        self.assert_raises_check_error(
            ShallowDataValue, Item('x'), ShallowDataValue.check)
        # success
        assert_type(
            ShallowDataValue.check(String('x')),
            ShallowDataValue)
        self.assertEqual(ShallowDataValue.check('x'), String('x'))

    def test__init__(self):
        self.assert_abstract_class(ShallowDataValue)


if __name__ == '__main__':
    Test.main()
