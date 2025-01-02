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
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(
            ReferenceRecordVariable.object_class, type[ReferenceRecord])
        self.assertIs(ReferenceRecordVariable.object_class, ReferenceRecord)

    def test_check(self) -> None:
        assert_type(
            ReferenceRecordVariable.check(ReferenceRecordVariable('x')),
            ReferenceRecordVariable)
        assert_type(
            ReferenceRecordVariable.check(Variable('x', ReferenceRecord)),
            ReferenceRecordVariable)
        self._test_check(ReferenceRecordVariable)

    def test__init__(self) -> None:
        assert_type(ReferenceRecordVariable('x'), ReferenceRecordVariable)
        self._test__init__(
            ReferenceRecordVariable, self.assert_reference_record_variable)

    def test_variables(self) -> None:
        assert_type(ReferenceRecordVariable('x').variables, Set[Variable])
        self._test_variables(ReferenceRecordVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(
            ReferenceRecordVariable('x').instantiate({}), Optional[Term])
        assert_type(
            ReferenceRecordVariable('x').match(ReferenceRecord()),
            Optional[Theta])
        self._test_instantiate_and_match(
            ReferenceRecordVariable,
            success=[
                ReferenceRecord(),
                ReferenceRecord(Property('x')(Item('y'))),
                ReferenceRecord(Property('x').no_value(), Property('y')('z')),
            ],
            failure=[
                Item('x'),
                Property('x').some_value(),
                QualifierRecord(),
                QualifierRecordVariable('x'),
                ReferenceRecordSet(),
                SnakSet(),
                SnakSet(Property('x').some_value()),
            ])


if __name__ == '__main__':
    Test.main()
