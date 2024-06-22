# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    ExternalId,
    Item,
    KIF_Object,
    Quantity,
    ShallowDataValue,
    ShallowDataValueVariable,
    String,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(
            ShallowDataValueVariable.object_class, type[ShallowDataValue])

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
            Optional[KIF_Object])
        self._test_instantiate(
            ShallowDataValueVariable,
            success=[
                String('x'),
                String.template_class(Variable('y')),
                ExternalId('x'),
                ExternalId.template_class(Variable('y'))],
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
