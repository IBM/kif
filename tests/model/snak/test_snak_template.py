# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Snak, SnakTemplate
from kif_lib.typing import assert_type

from ...tests import kif_SnakTemplateTestCase


class Test(kif_SnakTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(SnakTemplate.object_class, type[Snak])
        self.assertIs(SnakTemplate.object_class, Snak)

    def test__init__(self):
        self.assert_abstract_class(SnakTemplate)


if __name__ == '__main__':
    Test.main()
