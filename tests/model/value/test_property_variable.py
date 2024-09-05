# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    Entity,
    ExternalId,
    IRI,
    Item,
    Lexeme,
    NoValueSnakTemplate,
    Property,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    SomeValueSnakTemplate,
    StatementTemplate,
    String,
    Term,
    Text,
    Time,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    Variable,
)
from kif_lib.itertools import product
from kif_lib.model import TValue
from kif_lib.typing import assert_type, ClassVar, Optional

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(PropertyVariable.object_class, type[Property])
        self.assertIs(PropertyVariable.object_class, Property)

    def test_check(self) -> None:
        assert_type(
            PropertyVariable.check(PropertyVariable('x')), PropertyVariable)
        assert_type(
            PropertyVariable.check(Variable('x', Property)), PropertyVariable)
        self._test_check(PropertyVariable)

    def test__init__(self) -> None:
        assert_type(PropertyVariable('x'), PropertyVariable)
        self._test__init__(PropertyVariable, self.assert_property_variable)

    def test_instantiate(self) -> None:
        assert_type(
            PropertyVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            PropertyVariable,
            success_auto=[
                Property('x'),
                PropertyTemplate(Variable('x')),
            ],
            failure_auto=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Lexeme('x'),
                Lexeme.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
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
            (PropertyVariable('x'), 'ValueSnakTemplate'), {})
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce ValueSnak into Value',
            (PropertyVariable('x'), 'ValueSnakTemplate'),
            ValueSnakTemplate(Property('p'), Item('x')))
        # success
        assert_type(PropertyVariable('x')('y'), ValueSnakTemplate)
        for v in self._test__call__values:
            self.assert_value_snak_template(
                PropertyVariable('p')(v),
                PropertyVariable('p'), Value.check(v))
        # variant 2
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce int into Entity',
            (PropertyVariable('x'), 'StatementTemplate'), 0, 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce str into Entity',
            (PropertyVariable('x'), 'StatementTemplate'), 'x', 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI into Entity',
            (PropertyVariable('x'), 'StatementTemplate'), IRI('x'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (PropertyVariable('x'), 'ValueSnakTemplate'), Item('x'), {})
        assert_type(
            PropertyVariable('p')(Item('x'), IRI('y')), StatementTemplate)
        it = product(self._test__call__entities, self._test__call__values)
        for e, v in it:
            self.assert_statement_template(
                PropertyVariable('p')(e, v),
                e, ValueSnak(PropertyVariable('p'), v))

    def test_no_value(self) -> None:
        assert_type(PropertyVariable('x').no_value(), NoValueSnakTemplate)
        self.assert_no_value_snak_template(
            PropertyVariable('x').no_value(), PropertyVariable('x'))

    def test_some_value(self) -> None:
        assert_type(PropertyVariable('x').some_value(), SomeValueSnakTemplate)
        self.assert_some_value_snak_template(
            PropertyVariable('x').some_value(), PropertyVariable('x'))


if __name__ == '__main__':
    Test.main()
