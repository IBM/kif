# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Datatype,
    ExternalId,
    ExternalIdDatatype,
    String,
    StringDatatype,
)
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_instance(self) -> None:
        assert_type(StringDatatype.instance, StringDatatype)
        self.assertIs(StringDatatype.instance, StringDatatype())

    def test_value_class(self) -> None:
        assert_type(StringDatatype.value_class, type[String])

    def test_check(self) -> None:
        assert_type(StringDatatype.check(StringDatatype()), StringDatatype)
        self._test_check(StringDatatype)
        self.assertEqual(
            StringDatatype.check(ExternalIdDatatype()),
            ExternalId.datatype)
        self.assertEqual(
            StringDatatype.check(Datatype(ExternalIdDatatype)),
            ExternalId.datatype)
        self.assertEqual(
            StringDatatype.check(Datatype(ExternalId)),
            ExternalId.datatype)

    def test__init__(self) -> None:
        assert_type(StringDatatype(), StringDatatype)
        self._test__init__(StringDatatype, self.assert_string_datatype)


if __name__ == '__main__':
    Test.main()
