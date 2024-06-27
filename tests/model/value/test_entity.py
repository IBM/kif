# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

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

from ...tests import kif_EntityTestCase


class Test(kif_EntityTestCase):

    def test_template_class(self) -> None:
        assert_type(Entity.template_class, type[EntityTemplate])

    def test_variable_class(self) -> None:
        assert_type(Entity.variable_class, type[EntityVariable])

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

    def test__init__(self):
        self.assert_abstract_class(Entity)


if __name__ == '__main__':
    Test.main()
