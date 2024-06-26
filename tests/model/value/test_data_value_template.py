# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import DataValue, DataValueTemplate
from kif_lib.typing import assert_type

from ...tests import kif_DataValueTemplateTestCase


class Test(kif_DataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(DataValueTemplate.object_class, type[DataValue])

    def test__init__(self):
        self.assert_abstract_class(DataValueTemplate)


if __name__ == '__main__':
    Test.main()
