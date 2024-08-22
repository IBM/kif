# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import ShallowDataValue, ShallowDataValueTemplate
from kif_lib.typing import assert_type

from ...tests import ShallowDataValueTemplateTestCase


class Test(ShallowDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(
            ShallowDataValueTemplate.object_class, type[ShallowDataValue])
        self.assertIs(
            ShallowDataValueTemplate.object_class, ShallowDataValue)

    def test__init__(self) -> None:
        self.assert_abstract_class(ShallowDataValueTemplate)


if __name__ == '__main__':
    Test.main()
