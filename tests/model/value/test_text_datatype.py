# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Text, TextDatatype
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_value_class(self) -> None:
        assert_type(TextDatatype.value_class, type[Text])

    def test_check(self) -> None:
        assert_type(TextDatatype.check(TextDatatype()), TextDatatype)
        self._test_check(TextDatatype)

    def test__init__(self) -> None:
        assert_type(TextDatatype(), TextDatatype)
        self._test__init__(TextDatatype, self.assert_text_datatype)


if __name__ == '__main__':
    Test.main()
