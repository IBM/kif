# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DatatypeVariable,
    Entity,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemVariable,
    Property,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    QuantityVariable,
    Snak,
    SomeValueSnakTemplate,
    String,
    StringVariable,
    Term,
    Time,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueVariable,
    Variable,
)
from kif_lib.typing import assert_type, cast, Set

from ...tests import SnakTemplateTestCase


class Test(SnakTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(ValueSnakTemplate.object_class, type[ValueSnak])
        self.assertIs(ValueSnakTemplate.object_class, ValueSnak)

    def test_check(self) -> None:
        assert_type(
            ValueSnakTemplate.check(
                ValueSnakTemplate(Variable('x'), Variable('y'))),
            ValueSnakTemplate)
        self._test_check(
            ValueSnakTemplate,
            success=[
                (ValueSnakTemplate(Variable('x'), Variable('y')),
                 ValueSnakTemplate(PropertyVariable('x'), ValueVariable('y'))),
                (ValueSnakTemplate('x', Variable('y')),
                 ValueSnakTemplate(Property('x'), ValueVariable('y'))),
                (ValueSnakTemplate(PropertyVariable('x'), 'y'),
                 ValueSnakTemplate(PropertyVariable('x'), String('y'))),
            ],
            failure=[
                SomeValueSnakTemplate(Variable('x')),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(
            ValueSnakTemplate(Variable('x'), Variable('y')),
            ValueSnakTemplate)
        self._test__init__(
            ValueSnakTemplate,
            self.assert_value_snak_template,
            success=[
                ([Variable('x'), Variable('y')],
                 ValueSnak(PropertyVariable('x'), ValueVariable('y'))),
                ([Property(IRI(Variable('x'))), Variable('y')],
                 ValueSnak(
                     Property(IRI(Variable('x', String))),
                     ValueVariable('y'))),
                ([Property('x', Quantity), Quantity(Variable('y'))],
                 ValueSnak(
                     Property('x', Quantity),
                     Quantity(QuantityVariable('y')))),
                ([Property('x', Variable('y')), Item('z')],
                 ValueSnak(Property('x', DatatypeVariable('y')), Item('z'))),
                ([Property(Variable('x')), ItemVariable('y')],
                 ValueSnak(Property(Variable('x'), Item), ItemVariable('y'))),
                ([Property(Variable('x')), Item('y')],
                 ValueSnak(Property(Variable('x'), Item), Item('y'))),
                ([Property(Variable('x')), Item(Variable('y'))],
                 ValueSnak(
                     Property(Variable('x'), Item),
                     Item(Variable('y')))),
                ([Property(Variable('x'), Item), Variable('y', Entity)],
                 ValueSnak(
                     Property(Variable('x'), Item),
                     ItemVariable('y'))),
            ],
            failure=[
                [Property(Variable('x'), Item), Variable('y', IRI)],
            ],
            failure_value_error=[
                [Property(Variable('x'), Item), Property('y')],
            ],
            normalize=[
                ['x', 'y'],
                [IRI('x'), 'y'],
                [Property('x'), Item('y')],
            ])

        # extra
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            (ValueSnakTemplate, 'ValueSnak'), 0, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (ValueSnakTemplate, 'ValueSnak'), Property('x'), {})
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into PropertyVariable",
            ValueSnakTemplate, IRI_Variable('x'), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce SnakVariable into ValueVariable",
            ValueSnakTemplate, Property('p'), Variable('x', Snak))
        self.assert_value_snak_template(
            ValueSnakTemplate(x, Quantity(0)),
            Variable('x', Property), Quantity(0))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property(x), Quantity(0)),
            Property(Variable('x', IRI), Quantity), Quantity(0))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property('p'), x),
            Property('p'), ValueVariable('x'))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property('p'), IRI_Template(x)),
            Property('p', IRI), IRI(StringVariable('x')))
        self.assert_value_snak_template(
            ValueSnak(x, Quantity(0)),
            Variable('x', Property), Quantity(0))
        self.assert_value_snak_template(
            ValueSnak(Property(x), Quantity(0)),
            Property(Variable('x', IRI), Quantity), Quantity(0))
        self.assert_value_snak_template(
            ValueSnak(Property('p'), x),
            Property('p'), Variable('x', Value))
        self.assert_value_snak_template(
            cast(ValueSnakTemplate, ValueSnak(Property('p'), Time(x))),
            Property('p', Time), Time(Variable('x', Time)))
        self.assert_value_snak_template(
            PropertyTemplate(x)(String('s')),
            Property(x, String), String('s'))
        self.assert_value_snak(
            cast(ValueSnak, ValueSnakTemplate(Property('p'), Item('x'))),
            Property('p', Item), Item('x'))
        self.assertEqual(
            ValueSnak(x, x),
            ValueSnak(PropertyVariable('x'), PropertyVariable('x')))

    def test_variables(self) -> None:
        assert_type(
            ValueSnakTemplate(Variable('x'), 'y').variables, Set[Variable])
        self._test_variables(
            ValueSnakTemplate,
            (ValueSnak(Variable('x'), Variable('y')),
             {PropertyVariable('x'), ValueVariable('y')}),
            (ValueSnak(Property('x'), Variable('y')),
             {ValueVariable('y')}),
            (ValueSnak(Variable('x'), String('y')),
             {PropertyVariable('x')}),
            (ValueSnak(Property('x', Variable('x')), Variable('y')),
             {DatatypeVariable('x'), ValueVariable('y')}))

    def test_instantiate(self) -> None:
        assert_type(ValueSnakTemplate(
            Variable('x'), Variable('y')).instantiate({}), Term)
        self._test_instantiate(
            ValueSnakTemplate,
            success=[
                (ValueSnak(Variable('x'), Variable('y')),
                 ValueSnak('x', Variable('y')),
                 {PropertyVariable('x'): Property('x')}),
                (ValueSnak(Variable('x'), Variable('y')),
                 ValueSnak(Property('x', Item), Variable('y')),
                 {PropertyVariable('x'): Property('x', ItemDatatype())}),
                (ValueSnak(Property('x', Variable('y')), Item('z')),
                 ValueSnak(Property('x', ItemDatatype()), Item('z')),
                 {DatatypeVariable('y'): Item.datatype}),
                (ValueSnak(Variable('x'), Property('x')),
                 ValueSnak(Property('x'), Property('x')),
                 {PropertyVariable('x'): Property('x')}),
                (ValueSnak(Property(Variable('x')), IRI('x')),
                 ValueSnak(Property('z'), IRI('x')),
                 {IRI_Variable('x'): IRI('z')}),
            ],
            failure=[
                (ValueSnakTemplate(Variable('x'), Variable('y')),
                 {PropertyVariable('x'): Item('y')}),
                (ValueSnakTemplate(Variable('x'), Variable('y')),
                 {ValueVariable('y'): ValueSnakVariable('y')}),
            ])


if __name__ == '__main__':
    Test.main()
