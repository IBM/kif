# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    TextTemplate,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTestCase


class Test(kif_ShallowDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(String.datatype_class, type[StringDatatype])

    def test_datatype(self) -> None:
        assert_type(String.datatype, StringDatatype)
        self.assertIsInstance(String.datatype, StringDatatype)

    def test_template_class(self) -> None:
        assert_type(String.template_class, type[StringTemplate])

    def test_variable_class(self) -> None:
        assert_type(String.variable_class, type[StringVariable])

    def test_check(self) -> None:
        assert_type(String.check(String('x')), String)
        self._test_check(
            String,
            failure=[
                IRI('x'),
                Item('x'),
                TextTemplate(Variable('x')),
                Variable('x', Item),
            ])

    def test__init__(self) -> None:
        assert_type(String('x'), String)
        self._test__init__(
            String,
            self.assert_string,
            failure=[
                IRI('x'),
                Item('x'),
                TextTemplate(Variable('x')),
                Variable('x', Item),
            ])


if __name__ == '__main__':
    Test.main()
