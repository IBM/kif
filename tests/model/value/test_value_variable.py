# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    KIF_Object,
    Property,
    Quantity,
    Snak,
    Statement,
    String,
    Time,
    Value,
    ValueSnak,
    ValueVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(ValueVariable.object_class, type[Value])
        self.assertIs(ValueVariable.object_class, Value)

    def test_check(self) -> None:
        assert_type(ValueVariable.check(ValueVariable('x')), ValueVariable)
        assert_type(ValueVariable.check(Variable('x', Value)), ValueVariable)
        self._test_check(ValueVariable)

    def test__init__(self) -> None:
        assert_type(ValueVariable('x'), ValueVariable)
        self._test__init__(ValueVariable, self.assert_value_variable)

    def test_instantiate(self) -> None:
        assert_type(ValueVariable('x').instantiate({}), Optional[KIF_Object])
        self._test_instantiate(
            ValueVariable,
            success=[
                IRI.template_class(Variable('x')),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity(Variable('x')),
                String('x'),
                Time('2024-06-26'),
                Time(Variable('x')),
                Value.variable_class('x'),
            ],
            failure=[
                Statement(Item('x'), ValueSnak(Property('y'), Item('z'))),
                Snak.variable_class('x'),
            ])


if __name__ == '__main__':
    Test.main()
