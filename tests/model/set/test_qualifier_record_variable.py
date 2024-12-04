# Copyright (C) 2024 IBM Corp.
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
            QualifierRecordVariable.object_class, type[QualifierRecord])
        self.assertIs(QualifierRecordVariable.object_class, QualifierRecord)

    def test_check(self) -> None:
        assert_type(
            QualifierRecordVariable.check(QualifierRecordVariable('x')),
            QualifierRecordVariable)
        assert_type(
            QualifierRecordVariable.check(Variable('x', QualifierRecord)),
            QualifierRecordVariable)
        self._test_check(QualifierRecordVariable)

    def test__init__(self) -> None:
        assert_type(QualifierRecordVariable('x'), QualifierRecordVariable)
        self._test__init__(
            QualifierRecordVariable, self.assert_qualifier_record_variable)

    def test_variables(self) -> None:
        assert_type(QualifierRecordVariable('x').variables, Set[Variable])
        self._test_variables(QualifierRecordVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(
            QualifierRecordVariable('x').instantiate({}), Optional[Term])
        assert_type(
            QualifierRecordVariable('x').match(QualifierRecord()),
            Optional[Theta])
        self._test_instantiate_and_match(
            QualifierRecordVariable,
            success=[
                QualifierRecord(),
                QualifierRecord(Property('x')(Item('y'))),
                QualifierRecord(Property('x').no_value(), Property('y')('z')),
            ],
            failure=[
                Item('x'),
                Property('x').some_value(),
                ReferenceRecord(),
                ReferenceRecordSet(),
                ReferenceRecordVariable('x'),
                SnakSet(),
                SnakSet(Property('x').some_value()),
            ])


if __name__ == '__main__':
    Test.main()
