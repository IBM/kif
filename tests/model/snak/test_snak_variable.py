# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    KIF_Object,
    NoValueSnak,
    Property,
    Quantity,
    Snak,
    SnakVariable,
    SomeValueSnak,
    String,
    Value,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(SnakVariable.object_class, type[Snak])
        self.assertIs(SnakVariable.object_class, Snak)

    def test_check(self) -> None:
        assert_type(
            SnakVariable.check(SnakVariable('x')),
            SnakVariable)
        assert_type(
            SnakVariable.check(Variable('x', Snak)),
            SnakVariable)
        self._test_check(SnakVariable)

    def test__init__(self) -> None:
        assert_type(SnakVariable('x'), SnakVariable)
        self._test__init__(SnakVariable, self.assert_snak_variable)

    def test_instantiate(self) -> None:
        assert_type(
            SnakVariable('x').instantiate({}), Optional[KIF_Object])
        self._test_instantiate(
            SnakVariable,
            success=[
                NoValueSnak(Property('x')),
                SomeValueSnak(Variable('y')),
                ValueSnak('x', 'y'),
                ValueSnak(Variable('x'), 'y'),
            ],
            failure=[
                DataValue.variable_class('x'),
                Property('x'),
                Quantity(0),
                Quantity.template_class(Variable('x')),
                String('x'),
                String.template_class(Variable('x')),
                Value.variable_class('x'),
                Variable('x'),
            ])


if __name__ == '__main__':
    Test.main()
