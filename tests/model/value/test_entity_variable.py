# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    Entity,
    EntityVariable,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    Quantity,
    String,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(EntityVariable.object_class, type[Entity])
        self.assertIs(EntityVariable.object_class, Entity)

    def test_check(self) -> None:
        assert_type(
            EntityVariable.check(EntityVariable('x')),
            EntityVariable)
        assert_type(
            EntityVariable.check(Variable('x', Entity)),
            EntityVariable)
        self._test_check(EntityVariable)

    def test__init__(self) -> None:
        assert_type(EntityVariable('x'), EntityVariable)
        self._test__init__(EntityVariable, self.assert_entity_variable)

    def test_instantiate(self) -> None:
        assert_type(
            EntityVariable('x').instantiate({}), Optional[KIF_Object])
        self._test_instantiate(
            EntityVariable,
            success=[
                Item('x'),
                Item.template_class(Variable('y')),
                Lexeme('x'),
                Property.template_class(Variable('y'))
            ],
            failure=[
                DataValue.variable_class('x'),
                Quantity(0),
                Quantity.template_class(Variable('x')),
                String('x'),
                String.template_class(Variable('x')),
                Value.variable_class('x'),
            ])


if __name__ == '__main__':
    Test.main()
