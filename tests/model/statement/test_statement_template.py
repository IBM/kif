# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    EntityVariable,
    IRI,
    IRI_Variable,
    Item,
    ItemVariable,
    KIF_Object,
    NoValueSnak,
    Property,
    PropertyVariable,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    Statement,
    StatementTemplate,
    String,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueVariable,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_StatementTemplateTestCase


class Test(kif_StatementTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(StatementTemplate.object_class, type[Statement])
        self.assertIs(StatementTemplate.object_class, Statement)

    def test_check(self) -> None:
        assert_type(
            StatementTemplate.check(
                StatementTemplate(Variable('x'), Variable('y'))),
            StatementTemplate)
        self._test_check(
            StatementTemplate,
            success=[
                (StatementTemplate(Variable('x'), Variable('y')),
                 Statement(EntityVariable('x'), SnakVariable('y'))),
                (Statement(Item('x'), Variable('y')),
                 StatementTemplate(Item('x'), SnakVariable('y'))),
                (Statement(Item('x'), ValueSnak('y', Variable('z'))),
                 StatementTemplate(
                     Item('x'),
                     ValueSnakTemplate(Property('y'), ValueVariable('z')))),
            ],
            failure=[
                SomeValueSnakTemplate(Variable('x')),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(
            StatementTemplate(Variable('x'), Variable('y')),
            StatementTemplate)
        self._test__init__(
            StatementTemplate,
            self.assert_statement_template,
            success=[
                ([Variable('x'), Variable('y')],
                 Statement(EntityVariable('x'), SnakVariable('y'))),
                ([Variable('x'), NoValueSnak('y')],
                 StatementTemplate(EntityVariable('x'), NoValueSnak('y'))),
                ([Property('x'), Property(IRI(Variable('x')))(Variable('y'))],
                 StatementTemplate(
                     Property('x'),
                     ValueSnak(
                         Property(IRI(Variable('x', String))),
                         ValueVariable('y')))),
                ([Item(Variable('x')), NoValueSnak(Property(Variable('x')))],
                 StatementTemplate(
                     Item(Variable('x', IRI)),
                     NoValueSnak(Property(Variable('x', IRI))))),
                ([PropertyVariable('x'), ValueSnakVariable('y')],
                 StatementTemplate(
                     PropertyVariable('x'),
                     Variable('y', ValueSnak))),
            ],
            failure=[
                [IRI_Variable('x'), Variable('y')],
            ],
            normalize=[
                [Item('x'), NoValueSnak('y')],
                [Item('x'), Property('y')(Item('x'))],
            ])

    def test_instantiate(self) -> None:
        assert_type(StatementTemplate(
            Variable('x'), Variable('y')).instantiate({}), KIF_Object)
        self._test_instantiate(
            StatementTemplate,
            success=[
                (Statement(Variable('x'), Variable('y')),
                 Statement(Item('x'), NoValueSnak(Variable('y'))),
                 {EntityVariable('x'): Item('x'),
                  SnakVariable('y'): NoValueSnak(PropertyVariable('y'))}),
                (Statement(
                    PropertyVariable('x'),
                    SomeValueSnak(PropertyVariable('x'))),
                 Statement(
                     Property('y', IRI),
                     SomeValueSnak(Property('y', IRI))),
                 {PropertyVariable('x'): Property('y', IRI)}),
            ],
            failure=[
                (Statement(Variable('x'), Variable('y')),
                 {EntityVariable('x'): IRI('y')}),
                (Statement(Variable('x'), Variable('y')),
                 {SnakVariable('y'): Property('p')(Item('x'), 'y')}),
                (Statement(
                    ItemVariable('x'),
                    ValueSnak(Property(Variable('y'), IRI), Variable('z'))),
                 {IRI_Variable('z'): ItemVariable('z')}),
            ])


if __name__ == '__main__':
    Test.main()
