# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    ExternalIdVariable,
    IRI,
    Item,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    Term,
    TextTemplate,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueTestCase


class Test(ShallowDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(String.datatype_class, type[StringDatatype])
        self.assertIs(String.datatype_class, StringDatatype)

    def test_datatype(self) -> None:
        assert_type(String.datatype, StringDatatype)
        self.assert_string_datatype(String.datatype)

    def test_template_class(self) -> None:
        assert_type(String.template_class, type[StringTemplate])
        self.assertIs(String.template_class, StringTemplate)

    def test_variable_class(self) -> None:
        assert_type(String.variable_class, type[StringVariable])
        self.assertIs(String.variable_class, StringVariable)

    def test_check(self) -> None:
        assert_type(String.check(String('x')), String)
        self._test_check(
            String,
            success=[
                (ExternalId('x'), ExternalId('x')),
            ],
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
            success=[
                (['x'], String('x')),
                ([ExternalId('x')], ExternalId('x')),
            ],
            failure=[
                [IRI('x')],
                [Item('x')],
                [TextTemplate(Variable('x'))],
                [Variable('x', Item)],
            ])

    def test_variables(self) -> None:
        assert_type(String('x').variables, Set[Variable])
        self._test_variables(String)

    def test_instantiate(self) -> None:
        assert_type(String('x').instantiate({}), Term)
        self._test_instantiate(String)

    def test_match(self) -> None:
        assert_type(String('x').match(Variable('x')), Optional[Theta])
        self._test_match(
            String,
            failure=[(String('x'), ExternalIdVariable('x'))])


if __name__ == '__main__':
    Test.main()
