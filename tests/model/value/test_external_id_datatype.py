# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import ExternalId, ExternalIdDatatype, StringDatatype
from kif_lib.typing import assert_type

from ...tests import kif_DatatypeTestCase


class Test(kif_DatatypeTestCase):

    def test_value_class(self) -> None:
        assert_type(ExternalIdDatatype.value_class, type[ExternalId])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            ExternalIdDatatype, StringDatatype, ExternalIdDatatype.check)
        # success
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
