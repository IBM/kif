# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    String,
    StringVariable,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueVariableTestCase


class Test(ShallowDataValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(StringVariable.object_class, type[String])
        self.assertIs(StringVariable.object_class, String)

    def test_check(self) -> None:
        assert_type(
            StringVariable.check(StringVariable('x')), StringVariable)
        assert_type(
            StringVariable.check(Variable('x', String)), StringVariable)
        self._test_check(StringVariable)

    def test__init__(self) -> None:
        assert_type(StringVariable('x'), StringVariable)
        self._test__init__(StringVariable, self.assert_string_variable)
        self.assert_string_variable(Variable('x', ExternalId), 'x')

    def test_variables(self) -> None:
        assert_type(StringVariable('x').variables, Set[Variable])
        self._test_variables(StringVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(StringVariable('x').instantiate({}), Optional[Term])
        assert_type(StringVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            StringVariable,
            success=[
                ExternalId('x'),
                ExternalId(Variable('x')),
                String('x'),
                String(Variable('x')),
            ],
            failure=[
                IRI('x'),
                IRI(Variable('x')),
                Text('x'),
                Text(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
