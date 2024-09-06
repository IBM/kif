# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Entity,
    EntityVariable,
    Item,
    ItemVariable,
    Lexeme,
    LexemeVariable,
    Property,
    PropertyVariable,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import EntityVariableTestCase


class Test(EntityVariableTestCase):

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

    def test_variables(self) -> None:
        assert_type(EntityVariable('x').variables, Set[Variable])
        self._test_variables(EntityVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(EntityVariable('x').instantiate({}), Optional[Term])
        assert_type(EntityVariable('x').match(Item('x')), Optional[Theta])
        self._test_instantiate_and_match(
            EntityVariable,
            success=[
                Item('x'),
                Item(Variable('x')),
                ItemVariable('x'),
                Lexeme('x'),
                Lexeme(Variable('x')),
                LexemeVariable('x'),
                Property(Variable('x')),
                PropertyVariable('x'),
            ])


if __name__ == '__main__':
    Test.main()
