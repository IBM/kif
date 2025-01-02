# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    ShallowDataValue,
    ShallowDataValueVariable,
    String,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueVariableTestCase


class Test(ShallowDataValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(
            ShallowDataValueVariable.object_class, type[ShallowDataValue])
        self.assertIs(
            ShallowDataValueVariable.object_class, ShallowDataValue)

    def test_check(self) -> None:
        assert_type(
            ShallowDataValueVariable.check(ShallowDataValueVariable('x')),
            ShallowDataValueVariable)
        assert_type(
            ShallowDataValueVariable.check(Variable('x', ShallowDataValue)),
            ShallowDataValueVariable)
        self._test_check(ShallowDataValueVariable)

    def test__init__(self) -> None:
        assert_type(
            ShallowDataValueVariable('x'), ShallowDataValueVariable)
        self._test__init__(
            ShallowDataValueVariable,
            self.assert_shallow_data_value_variable)

    def test_variables(self) -> None:
        assert_type(ShallowDataValueVariable('x').variables, Set[Variable])
        self._test_variables(ShallowDataValueVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(
            ShallowDataValueVariable('x').instantiate({}), Optional[Term])
        assert_type(
            ShallowDataValueVariable('x').match(String('x')), Optional[Theta])
        self._test_instantiate(
            ShallowDataValueVariable,
            success_auto=[
                IRI('x'),
                IRI(Variable('x')),
                Text('x'),
                Text(Variable('x')),
                Text('x', Variable('y')),
                String('x'),
                String(Variable('x')),
                ExternalId('x'),
                ExternalId(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
