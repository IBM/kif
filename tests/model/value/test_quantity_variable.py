# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Item,
    Quantity,
    QuantityTemplate,
    QuantityVariable,
    String,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(QuantityVariable.object_class, type[Quantity])
        self.assertIs(QuantityVariable.object_class, Quantity)

    def test_check(self) -> None:
        assert_type(
            QuantityVariable.check(QuantityVariable('x')), QuantityVariable)
        assert_type(
            QuantityVariable.check(Variable('x', Quantity)), QuantityVariable)
        self._test_check(QuantityVariable)

    def test__init__(self) -> None:
        assert_type(QuantityVariable('x'), QuantityVariable)
        self._test__init__(QuantityVariable, self.assert_quantity_variable)

    def test_instantiate(self) -> None:
        assert_type(
            QuantityVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            QuantityVariable,
            success=[
                Quantity(0),
                Quantity(0, None, None, Variable('x')),
                Quantity(0, None, Variable('x')),
                Quantity(0, Variable('x')),
                QuantityTemplate(Variable('y')),
            ],
            failure=[
                Item('x'),
                Item.template_class(Variable('x')),
                String('x'),
                String.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()
