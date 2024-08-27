# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Lexeme, LexemeDatatype
from kif_lib.typing import assert_type

from ...tests import DatatypeTestCase


class Test(DatatypeTestCase):

    def test_value_class(self) -> None:
        assert_type(LexemeDatatype.value_class, type[Lexeme])

    def test_check(self) -> None:
        assert_type(LexemeDatatype.check(LexemeDatatype()), LexemeDatatype)
        self._test_check(LexemeDatatype)

    def test__init__(self) -> None:
        assert_type(LexemeDatatype(), LexemeDatatype)
        self._test__init__(LexemeDatatype, self.assert_lexeme_datatype)


if __name__ == '__main__':
    Test.main()
