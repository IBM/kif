# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AnnotatedStatement,
    AnnotatedStatementTemplate,
    AnnotatedStatementVariable,
    DeprecatedRank,
    EntityVariable,
    ExternalId,
    IRI,
    Item,
    ItemTemplate,
    NormalRank,
    NoValueSnak,
    PreferredRank,
    Property,
    QualifierRecord,
    QualifierRecordVariable,
    Quantity,
    RankVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    ReferenceRecordSetVariable,
    SnakVariable,
    SomeValueSnak,
    Statement,
    StatementVariable,
    String,
    Term,
    Text,
    Theta,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import StatementTestCase


class Test(StatementTestCase):

    def test_template_class(self) -> None:
        assert_type(
            AnnotatedStatement.template_class,
            type[AnnotatedStatementTemplate])
        self.assertIs(
            AnnotatedStatement.template_class,
            AnnotatedStatementTemplate)

    def test_variable_class(self) -> None:
        assert_type(
            AnnotatedStatement.variable_class,
            type[AnnotatedStatementVariable])
        self.assertIs(
            AnnotatedStatement.variable_class,
            AnnotatedStatementVariable)

    def test_check(self) -> None:
        assert_type(AnnotatedStatement.check(
            (Item('x'), 'y', 'z')), AnnotatedStatement)
        self._test_check(
            AnnotatedStatement,
            success=[
                ((Item('x'), 'y', 'z'),
                 AnnotatedStatement(
                     Item('x'), ValueSnak(Property('y'), String('z')))),
                ((Item('x'), ('y', 'z')),
                 AnnotatedStatement(
                     Item('x'), ValueSnak(Property('y'), String('z')))),
                ((Item('x'), NoValueSnak('y')),
                 AnnotatedStatement(Item('x'), NoValueSnak(Property('y')))),
                (Property('y')(Property('x'), ExternalId('z')),
                 AnnotatedStatement(
                     Property('x'), Property('y')(ExternalId('z')))),
                (Property('y')(Property('x'), ExternalId('z')).annotate(
                    rank=DeprecatedRank()),
                 AnnotatedStatement(
                     Property('x'),
                     Property('y')(ExternalId('z')),
                     QualifierRecord(),
                     ReferenceRecordSet(),
                     DeprecatedRank()))
            ],
            failure=[
                (0, 'x'),
                (Item('x'), 'x'),
                0,
                Item('x'),
                ItemTemplate(Variable('x')),
                NoValueSnak('x'),
                Quantity(0),
                SomeValueSnak(Property('x')),
                Statement(Variable('x'), Variable('y')),
                Text('x'),
                ValueSnak('x', 'y'),
                Variable('x', Text),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(
            AnnotatedStatement(
                Item('x'), NoValueSnak('y'), rank=PreferredRank),
            AnnotatedStatement)
        self._test__init__(
            AnnotatedStatement,
            self.assert_annotated_statement,
            success=[
                ([Item('x'), ValueSnak('y', 'z'), [Property('p')(0)]],
                 AnnotatedStatement(
                     Item('x'), ValueSnak('y', 'z'),
                     QualifierRecord(Property('p')(0)),
                     ReferenceRecordSet(), NormalRank())),
                ([Item('x'), SomeValueSnak('y'), None,
                  [[Property('p')(0)]], DeprecatedRank],
                 AnnotatedStatement(
                     Item('x'), SomeValueSnak('y'), QualifierRecord(),
                     ReferenceRecordSet(ReferenceRecord(Property('p')(0))),
                     DeprecatedRank())),
                ([Item('x'), Property('y')('z'),
                  None, None, PreferredRank()],
                 (Property('y')(Item('x'), 'z'))@{  # pyright: ignore
                     'rank': PreferredRank, 'replace': False}),
                ([Property('x'), NoValueSnak('y')],
                 AnnotatedStatement(Property('x'), NoValueSnak('y'))),
            ],
            failure=[
                [0, 'x'],
                [IRI('x'), NoValueSnak('x')],
                [Item('x'), Property('x')],
                [NoValueSnak('x'), NoValueSnak('y')],
                [SomeValueSnak('x'), SomeValueSnak('y')],
                [String(Variable('x')), Property('y')],
                [Text('x'), 'x'],
                [ValueSnak('x', 'x'), 'y'],
                [Variable('x', IRI), Variable('y')],
                [{}, 'y'],
            ])

    def test_variables(self) -> None:
        assert_type(
            AnnotatedStatement(Item('x'), SomeValueSnak('y')).variables,
            Set[Variable])
        self._test_variables(
            AnnotatedStatement,
            (AnnotatedStatement(Item('x'), SomeValueSnak('y')), set()))

    def test_instantiate(self) -> None:
        assert_type(
            AnnotatedStatement(
                Item('x'), NoValueSnak('y')).instantiate({}), Term)
        self._test_instantiate(
            AnnotatedStatement,
            success=[
                (AnnotatedStatement(Item('x'), ValueSnak('y', 'z')),
                 AnnotatedStatement(Item('x'), ValueSnak('y', 'z')),
                 {Variable('x'): String('y')}),
            ])

    def test_match(self) -> None:
        assert_type(
            AnnotatedStatement(Item('x'), ValueSnak('y', 'z')).match(
                AnnotatedStatement(Item('x'), ValueSnak('y', 'z'))),
            Optional[Theta])
        self._test_match(
            AnnotatedStatement,
            success=[
                (AnnotatedStatement(Item('x'), ValueSnak('y', 'z')),
                 AnnotatedStatement(
                     Item('x'), ValueSnak('y', 'z'), [], [], NormalRank), {}),
                (AnnotatedStatement(Item('x'), SomeValueSnak('y')),
                 StatementVariable('x'),
                 {StatementVariable('x'):
                  AnnotatedStatement(Item('x'), SomeValueSnak('y'))}),
                (AnnotatedStatement(Item('x'), SomeValueSnak('y')),
                 AnnotatedStatementVariable('x'),
                 {AnnotatedStatementVariable('x'):
                  AnnotatedStatement(Item('x'), SomeValueSnak('y'))}),
                (AnnotatedStatement(Property('x'), NoValueSnak('y')),
                 AnnotatedStatement(Variable('x'), Variable('y')),
                 {EntityVariable('x'): Property('x'),
                  SnakVariable('y'): NoValueSnak('y')}),
                (Property('x')(Item('y'), 'z').annotate(
                    Variable('a'), Variable('b'), Variable('c')),
                 AnnotatedStatement(
                     Item('y'), Property('x')('z'),
                     QualifierRecordVariable('a'),
                     ReferenceRecordSet(ReferenceRecord(Property('p')(0))),
                     RankVariable('c')),
                 {ReferenceRecordSetVariable('b'): ReferenceRecordSet(
                     [Property('p')(0)])}),
            ],
            failure=[
                (AnnotatedStatement(Item('x'), NoValueSnak('y')),
                 AnnotatedStatement(Property('x'), NoValueSnak('y'))),
                (AnnotatedStatement(Item('x'), ValueSnak('y', 'z')),
                 ValueSnak('y', 'z')),
                (AnnotatedStatement(Item('x'), Property('y')('z')),
                 Statement(Item('x'), Property('y')('z'))),
                (AnnotatedStatement(
                    Item('x'), Property('y')('z'), rank=NormalRank),
                 AnnotatedStatement(
                     Item('x'), Property('y')('z'), rank=PreferredRank())),
            ])

    def test_annotate(self) -> None:
        assert_type(
            Statement(Item('x'), SomeValueSnak('y')).annotate(),
            AnnotatedStatement)
        stmt = Statement(Item('x'), SomeValueSnak('y'))
        self.assertEqual(stmt.annotate(), AnnotatedStatement(*stmt))
        self.assert_annotated_statement(
            stmt.annotate([Property('p')(0)]).annotate([Property('q')(1)]),
            stmt[0], stmt[1], QualifierRecord(
                Property('p')(0), Property('q')(1)))
        self.assert_annotated_statement(
            stmt.annotate([Property('p')(0)]).annotate(
                [Property('q')(1)], replace=True),
            stmt[0], stmt[1], QualifierRecord(Property('q')(1)))
        self.assert_annotated_statement(
            stmt
            .annotate(references=[[Property('p')(0)]])
            .annotate(references=[[Property('q')(1)]]),
            stmt[0], stmt[1], references=ReferenceRecordSet(
                ReferenceRecord(Property('p')(0)),
                ReferenceRecord(Property('q')(1))))
        self.assert_annotated_statement(
            stmt
            .annotate(references=[[Property('p')(0)]])
            .annotate(references=[[Property('q')(1)]], replace=True),
            stmt[0], stmt[1], references=ReferenceRecordSet(
                ReferenceRecord(Property('q')(1))))
        self.assert_annotated_statement(
            stmt.annotate(rank=PreferredRank),
            stmt[0], stmt[1], rank=PreferredRank())
        self.assert_annotated_statement(
            stmt.annotate(rank=PreferredRank).annotate(rank=DeprecatedRank),
            stmt[0], stmt[1], rank=DeprecatedRank())
        self.assert_annotated_statement(
            stmt.annotate(rank=PreferredRank).annotate(rank=None),
            stmt[0], stmt[1], rank=PreferredRank())


if __name__ == '__main__':
    Test.main()
