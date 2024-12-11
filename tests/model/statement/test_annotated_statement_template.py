# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AnnotatedStatement,
    AnnotatedStatementTemplate,
    DatatypeVariable,
    DeprecatedRank,
    Entity,
    EntityVariable,
    IRI,
    IRI_Variable,
    Item,
    ItemVariable,
    Lexeme,
    LexemeTemplate,
    NormalRank,
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    PreferredRank,
    Property,
    PropertyTemplate,
    PropertyVariable,
    QualifierRecord,
    QualifierRecordVariable,
    Quantity,
    RankVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    ReferenceRecordSetVariable,
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
    Variables,
)
from kif_lib.typing import assert_type, cast, Optional, Set

from ...tests import StatementTemplateTestCase


class Test(StatementTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(
            AnnotatedStatementTemplate.object_class, type[AnnotatedStatement])
        self.assertIs(
            AnnotatedStatementTemplate.object_class, AnnotatedStatement)

    def test_check(self) -> None:
        assert_type(
            AnnotatedStatementTemplate.check(
                AnnotatedStatementTemplate(Variable('x'), Variable('y'))),
            AnnotatedStatementTemplate)
        self._test_check(
            AnnotatedStatementTemplate,
            success=[
                (AnnotatedStatementTemplate(Variable('x'), Variable('y')),
                 AnnotatedStatement(EntityVariable('x'), SnakVariable('y'))),
                (AnnotatedStatement(Item('x'), Variable('y')),
                 AnnotatedStatementTemplate(Item('x'), SnakVariable('y'))),
                (AnnotatedStatement(Item('x'), ValueSnak('y', Variable('z'))),
                 AnnotatedStatementTemplate(
                     Item('x'),
                     ValueSnakTemplate(Property('y'), ValueVariable('z')))),
                (AnnotatedStatement(
                    Item('x'), ValueSnak('y', 'z'), [], None, Variable('r')),
                 AnnotatedStatementTemplate(
                     Item('x'), ValueSnak('y', 'z'),
                     QualifierRecord(), ReferenceRecordSet(),
                     RankVariable('r'))),
            ],
            failure=[
                AnnotatedStatementTemplate(Item('x'), ValueSnak('y', 'z')),
                SomeValueSnakTemplate(Variable('x')),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(
            AnnotatedStatementTemplate(Variable('x'), Variable('y')),
            AnnotatedStatementTemplate)
        self._test__init__(
            AnnotatedStatementTemplate,
            self.assert_annotated_statement_template,
            success=[
                ([Variable('x'), Variable('y')],
                 AnnotatedStatementTemplate(
                     EntityVariable('x'), SnakVariable('y'))),
                ([*Variables(*'xyabc')],
                 AnnotatedStatementTemplate(
                     EntityVariable('x'), SnakVariable('y'),
                     QualifierRecordVariable('a'),
                     ReferenceRecordSetVariable('b'),
                     RankVariable('c'))),
                ([Variable('x'), NoValueSnak('y')],
                 AnnotatedStatementTemplate(
                     EntityVariable('x'), NoValueSnak('y'))),
                ([Property('x'), Property(IRI(Variable('x')))(Variable('y'))],
                 AnnotatedStatementTemplate(
                     Property('x'),
                     ValueSnak(
                         Property(IRI(Variable('x', String))),
                         ValueVariable('y')))),
                ([Item(Variable('x')), NoValueSnak(Property(Variable('x')))],
                 AnnotatedStatementTemplate(
                     Item(Variable('x', IRI)),
                     NoValueSnak(Property(Variable('x', IRI))))),
                ([PropertyVariable('x'), ValueSnakVariable('y')],
                 AnnotatedStatementTemplate(
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
            (AnnotatedStatementTemplate, 'AnnotatedStatement'),
            0, Property('p')(0))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce int into Snak',
            (AnnotatedStatementTemplate, 'AnnotatedStatement'),
            Item('x'), 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI_Variable into EntityVariable',
            AnnotatedStatementTemplate, IRI_Variable('x'), x)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce IRI_Variable into SnakVariable',
            AnnotatedStatementTemplate, x, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'cannot coerce ReferenceRecordSetVariable '
            'into QualifierRecordVariable',
            AnnotatedStatementTemplate, Item('x'), x,
            ReferenceRecordSetVariable('y'))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            'cannot coerce QualifierRecordVariable '
            'into ReferenceRecordSetVariable',
            AnnotatedStatementTemplate, Item('x'), x, None,
            QualifierRecordVariable('y'))
        self.assert_raises_bad_argument(
            TypeError, 5, None,
            'cannot coerce EntityVariable into RankVariable',
            AnnotatedStatementTemplate, Item('x'), x, None,
            None, EntityVariable('y'))
        self.assert_annotated_statement_template(
            StatementTemplate(x, Property('p')(0)).annotate(),
            Variable('x', Entity), Property('p')(Quantity(0)))
        self.assert_annotated_statement_template(
            AnnotatedStatementTemplate(Lexeme(x), Property('p')(0)),
            LexemeTemplate(IRI_Variable('x')),
            Property('p')(Quantity(0)))
        self.assert_annotated_statement_template(
            AnnotatedStatementTemplate(Item('x'), x),
            Item('x'), Variable('x', Snak))
        self.assert_annotated_statement_template(
            AnnotatedStatementTemplate(Item('x'), x, [Property('p')(0)]),
            Item('x'), Variable('x', Snak), QualifierRecord(Property('p')(0)))
        self.assert_annotated_statement_template(
            AnnotatedStatementTemplate(Item('x'), x, None, [
                [Property('p')(0)],
                [Property('p')(1), Property('p')(1)]]),
            Item('x'), Variable('x', Snak), references=ReferenceRecordSet(
                ReferenceRecord(Property('p')(0)),
                ReferenceRecord(Property('p')(1), Property('p')(1))))
        self.assert_annotated_statement_template(
            AnnotatedStatement(Item('x'), x, None, None, DeprecatedRank()),
            Item('x'), SnakVariable('x'), rank=DeprecatedRank())
        self.assert_annotated_statement_template(
            AnnotatedStatement(Item('x'), Property('p')(0), x),
            Item('x'), Property('p')(0), QualifierRecordVariable('x'))
        self.assert_annotated_statement_template(
            AnnotatedStatement(Item('x'), Property('p')(0), None, x),
            Item('x'), Property('p')(0),
            references=ReferenceRecordSetVariable('x'))
        self.assert_annotated_statement_template(
            AnnotatedStatement(Item('x'), Property('p')(0), None, None, x),
            Item('x'), Property('p')(0), rank=RankVariable('x'))
        self.assert_annotated_statement_template(
            AnnotatedStatementTemplate(Item('x'), NoValueSnakTemplate(x)),
            Item('x'), NoValueSnakTemplate(PropertyVariable('x')))
        self.assert_annotated_statement_template(
            AnnotatedStatement(Lexeme(x), Property('p')(0)),
            Lexeme(IRI_Variable('x')), Property('p')(Quantity(0)))
        self.assert_annotated_statement_template(
            AnnotatedStatementTemplate(Item('x'), x),
            Item('x'), Variable('x', Snak))
        self.assert_annotated_statement_template(
            AnnotatedStatementTemplate(Item('x'), NoValueSnak(x)).annotate(),
            Item('x'), NoValueSnak(PropertyVariable('x')))
        self.assert_annotated_statement_template(
            PropertyTemplate(x)(Item('i'), String('s')).annotate(),
            Item('i'), PropertyTemplate(x)(String('s')))
        self.assert_annotated_statement(
            cast(AnnotatedStatement,
                 PropertyTemplate('x')(Item('i'), String('s'))).annotate(),
            Item('i'), Property('x')(String('s')))
        self.assertRaises(TypeError, AnnotatedStatement, x, x)
        self.assertEqual(
            AnnotatedStatementTemplate(x, x(x)),
            AnnotatedStatementTemplate(PropertyVariable('x'), ValueSnak(
                PropertyVariable('x'), PropertyVariable('x'))))
        self.assertEqual(
            AnnotatedStatementTemplate(x, SomeValueSnak(x)),
            AnnotatedStatementTemplate(
                PropertyVariable('x'),
                SomeValueSnak(PropertyVariable('x'))))
        self.assertEqual(
            AnnotatedStatementTemplate(x, NoValueSnak(x)),
            AnnotatedStatementTemplate(
                PropertyVariable('x'),
                NoValueSnak(PropertyVariable('x'))))

    def test_variables(self) -> None:
        assert_type(
            AnnotatedStatementTemplate(
                Variable('x'), Variable('y')).variables, Set[Variable])
        self._test_variables(
            AnnotatedStatementTemplate,
            (AnnotatedStatementTemplate(Variable('x'), Variable('y')),
             {EntityVariable('x'), SnakVariable('y')}),
            (AnnotatedStatementTemplate(Property('x'), Variable('y')),
             {SnakVariable('y')}),
            (AnnotatedStatementTemplate(
                Property('x', Variable('y')), Variable('z')),
             {DatatypeVariable('y'), SnakVariable('z')}),
            (AnnotatedStatementTemplate(
                Property('x', Variable('y')),
                ValueSnakVariable('z')),
             {DatatypeVariable('y'), ValueSnakVariable('z')}),
            (AnnotatedStatementTemplate(
                Property('x', Variable('y')),
                NoValueSnak(Variable('z'))),
             {DatatypeVariable('y'), PropertyVariable('z')}),
            (AnnotatedStatementTemplate(
                Property('x', Variable('y')),
                NoValueSnak(Variable('z')), *Variables(*'abc')),
             {DatatypeVariable('y'),
              PropertyVariable('z'),
              QualifierRecordVariable('a'),
              ReferenceRecordSetVariable('b'),
              RankVariable('c')}))

    def test_instantiate(self) -> None:
        assert_type(AnnotatedStatementTemplate(
            Variable('x'), Variable('y')).instantiate({}), Term)
        self._test_instantiate(
            AnnotatedStatementTemplate,
            success=[
                (AnnotatedStatement(Variable('x'), Variable('y')),
                 AnnotatedStatement(Item('x'), NoValueSnak(Variable('y'))),
                 {EntityVariable('x'): Item('x'),
                  SnakVariable('y'): NoValueSnak(PropertyVariable('y'))}),
                (AnnotatedStatement(
                    PropertyVariable('x'),
                    SomeValueSnak(PropertyVariable('x'))),
                 AnnotatedStatement(
                     Property('y', IRI),
                     SomeValueSnak(Property('y', IRI))),
                 {PropertyVariable('x'): Property('y', IRI)}),
                (AnnotatedStatement(
                    Item('x'), Property('y')(0), rank=Variable('x')),
                 Statement(Item('x'), Property('y')(0)).annotate(
                     rank=DeprecatedRank),
                 {RankVariable('x'): DeprecatedRank()})
            ],
            failure=[
                (AnnotatedStatement(Variable('x'), Variable('y')),
                 {EntityVariable('x'): IRI('y')}),
                (AnnotatedStatement(Variable('x'), Variable('y')),
                 {SnakVariable('y'): Property('p')(Item('x'), 'y')}),
                (AnnotatedStatement(
                    Variable('x'), NoValueSnak('p'), Variable('y')),
                 {QualifierRecordVariable('y'): Item('y')}),
                (AnnotatedStatement(
                    ItemVariable('x'),
                    ValueSnak(Property(Variable('y'), IRI), Variable('z'))),
                 {IRI_Variable('z'): ItemVariable('z')}),
            ])

    def test_match(self) -> None:
        assert_type(
            AnnotatedStatementTemplate(Variable('x'), Variable('y')).match(
                Statement(Item('x'), ValueSnak('x', 'y'))), Optional[Theta])
        self._test_match(
            AnnotatedStatementTemplate,
            success=[
                (AnnotatedStatement(Variable('x'), Variable('y')),
                 AnnotatedStatement(Item('x'), ValueSnak('y', 'z')),
                 {EntityVariable('x'): Item('x'),
                  SnakVariable('y'): ValueSnak('y', 'z')}),
                (Statement(
                    ItemVariable('x'), NoValueSnakVariable('y')).annotate(),
                 AnnotatedStatement(Item('x'), SnakVariable('y')),
                 {ItemVariable('x'): Item('x'),
                  SnakVariable('y'): NoValueSnakVariable('y')}),
                (Statement(
                    Variable('x'),
                    ValueSnak('y', Quantity(Variable('w')))).annotate(
                        rank=Variable('r')),
                 Statement(
                     Item('x'),
                     ValueSnak(Variable('y'), Variable('z'))).annotate(),
                 {EntityVariable('x'): Item('x'),
                  PropertyVariable('y'): Property('y', Quantity),
                  ValueVariable('z'): Quantity(Variable('w')),
                  RankVariable('r'): NormalRank()}),
            ],
            failure=[
                (AnnotatedStatement(ItemVariable('x'), ValueSnak('y', 'z')),
                 Statement(Item('x'), ValueSnak('y', 'z'))),
                (AnnotatedStatement(Variable('x'), ValueSnak('y', 'z')),
                 AnnotatedStatement(
                     Item('x'), ValueSnak('y', ValueVariable('z')))),
            ])

    def test_annotate(self) -> None:
        assert_type(
            AnnotatedStatementTemplate(
                Variable('x'), SomeValueSnak('y')).annotate(),
            AnnotatedStatementTemplate)
        stmt = StatementTemplate(Variable('x'), SomeValueSnak('y'))
        self.assertEqual(stmt.annotate(), AnnotatedStatement(*stmt))
        self.assert_annotated_statement_template(
            stmt.annotate([Property('p')(0)]).annotate([Property('q')(1)]),
            stmt[0], stmt[1], QualifierRecord(
                Property('p')(0), Property('q')(1)))
        self.assert_annotated_statement_template(
            stmt.annotate([Property('p')(0)]).annotate(
                [Property('q')(1)], replace=True),
            stmt[0], stmt[1], QualifierRecord(Property('q')(1)))
        self.assert_annotated_statement_template(
            stmt
            .annotate(references=[[Property('p')(0)]])
            .annotate(references=[[Property('q')(1)]]),
            stmt[0], stmt[1], references=ReferenceRecordSet(
                ReferenceRecord(Property('p')(0)),
                ReferenceRecord(Property('q')(1))))
        self.assert_annotated_statement_template(
            stmt
            .annotate(references=[[Property('p')(0)]])
            .annotate(references=[[Property('q')(1)]], replace=True),
            stmt[0], stmt[1], references=ReferenceRecordSet(
                ReferenceRecord(Property('q')(1))))
        self.assert_annotated_statement_template(
            stmt@(None, None, PreferredRank),
            stmt[0], stmt[1], rank=PreferredRank())
        self.assert_annotated_statement_template(
            stmt.annotate(rank=PreferredRank)@{  # pyright: ignore
                'rank': DeprecatedRank},
            stmt[0], stmt[1], rank=DeprecatedRank())
        self.assert_annotated_statement_template(
            stmt.annotate(rank=PreferredRank).annotate(rank=Variable('y')),
            stmt[0], stmt[1], rank=RankVariable('y'))


if __name__ == '__main__':
    Test.main()
