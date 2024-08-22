# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import DeepDataValue, DeepDataValueTemplate
from kif_lib.typing import assert_type

from ...tests import DeepDataValueTemplateTestCase


class Test(DeepDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(DeepDataValueTemplate.object_class, type[DeepDataValue])
        self.assertIs(DeepDataValueTemplate.object_class, DeepDataValue)

    def test__init__(self) -> None:
        self.assert_abstract_class(DeepDataValueTemplate)


if __name__ == '__main__':
    Test.main()
