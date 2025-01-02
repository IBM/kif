# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Time, TimeDatatype
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_instance(self) -> None:
        assert_type(TimeDatatype.instance, TimeDatatype)
        self.assertIs(TimeDatatype.instance, TimeDatatype())

    def test_value_class(self) -> None:
        assert_type(TimeDatatype.value_class, type[Time])

    def test_check(self) -> None:
        assert_type(TimeDatatype.check(TimeDatatype()), TimeDatatype)
        self._test_check(TimeDatatype)

    def test__init__(self) -> None:
        assert_type(TimeDatatype(), TimeDatatype)
        self._test__init__(TimeDatatype, self.assert_time_datatype)


if __name__ == '__main__':
    Test.main()
