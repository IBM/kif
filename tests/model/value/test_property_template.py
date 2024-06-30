# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime

from kif_lib import (
    Datatype,
    Entity,
    ExternalId,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    PropertyTemplate,
    Quantity,
    Statement,
    StatementTemplate,
    String,
    Text,
    Time,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    Variable,
)
from kif_lib.itertools import product
from kif_lib.model import TValue
from kif_lib.typing import assert_type, cast, ClassVar

from ...tests import kif_EntityTemplateTestCase


class Test(kif_EntityTemplateTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(PropertyTemplate(
            Variable('x')).instantiate({}), KIF_Object)
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

    _test__call__entities: ClassVar[list[Entity]] = [
        Item('x'),
        Lexeme('z'),
        Property('y', Item.datatype)
    ]

    _test__call__values: ClassVar[list[TValue]] = [
        'x',
        0,
        datetime.datetime(2024, 6, 24, tzinfo=datetime.timezone.utc),
        ExternalId('x'),
        IRI('x'),
        Item('x'),
        Property('x'),
        Quantity(0),
        String('x'),
        Text('x', 'y'),
        Time('2024-06-24')
    ]

    def test__call__(self) -> None:
        # variant 1
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
        for v in self._test__call__values:
            self.assert_value_snak_template(
                PropertyTemplate(Variable('x'))(v),
                Property(Variable('x')), Value.check(v))
            self.assert_value_snak(
                cast(ValueSnak, PropertyTemplate('p')(v)),
                Property('p'), Value.check(v))
        # variant 2
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
        for e, v in it:
            self.assert_statement_template(
                PropertyTemplate(
                    Variable('p'))(e, v), e,
                ValueSnak(Property(Variable('p')), v))
            self.assert_statement_template(
                Property('p', Variable('q'))(e, v), e,
                ValueSnak(Property('p', Variable('q')), v))
            self.assert_statement(
                cast(Statement, PropertyTemplate('p')(e, v)),
                e, ValueSnak(Property('p'), v))


if __name__ == '__main__':
    Test.main()
