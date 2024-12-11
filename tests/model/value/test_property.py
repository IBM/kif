# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    DatatypeVariable,
    Entity,
    ExternalId,
    IRI,
    IRI_Variable,
    Item,
    itertools,
    Lexeme,
    NoValueSnak,
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    QuantityDatatype,
    SomeValueSnak,
    Statement,
    String,
    Term,
    Text,
    Theta,
    Time,
    Value,
    ValueSnak,
    Variable,
)
from kif_lib.model import TDatatype, TValue
from kif_lib.typing import assert_type, cast, ClassVar, Iterable, Optional, Set

from ...tests import EntityTestCase


class Test(EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Property.datatype_class, type[PropertyDatatype])
        self.assertIs(Property.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(Property.datatype, PropertyDatatype)
        self.assert_property_datatype(Property.datatype)

    def test_template_class(self) -> None:
        assert_type(Property.template_class, type[PropertyTemplate])
        self.assertIs(Property.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(Property.variable_class, type[PropertyVariable])
        self.assertIs(Property.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(Property.check(Property('x')), Property)
        self._test_check(
            Property,
            success=[
                ('x', Property('x')),
                (ExternalId('x'), Property('x')),
            ],
            failure=[
                Item('x'),
                Lexeme('x'),
                PropertyTemplate(Variable('x')),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce Item into Datatype',
            Property, 'x', Item('y'))
        # success
        assert_type(Property('x'), Property)
        self._test__init__(
            Property,
            self.assert_property,
            success=[
                (['x', String('y')], Property('x', 'y')),  # type: ignore
            ],
            failure=[
                ['x', Item('y')],
                ['x', Text('y')],
                [Item('x')],
                [Lexeme('x')],
                [PropertyTemplate(Variable('x'))],
                [Text('x')],
                [Variable('x', Text)],
            ])
        self.assert_property(Property('x'), IRI('x'), None)
        self.assert_property(
            Property('x', Item), IRI('x'), Item.datatype)
        self.assert_property(
            Property('x', Item.datatype_class), IRI('x'), Item.datatype)
        self.assert_property(
            Property('x', Item.datatype), IRI('x'), Item.datatype)

    _test__call__entities: ClassVar[list[Entity]] = [
        Item('x'),
        Lexeme('z'),
        Property('y', Item.datatype)
    ]

    _test__call__values: ClassVar[list[tuple[TValue, TDatatype]]] = [
        ('x', String),
        (0, Quantity),
        (datetime.datetime(2024, 6, 24, tzinfo=datetime.timezone.utc), Time),
        (ExternalId('x'), ExternalId),
        (IRI('x'), IRI),
        (Item('x'), Item),
        (Property('x'), Property),
        (Quantity(0), Quantity),
        (String('x'), String),
        (Text('x', 'y'), Text),
        (Time('2024-06-24'), Time),
    ]

    def test__call__(self) -> None:
        # variant 1
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (Property('x'), 'ValueSnak'), {})
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce ValueSnak into Value',
            (Property('x'), 'ValueSnak'),
            ValueSnak(Property('p'), Item('x')))
        # success
        assert_type(Property('p')(String('x')), ValueSnak)
        for v, dt in self._test__call__values:
            self.assert_value_snak(
                Property('p')(v), Property('p', dt), Value.check(v))
            self.assert_value_snak(
                cast(ValueSnak, PropertyTemplate('p')(v)),
                Property('p', dt), Value.check(v))
        # variant 2
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce int into Entity',
            (Property('x'), 'Statement'), 0, 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce str into Entity',
            (Property('x'), 'Statement'), 'x', 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI into Entity',
            (Property('x'), 'Statement'), IRI('x'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (Property('x'), 'ValueSnak'), Item('x'), {})
        # success
        assert_type(Property('p')(Item('x'), IRI('y')), Statement)
        it = itertools.product(
            self._test__call__entities, self._test__call__values)
        for e, (v, dt) in it:
            self.assert_statement(
                Property('p')(e, v), e, ValueSnak(Property('p'), v))
            self.assert_statement(
                cast(Statement, PropertyTemplate('p')(e, v)),
                e, ValueSnak(Property('p'), v))

    def test_no_value(self) -> None:
        assert_type(Property('x').no_value(), NoValueSnak)
        self.assert_no_value_snak(Property('x').no_value(), Property('x'))
        self.assert_no_value_snak(
            Property('x', Item).no_value(), Property('x', Item))
        self.assert_no_value_snak(
            Property('x', Quantity).no_value(), Property('x', Quantity))

    def test_some_value(self) -> None:
        assert_type(Property('x').some_value(), SomeValueSnak)
        self.assert_some_value_snak(Property('x').some_value(), Property('x'))
        self.assert_some_value_snak(
            Property('x', Item).some_value(), Property('x', Item))
        self.assert_some_value_snak(
            Property('x', Quantity).some_value(), Property('x', Quantity))

    def test_variables(self) -> None:
        assert_type(Property('x').variables, Set[Variable])
        self._test_variables(Property, (Property('x', Item), set()))

    def test_instantiate(self) -> None:
        assert_type(Item('x').instantiate({}), Term)
        self._test_instantiate(
            Property,
            success=[
                (Property('x', Item),
                 Property('x', Item),
                 {IRI_Variable('x'): IRI('y')})
            ])

    def test_match(self) -> None:
        assert_type(Property('x').match(Variable('x')), Optional[Theta])
        self._test_match(
            Property,
            success=[
                (Property('x'),
                 Property(Variable('x'), Variable('y')),
                 {IRI_Variable('x'): IRI('x'),
                  DatatypeVariable('y'): None}),
                (Property('x', Quantity),
                 Property('x', Variable('y')),
                 {DatatypeVariable('y'): QuantityDatatype()}),
            ],
            failure=[
                (Property('x'), Property('x', Item)),
                (Property('x', Quantity), Property(Variable('x'), Item)),
            ])

    def test_Properties(self) -> None:
        assert_type(Properties('a', 'b', 'c'), Iterable[Property])
        self._test_Entities(
            Properties,
            self.assert_property,
            failure=[
                Item('x'),
                Lexeme('x'),
                Property('x'),
                PropertyTemplate(Variable('x')),
                Text('x'),
                Variable('x', Text),
            ])


if __name__ == '__main__':
    Test.main()
