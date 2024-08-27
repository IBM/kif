# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import DataValue, DataValueTemplate
from kif_lib.typing import assert_type

from ...tests import DataValueTemplateTestCase


class Test(DataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(DataValueTemplate.object_class, type[DataValue])
        self.assertIs(DataValueTemplate.object_class, DataValue)

    def test__init__(self) -> None:
        self.assert_abstract_class(DataValueTemplate)


if __name__ == '__main__':
    Test.main()
