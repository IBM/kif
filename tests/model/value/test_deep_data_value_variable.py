# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DeepDataValue,
    DeepDataValueVariable,
    Quantity,
    Term,
    Theta,
    Time,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(DeepDataValueVariable.object_class, type[DeepDataValue])
        self.assertIs(DeepDataValueVariable.object_class, DeepDataValue)

    def test_check(self) -> None:
        assert_type(
            DeepDataValueVariable.check(DeepDataValueVariable('x')),
            DeepDataValueVariable)
        assert_type(
            DeepDataValueVariable.check(Variable('x', DeepDataValue)),
            DeepDataValueVariable)
        self._test_check(DeepDataValueVariable)

    def test__init__(self) -> None:
        assert_type(
            DeepDataValueVariable('x'), DeepDataValueVariable)
        self._test__init__(
            DeepDataValueVariable,
            self.assert_deep_data_value_variable)

    def test_variables(self) -> None:
        assert_type(DeepDataValueVariable('x').variables, Set[Variable])
        self._test_variables(DeepDataValueVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(
            DeepDataValueVariable('x').instantiate({}), Optional[Term])
        assert_type(
            DeepDataValueVariable('x').match(Quantity(0)), Optional[Theta])
        self._test_instantiate(
            DeepDataValueVariable,
            success_auto=[
                Quantity(0),
                Quantity(Variable('x')),
                Time('2024-09-09'),
                Time(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
