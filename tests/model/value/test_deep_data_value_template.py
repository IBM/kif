# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import DeepDataValue, DeepDataValueTemplate
from kif_lib.typing import assert_type

from ...tests import kif_DeepDataValueTemplateTestCase


class Test(kif_DeepDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(DeepDataValueTemplate.object_class, type[DeepDataValue])

    def test__init__(self):
        self.assert_abstract_class(DeepDataValueTemplate)


if __name__ == '__main__':
    Test.main()
