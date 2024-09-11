# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DatatypeVariable,
    Entity,
    EntityVariable,
    IRI,
    IRI_Variable,
    Item,
    ItemVariable,
    Lexeme,
    LexemeTemplate,
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    Property,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    Snak,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    Statement,
    StatementTemplate,
    String,
    Term,
    Theta,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueVariable,
    Variable,
)
from kif_lib.typing import assert_type, cast, Optional, Set

from ...tests import StatementTemplateTestCase


class Test(StatementTemplateTestCase):

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

        # extra
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce int into Entity',
            (StatementTemplate, 'Statement'), 0, Property('p')(0))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce int into Snak',
            (StatementTemplate, 'Statement'), Item('x'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into EntityVariable",
            StatementTemplate, IRI_Variable('x'), x)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce IRI_Variable into SnakVariable",
            StatementTemplate, x, IRI_Variable('x'))
        self.assert_statement_template(
            StatementTemplate(x, Property('p')(0)),
            Variable('x', Entity), Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Lexeme(x), Property('p')(0)),
            LexemeTemplate(IRI_Variable('x')),
            Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Item('x'), x), Item('x'), Variable('x', Snak))
        self.assert_statement_template(
            StatementTemplate(Item('x'), NoValueSnakTemplate(x)),
            Item('x'), NoValueSnakTemplate(PropertyVariable('x')))
        self.assert_statement_template(
            Statement(Lexeme(x), Property('p')(0)),
            Lexeme(IRI_Variable('x')), Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Item('x'), x), Item('x'), Variable('x', Snak))
        self.assert_statement_template(
            StatementTemplate(Item('x'), NoValueSnak(x)),
            Item('x'), NoValueSnak(PropertyVariable('x')))
        self.assert_statement_template(
            PropertyTemplate(x)(Item('i'), String('s')),
            Item('i'), PropertyTemplate(x)(String('s')))
        self.assert_statement(
            cast(Statement, PropertyTemplate('x')(Item('i'), String('s'))),
            Item('i'), Property('x')(String('s')))
        self.assertRaises(TypeError, Statement, x, x)
        self.assertEqual(
            StatementTemplate(x, x(x)),
            StatementTemplate(PropertyVariable('x'), ValueSnak(
                PropertyVariable('x'), PropertyVariable('x'))))
        self.assertEqual(
            StatementTemplate(x, SomeValueSnak(x)),
            StatementTemplate(
                PropertyVariable('x'),
                SomeValueSnak(PropertyVariable('x'))))
        self.assertEqual(
            StatementTemplate(x, NoValueSnak(x)),
            StatementTemplate(
                PropertyVariable('x'),
                NoValueSnak(PropertyVariable('x'))))

    def test_variables(self) -> None:
        assert_type(
            StatementTemplate(Variable('x'), Variable('y')).variables,
            Set[Variable])
        self._test_variables(
            StatementTemplate,
            (StatementTemplate(Variable('x'), Variable('y')),
             {EntityVariable('x'), SnakVariable('y')}),
            (StatementTemplate(Property('x'), Variable('y')),
             {SnakVariable('y')}),
            (StatementTemplate(Property('x', Variable('y')), Variable('z')),
             {DatatypeVariable('y'), SnakVariable('z')}),
            (StatementTemplate(
                Property('x', Variable('y')),
                ValueSnakVariable('z')),
             {DatatypeVariable('y'), ValueSnakVariable('z')}),
            (StatementTemplate(
                Property('x', Variable('y')),
                NoValueSnak(Variable('z'))),
             {DatatypeVariable('y'), PropertyVariable('z')}))

    def test_instantiate(self) -> None:
        assert_type(StatementTemplate(
            Variable('x'), Variable('y')).instantiate({}), Term)
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

    def test_match(self) -> None:
        assert_type(
            StatementTemplate(Variable('x'), Variable('y')).match(
                Statement(Item('x'), ValueSnak('x', 'y'))), Optional[Theta])
        self._test_match(
            StatementTemplate,
            success=[
                (Statement(Variable('x'), Variable('y')),
                 Statement(Item('x'), ValueSnak('y', 'z')),
                 {EntityVariable('x'): Item('x'),
                  SnakVariable('y'): ValueSnak('y', 'z')}),
                (Statement(ItemVariable('x'), NoValueSnakVariable('y')),
                 Statement(Item('x'), SnakVariable('y')),
                 {ItemVariable('x'): Item('x'),
                  SnakVariable('y'): NoValueSnakVariable('y')}),
                ###
                # TODO: Should we infer that the datatype of property 'y' is
                # String here? If so, how can we do that?
                ###
                (Statement(Item('x'), ValueSnak(Variable('y'), 'z')),
                 Statement(Item('x'), ValueSnak('y', ValueVariable('z'))),
                 {PropertyVariable('y'): Property('y'),
                  ValueVariable('z'): String('z')}),
                (Statement(Variable('x'),
                           ValueSnak('y', Quantity(Variable('w')))),
                 Statement(Item('x'), ValueSnak(Variable('y'), Variable('z'))),
                 {EntityVariable('x'): Item('x'),
                  PropertyVariable('y'): Property('y', Quantity),
                  ValueVariable('z'): Quantity(Variable('w'))}),
            ], failure=[
                (Statement(ItemVariable('x'), ValueSnak('y', 'z')),
                 Statement(Property('x'), ValueSnak('y', 'z'))),
                (Statement(Variable('x'), ValueSnak('y', 'z')),
                 Statement(Item('x'), ValueSnak('y', ValueVariable('z')))),
            ])


if __name__ == '__main__':
    Test.main()
