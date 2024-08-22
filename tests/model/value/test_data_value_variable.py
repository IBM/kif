# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    DataValueVariable,
    IRI,
    Item,
    Quantity,
    String,
    Term,
    Time,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import VariableTestCase


class Test(VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(
            DataValueVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            DataValueVariable,
            success=[
                DataValue.variable_class('x'),
                IRI.template_class(Variable('x')),
                Quantity(0),
                Quantity(Variable('x')),
                String('x'),
                Time('2024-06-26'),
                Time(Variable('x')),
            ],
            failure=[
                Item('x'),
                Item.template_class(Variable('x')),
                Value.variable_class('x'),
            ])


if __name__ == '__main__':
    Test.main()
