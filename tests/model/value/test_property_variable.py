# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    AliasProperty,
    DescriptionProperty,
    Entity,
    ExternalId,
    IRI,
    Item,
    itertools,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexicalCategoryProperty,
    NoValueSnakTemplate,
    PreferredRank,
    Property,
    PropertyTemplate,
    PropertyVariable,
    QualifierRecord,
    Quantity,
    RankVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    SomeValueSnakTemplate,
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
from kif_lib.model import TValue
from kif_lib.typing import assert_type, ClassVar, Optional, Set

from ...tests import EntityVariableTestCase


class Test(EntityVariableTestCase):

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

    def test_variables(self) -> None:
        assert_type(PropertyVariable('x').variables, Set[Variable])
        self._test_variables(PropertyVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(
            PropertyVariable('x').instantiate({}), Optional[Term])
        assert_type(PropertyVariable('x').match(
            Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            PropertyVariable,
            success=[
                Property('x'),
                PropertyTemplate(Variable('x')),
                LabelProperty(),
                AliasProperty(),
                DescriptionProperty(),
                LemmaProperty(),
                LexicalCategoryProperty(),
                LanguageProperty(),
            ],
            failure=[
                Item('x'),
                Item(Variable('x')),
                Lexeme('x'),
                Lexeme(Variable('x')),
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
        # statement template
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
        it = itertools.product(
            self._test__call__entities, self._test__call__values)
        for e, v in it:
            self.assert_statement_template(
                PropertyVariable('p')(e, v),
                e, ValueSnak(PropertyVariable('p'), v))
            self.assert_annotated_statement_template(
                PropertyVariable('p')(e, v, [Property('p')(0)]),
                e, ValueSnak(PropertyVariable('p'), v),
                qualifiers=QualifierRecord(Property('p')(0)))
            self.assert_annotated_statement_template(
                PropertyVariable('p')(e, v, None, [[Property('p')(0)]]),
                e, ValueSnak(PropertyVariable('p'), v),
                references=ReferenceRecordSet(
                    ReferenceRecord(Property('p')(0))))
            self.assert_annotated_statement_template(
                PropertyVariable('p')(e, v, None, None, rank=PreferredRank()),
                e, ValueSnak(PropertyVariable('p'), v),
                rank=PreferredRank())
        # value snak template
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

    def test_no_value(self) -> None:
        # statement template
        assert_type(
            PropertyVariable('x').no_value(Item('y')), StatementTemplate)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into Entity',
            (PropertyVariable('x').no_value, 'StatementTemplate'), {})
        self.assert_statement_template(
            PropertyVariable('x').no_value(Item('y')),
            Item('y'), NoValueSnakTemplate(PropertyVariable('x')))
        self.assert_annotated_statement_template(
            PropertyVariable('x').no_value(Item('y'), rank=RankVariable('r')),
            Item('y'), NoValueSnakTemplate(PropertyVariable('x')),
            rank=RankVariable('r'))
        # no value snak template
        assert_type(PropertyVariable('x').no_value(), NoValueSnakTemplate)
        self.assert_no_value_snak_template(
            PropertyVariable('x').no_value(), PropertyVariable('x'))

    def test_some_value(self) -> None:
        # statement template
        assert_type(
            PropertyVariable('x').some_value(Item('y')), StatementTemplate)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into Entity',
            (PropertyVariable('x').some_value, 'StatementTemplate'), {})
        self.assert_statement_template(
            PropertyVariable('x').some_value(Item('y')),
            Item('y'), SomeValueSnakTemplate(PropertyVariable('x')))
        self.assert_annotated_statement_template(
            PropertyVariable('x').some_value(
                Item('y'), rank=RankVariable('r')),
            Item('y'), SomeValueSnakTemplate(PropertyVariable('x')),
            rank=RankVariable('r'))
        # some value snak template
        assert_type(
            PropertyVariable('x').some_value(), SomeValueSnakTemplate)
        self.assert_some_value_snak_template(
            PropertyVariable('x').some_value(), PropertyVariable('x'))


if __name__ == '__main__':
    Test.main()
