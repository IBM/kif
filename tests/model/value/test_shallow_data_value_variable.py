# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DataValue,
    ExternalId,
    Item,
    Quantity,
    ShallowDataValue,
    ShallowDataValueVariable,
    String,
    Term,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import VariableTestCase


class Test(VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(
            ShallowDataValueVariable('x').instantiate({}),
            Optional[Term])
        self._test_instantiate(
            ShallowDataValueVariable,
            success=[
                ExternalId('x'),
                ExternalId.template_class(Variable('y')),
                String('x'),
                String.template_class(Variable('y')),
            ],
            failure=[
                DataValue.variable_class('x'),
                Item('x'),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
                Value.variable_class('x'),
            ])


if __name__ == '__main__':
    Test.main()
