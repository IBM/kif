# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    KIF_Object,
    Quantity,
    Statement,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    Variable,
    Variables,
)
from kif_lib.model import (
    IRI_Variable,
    ItemTemplate,
    ItemVariable,
    PropertyVariable,
    QuantityVariable,
    StatementTemplate,
    Template,
)
from kif_lib.typing import assert_type, cast, Set

from ..tests import kif_TemplateTestCase


class Test(kif_TemplateTestCase):

    def test_check(self) -> None:
        assert_type(Template.check(ItemTemplate(Variable('x'))), Template)
        super()._test_check(
            Template,
            success=[
                (Item(Variable('x')), ItemTemplate(Variable('x', IRI))),
                (ValueSnak('x', Variable('y')),
                 ValueSnakTemplate('x', Variable('y', Value))),
            ],
            failure=[
                Item('x'),
                ItemTemplate('x'),
                ValueSnakTemplate('x', 'y'),
            ])

    def test__init__(self) -> None:
        self.assert_abstract_class(Template)

    def test_get_variables(self) -> None:
        assert_type(ItemTemplate(Variable('x')).variables, Set[Variable])
        self.assertEqual(
            ItemTemplate(Variable('x')).get_variables(),
            {IRI_Variable('x')})
        x, y, z = Variables('x', 'y', 'z')
        self.assertEqual(
            cast(StatementTemplate, Statement(
                x, ValueSnak(y, Quantity(123, x, z)))).variables, {
                ItemVariable('x'),
                PropertyVariable('y'),
                QuantityVariable('z')})

    def test_instantiate(self) -> None:
        assert_type(ItemTemplate(Variable('x')).instantiate({}), KIF_Object)
        x = Variable('x')
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate IRI_Variable 'x' with Item",
            ItemTemplate(x).instantiate, {IRI_Variable('x'): Item('x')})
        self.assertEqual(
            ItemTemplate(x).instantiate({IRI_Variable('x'): IRI('x')}),
            Item(IRI('x')))


if __name__ == '__main__':
    Test.main()
