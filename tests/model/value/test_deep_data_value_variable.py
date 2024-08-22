# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    DeepDataValue,
    DeepDataValueVariable,
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

    def test_instantiate(self) -> None:
        assert_type(
            DeepDataValueVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            DeepDataValueVariable,
            success=[
                DeepDataValue.variable_class('x'),
                Quantity(0),
                Quantity(Variable('x')),
                Time('2024-06-26'),
                Time(Variable('x')),
            ],
            failure=[
                DataValue.variable_class('x'),
                IRI.template_class(Variable('x')),
                Item('x'),
                Item.template_class(Variable('x')),
                String('x'),
                Value.variable_class('x'),
            ])


if __name__ == '__main__':
    Test.main()
