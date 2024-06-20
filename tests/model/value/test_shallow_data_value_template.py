# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ShallowDataValue,
    ShallowDataValueTemplate,
)
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_object_class(self) -> None:
        assert_type(
            ShallowDataValueTemplate.object_class, type[ShallowDataValue])

    def test__init__(self):
        self.assert_abstract_class(ShallowDataValueTemplate)


if __name__ == '__main__':
    Test.main()
