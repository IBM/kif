# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AnnotatedStatement,
    DeprecatedRank,
    Graph,
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    PreferredRank,
    Property,
    QualifierRecord,
    Quantity,
    SnakSet,
    Statement,
    StatementVariable,
    Text,
    ValueSet,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import ClosedTermSetTestCase


class Test(ClosedTermSetTestCase):

    def test_children_class(self) -> None:
        assert_type(Graph.children_class, type[Statement])
        self.assertIs(Graph.children_class, Statement)

    def test_check(self) -> None:
        assert_type(Graph.check([(Item('x'), Property('y'), 0)]), Graph)
        super()._test_check(
            Graph,
            success=[
                ([], Graph()),
                ([Property('x')(Item('y'), 0, rank=PreferredRank()),
                  Statement(Item('z'), NoValueSnak('w'))],
                 Graph(
                     AnnotatedStatement(
                         Item('y'), Property('x')(0), rank=PreferredRank()),
                     Statement(Item('z'), NoValueSnak('w')))),
            ],
            failure=[
                0,
                [0],
                [Quantity(0)],
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                SnakSet(Property('x')(0)),
                ValueSet(0, 1, 2),
                ValueSnak(Property('x'), 'y'),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(Graph(Statement(Item('x'), Property('y')('z'))), Graph)
        self._test__init__(
            Graph,
            self.assert_graph,
            success=[
                ([Property('x')(Item('y'), 0, rank=DeprecatedRank()),
                  Statement(Item('z'), Property('w').no_value()).annotate(
                      qualifiers=[Property('p')(0)])],
                 Graph(
                     AnnotatedStatement(
                         Item('y'), Property('x')(0), rank=DeprecatedRank),
                     AnnotatedStatement(
                         Item('z'), NoValueSnak(Property('w')),
                         QualifierRecord(Property('p')(0))))),
            ],
            failure=[
                [Item('x'), NoValueSnak('x')],
                [ItemTemplate(Variable('x'))],
                [StatementVariable('x')],
                [Variable('x', Text)],
            ])

    def test__contains__(self) -> None:
        self.assertNotIn(0, Graph())
        self.assertIn(
            Property('p')(Property('q'), 0),
            Graph(Property('p')(Property('q'), 0)))
        self.assertIn(
            Property('p')(Property('q'), 0, rank=DeprecatedRank),
            Graph(Property('p')(Property('q'), 0, rank=DeprecatedRank)))
        self.assertNotIn(
            Property('p')(Property('q'), 0),
            Graph(Property('q')(Property('p'), 0)))
        self.assertNotIn(
            Property('p')(Property('q'), 0),
            Graph(Property('q')(Property('p'), 0, rank=DeprecatedRank())))
        self.assertNotIn(
            Property('p')(Property('q'), 0, rank=DeprecatedRank()),
            Graph(Property('q')(Property('p'), 0)))

    def test_union(self) -> None:
        assert_type(Graph().union(), Graph)
        self.assert_graph(Graph().union(Graph(), Graph()))
        self.assert_graph(
            Graph(Property('x')(Item('y'), 0)).union(
                Graph(Property('x')(Item('y'), 1, rank=PreferredRank()))),
            AnnotatedStatement(
                Item('y'), Property('x')(1), rank=PreferredRank()),
            Statement(Item('y'), Property('x')(0)))
        s1 = Graph(
            Property('p')(Item('i'), IRI('x')),
            Property('q')(Item('j'), IRI('y')))
        s2 = Graph(Statement(Item('i'), NoValueSnak(Property('p'))))
        s3 = Graph()
        s4 = Graph(
            Property('p')(Item('i'), IRI('x')),
            Property('q')(Item('j'), IRI('z'), rank=DeprecatedRank()))
        self.assertEqual(
            s1.union(s2, s3, s4),
            Graph(
                Statement(Item('i'), NoValueSnak(Property('p'))),
                Statement(Item('i'), Property('p')(IRI('x'))),
                Statement(Item('j'), Property('q')(IRI('y'))),
                AnnotatedStatement(Item('j'), Property('q')(IRI('z')),
                                   rank=DeprecatedRank)))


if __name__ == '__main__':
    Test.main()
