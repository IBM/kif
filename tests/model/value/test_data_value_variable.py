# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DataValue,
    DataValueVariable,
    IRI,
    Quantity,
    String,
    Term,
    Theta,
    Time,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import DataValueVariableTestCase


class Test(DataValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(DataValueVariable.object_class, type[DataValue])
        self.assertIs(DataValueVariable.object_class, DataValue)

    def test_check(self) -> None:
        assert_type(
            DataValueVariable.check(DataValueVariable('x')),
            DataValueVariable)
        assert_type(
            DataValueVariable.check(Variable('x', DataValue)),
            DataValueVariable)
        self._test_check(DataValueVariable)

    def test__init__(self) -> None:
        assert_type(DataValueVariable('x'), DataValueVariable)
        self._test__init__(DataValueVariable, self.assert_data_value_variable)

    def test_variables(self) -> None:
        assert_type(DataValueVariable('x').variables, Set[Variable])
        self._test_variables(DataValueVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(
            DataValueVariable('x').instantiate({}), Optional[Term])
        assert_type(
            DataValueVariable('x').match(IRI('x')), Optional[Theta])
        self._test_instantiate_and_match(
            DataValueVariable,
            success=[
                DataValueVariable('x'),
                IRI.template_class(Variable('x')),
                Quantity(0),
                Quantity(Variable('x')),
                String('x'),
                Time('2024-06-26'),
                Time(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
