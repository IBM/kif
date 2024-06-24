# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime

from kif_lib import (
    Entity,
    ExternalId,
    IRI,
    Item,
    Lexeme,
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    Statement,
    String,
    Text,
    Time,
    Value,
    ValueSnak,
    Variable,
)
from kif_lib.itertools import product
from kif_lib.model import TValue
from kif_lib.typing import assert_type, cast, ClassVar, Iterable

from ...tests import kif_EntityTestCase


class Test(kif_EntityTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Property.datatype_class, type[PropertyDatatype])

    def test_datatype(self) -> None:
        assert_type(Property.datatype, PropertyDatatype)
        self.assertIsInstance(Property.datatype, PropertyDatatype)

    def test_template_class(self) -> None:
        assert_type(Property.template_class, type[PropertyTemplate])

    def test_variable_class(self) -> None:
        assert_type(Property.variable_class, type[PropertyVariable])

    def test_check(self) -> None:
        assert_type(Property.check(Property('x')), Property)
        self._test_check(
            Property,
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
            failure=[
                Item('x'),
                Lexeme('x'),
                PropertyTemplate(Variable('x')),
                Text('x'),
                Variable('x', Text),
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
            (Property('x'), 'ValueSnak'), {})
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce ValueSnak into Value',
            (Property('x'), 'ValueSnak'),
            ValueSnak(Property('p'), Item('x')))
        # success
        assert_type(Property('p')(String('x')), ValueSnak)
        for v in self._test__call__values:
            self.assert_value_snak(
                Property('p')(v), Property('p'), Value.check(v))
            self.assert_value_snak(
                cast(ValueSnak, PropertyTemplate('p')(v)),
                Property('p'), Value.check(v))
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
        it = product(self._test__call__entities, self._test__call__values)
        for e, v in it:
            self.assert_statement(
                Property('p')(e, v), e, ValueSnak(Property('p'), v))
            self.assert_statement(
                cast(Statement, PropertyTemplate('p')(e, v)),
                e, ValueSnak(Property('p'), v))

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
