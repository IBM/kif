# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Value, ValueTemplate
from kif_lib.typing import assert_type

from ...tests import kif_ValueTemplateTestCase


class Test(kif_ValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(ValueTemplate.object_class, type[Value])
        self.assertIs(ValueTemplate.object_class, Value)

    def test__init__(self):
        self.assert_abstract_class(ValueTemplate)


if __name__ == '__main__':
    Test.main()
