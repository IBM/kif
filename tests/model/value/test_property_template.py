# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    Datatype,
    DatatypeVariable,
    Entity,
    ExternalId,
    IRI,
    IRI_Variable,
    Item,
    Lexeme,
    NoValueSnakTemplate,
    Property,
    PropertyTemplate,
    QualifierRecord,
    Quantity,
    QuantityDatatype,
    RankVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    SomeValueSnakTemplate,
    Statement,
    StatementTemplate,
    String,
    Term,
    Text,
    Theta,
    Time,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    Variable,
)
from kif_lib.itertools import product
from kif_lib.model import TDatatype, TValue
from kif_lib.typing import assert_type, cast, ClassVar, Optional, Set

from ...tests import EntityTemplateTestCase


class Test(EntityTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(PropertyTemplate.object_class, type[Property])
        self.assertIs(PropertyTemplate.object_class, Property)

    def test_check(self) -> None:
        assert_type(
            PropertyTemplate.check(PropertyTemplate(Variable('x'))),
            PropertyTemplate)
        self._test_check(PropertyTemplate)

    def test__init__(self) -> None:
        assert_type(PropertyTemplate(Variable('x')), PropertyTemplate)
        self._test__init__(
            PropertyTemplate,
            self.assert_property_template,
            success=[
                ([IRI('x'), Variable('y', Datatype)],
                 Property(IRI('x'), Variable('y', Datatype))),
                ([Variable('x', IRI), None],
                 Property(Variable('x', IRI), None)),
                ([Variable('x', IRI), Variable('y', Datatype)],
                 Property(Variable('x', IRI), Variable('y', Datatype))),
            ],
            failure=[
                [Item('x')],
                [Lexeme('x')],
                [Variable('x', IRI), Variable('x', Datatype)],
            ])
        self.assert_property_template(
            PropertyTemplate(Variable('x'), Variable('y')),
            Variable('x', IRI), Variable('y', Datatype))

    def test_variables(self) -> None:
        assert_type(PropertyTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(
            PropertyTemplate,
            (PropertyTemplate(Variable('x'), Variable('y')),
             {IRI_Variable('x'), DatatypeVariable('y')}),
            (PropertyTemplate('x', Variable('y')),
             {DatatypeVariable('y')}))

    def test_instantiate(self) -> None:
        assert_type(PropertyTemplate(
            Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            PropertyTemplate,
            success=[
                (PropertyTemplate(Variable('x'), Variable('y')),
                 Property('x', Item),
                 {Variable('x', IRI): IRI('x'),
                  Variable('y', Datatype): Item.datatype}),
                (PropertyTemplate('x', Variable('y')),
                 Property('x'),
                 {Variable('y', Datatype): None}),
            ],
            failure=[
                (PropertyTemplate(Variable('x'), Variable('y')),
                 {Variable('y', Datatype): Item('x')}),
            ])

    def test_match(self) -> None:
        assert_type(
            PropertyTemplate(Variable('x')).match(Variable('x')),
            Optional[Theta])
        self._test_match(
            PropertyTemplate,
            success=[
                (Property(Variable('x')),
                 Property('x', Variable('y')),
                 {DatatypeVariable('y'): None,
                  IRI_Variable('x'): IRI('x')}),
                (Property('x', Variable('y')),
                 Property(Variable('x'), Quantity),
                 {IRI_Variable('x'): IRI('x'),
                  DatatypeVariable('y'): QuantityDatatype()}),
            ],
            failure=[
                (Property(Variable('x')), Property('x', Item)),
                (Property(Variable('x'), Quantity),
                 Property(Variable('y'), Property)),
            ])

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
        # statement template
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce int into Entity',
            (Property(Variable('x')), 'StatementTemplate'), 0, 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce str into Entity',
            (Property('x', Variable('y')), 'StatementTemplate'), 'x', 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI into Entity',
            (PropertyTemplate(Variable('x')), 'StatementTemplate'),
            IRI('x'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (PropertyTemplate('x', Variable('y')),
             'ValueSnakTemplate'), Item('x'), {})
        # success
        assert_type(
            PropertyTemplate(Variable('p'))(Item('x'), IRI('y')),
            StatementTemplate)
        assert_type(
            PropertyTemplate('x', Variable('y'))(Item('x'), IRI('y')),
            StatementTemplate)
        it = product(self._test__call__entities, self._test__call__values)
        for e, (v, dt) in it:
            self.assert_statement_template(
                PropertyTemplate(
                    Variable('p'))(e, v), e,
                ValueSnak(Property(Variable('p')), v))
            self.assert_statement_template(
                Property('p', Variable('q'))(e, v), e,
                ValueSnak(Property('p', Variable('q')), v))
            self.assert_annotated_statement_template(
                Property('p', Variable('q'))(
                    e, v, [Property('p')(0)]), e,
                ValueSnak(Property('p', Variable('q')), v),
                qualifiers=QualifierRecord(Property('p')(0)))
            self.assert_annotated_statement_template(
                Property('p', Variable('q'))(
                    e, v, None, [[Property('p')(0)]]), e,
                ValueSnak(Property('p', Variable('q')), v),
                references=ReferenceRecordSet(
                    ReferenceRecord(Property('p')(0))))
            self.assert_annotated_statement_template(
                cast(Statement, PropertyTemplate('p')(
                    e, v, rank=RankVariable('r'))),
                e, ValueSnak(Property('p'), v), rank=RankVariable('r'))
            self.assert_statement(
                cast(Statement, PropertyTemplate('p')(e, v)),
                e, ValueSnak(Property('p'), v))
        # value snak template
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (PropertyTemplate(Variable('x')), 'ValueSnakTemplate'), {})
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce ValueSnak into Value',
            (PropertyTemplate('x'), 'ValueSnak'),
            ValueSnak(Property('p'), Item('x')))
        # success
        assert_type(
            PropertyTemplate(Variable('x'))(String('x')), ValueSnakTemplate)
        assert_type(
            PropertyTemplate('x', Variable('y'))(String('x')),
            ValueSnakTemplate)
        for v, dt in self._test__call__values:
            self.assert_value_snak_template(
                PropertyTemplate(Variable('x'))(v),
                Property(Variable('x'), dt), Value.check(v))
            self.assert_value_snak(
                cast(ValueSnak, PropertyTemplate('p')(v)),
                Property('p', dt), Value.check(v))

    def test_no_value(self) -> None:
        x = IRI_Variable('x')
        y = DatatypeVariable('y')
        # statement template
        assert_type(
            PropertyTemplate(x).no_value(Item('y')), StatementTemplate)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into Entity',
            (Property('x', y).no_value, 'StatementTemplate'), {})
        self.assert_statement_template(
            Property(x).no_value(Item('y')),
            Item('y'), NoValueSnakTemplate(Property(x)))
        self.assert_annotated_statement_template(
            Property('x', y).no_value(
                Item('y'), rank=RankVariable('r')),
            Item('y'), NoValueSnakTemplate(Property('x', y)),
            rank=RankVariable('r'))
        # no value snak template
        assert_type(PropertyTemplate(x).no_value(), NoValueSnakTemplate)
        self.assert_no_value_snak_template(
            PropertyTemplate(x).no_value(), PropertyTemplate(x))
        self.assert_no_value_snak_template(
            Property(x, Item).no_value(), Property(x, Item))
        self.assert_no_value_snak_template(
            Property('z', y).no_value(), Property('z', y))
        self.assert_no_value_snak_template(
            Property(x, y).no_value(), Property(x, y))

    def test_some_value(self) -> None:
        x = IRI_Variable('x')
        y = DatatypeVariable('y')
        # statement template
        assert_type(
            PropertyTemplate(x).some_value(Item('y')), StatementTemplate)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into Entity',
            (Property('x', y).some_value, 'StatementTemplate'), {})
        self.assert_statement_template(
            Property(x).some_value(Item('y')),
            Item('y'), SomeValueSnakTemplate(Property(x)))
        self.assert_annotated_statement_template(
            Property('x', y).some_value(
                Item('y'), rank=RankVariable('r')),
            Item('y'), SomeValueSnakTemplate(Property('x', y)),
            rank=RankVariable('r'))
        # some value snak template
        assert_type(PropertyTemplate(x).some_value(), SomeValueSnakTemplate)
        self.assert_some_value_snak_template(
            PropertyTemplate(x).some_value(), PropertyTemplate(x))
        self.assert_some_value_snak_template(
            Property(x, Item).some_value(), Property(x, Item))
        self.assert_some_value_snak_template(
            Property('z', y).some_value(), Property('z', y))
        self.assert_some_value_snak_template(
            Property(x, y).some_value(), Property(x, y))


if __name__ == '__main__':
    Test.main()
