# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ExternalId, ExternalIdDatatype
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_instance(self) -> None:
        assert_type(ExternalIdDatatype.instance, ExternalIdDatatype)
        self.assertIs(ExternalIdDatatype.instance, ExternalIdDatatype())

    def test_value_class(self) -> None:
        assert_type(ExternalIdDatatype.value_class, type[ExternalId])

    def test_check(self) -> None:
        assert_type(
            ExternalIdDatatype.check(ExternalIdDatatype()),
            ExternalIdDatatype)
        self._test_check(ExternalIdDatatype)

    def test__init__(self) -> None:
        assert_type(ExternalIdDatatype(), ExternalIdDatatype)
        self._test__init__(
            ExternalIdDatatype, self.assert_external_id_datatype)


if __name__ == '__main__':
    Test.main()
