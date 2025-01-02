# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    Property,
    QualifierRecord,
    QualifierRecordVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    ReferenceRecordVariable,
    SnakSet,
    SnakSetVariable,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(SnakSetVariable.object_class, type[SnakSet])
        self.assertIs(SnakSetVariable.object_class, SnakSet)

    def test_check(self) -> None:
        assert_type(
            SnakSetVariable.check(SnakSetVariable('x')), SnakSetVariable)
        assert_type(
            SnakSetVariable.check(Variable('x', SnakSet)), SnakSetVariable)
        self._test_check(SnakSetVariable)

    def test__init__(self) -> None:
        assert_type(SnakSetVariable('x'), SnakSetVariable)
        self._test__init__(
            SnakSetVariable, self.assert_snak_set_variable)

    def test_variables(self) -> None:
        assert_type(SnakSetVariable('x').variables, Set[Variable])
        self._test_variables(SnakSetVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(SnakSetVariable('x').instantiate({}), Optional[Term])
        assert_type(SnakSetVariable('x').match(SnakSet()), Optional[Theta])
        self._test_instantiate_and_match(
            SnakSetVariable,
            success=[
                QualifierRecord(),
                QualifierRecordVariable('x'),
                ReferenceRecord(),
                ReferenceRecordVariable('x'),
                SnakSet(),
                SnakSet(Property('x')(Item('y'))),
                SnakSet(Property('x').no_value(), Property('y')('z')),
            ],
            failure=[
                Item('x'),
                Property('x').some_value(),
                ReferenceRecordSet(),
            ])


if __name__ == '__main__':
    Test.main()
