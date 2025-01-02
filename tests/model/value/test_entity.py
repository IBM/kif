# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Entity,
    EntityTemplate,
    EntityVariable,
    IRI,
    Item,
    Lexeme,
    Property,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import EntityTestCase


class Test(EntityTestCase):

    def test_template_class(self) -> None:
        assert_type(Entity.template_class, type[EntityTemplate])
        self.assertIs(Entity.template_class, EntityTemplate)

    def test_variable_class(self) -> None:
        assert_type(Entity.variable_class, type[EntityVariable])
        self.assertIs(Entity.variable_class, EntityVariable)

    def test_check(self) -> None:
        assert_type(Entity.check(Item('x')), Entity)
        super()._test_check(
            Entity,
            success=[
                (Item('x'), Item('x')),
                (Property('x'), Property('x')),
                (Lexeme('x'), Lexeme('x')),
            ],
            failure=[
                'x',
                0,
                IRI('x'),
                Item(Variable('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        self.assert_abstract_class(Entity)


if __name__ == '__main__':
    Test.main()
