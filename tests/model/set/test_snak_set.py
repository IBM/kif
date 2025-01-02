# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    Property,
    Quantity,
    Snak,
    SnakSet,
    SomeValueSnak,
    Text,
    ValueSet,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import ClosedTermSetTestCase


class Test(ClosedTermSetTestCase):

    def test_children_class(self) -> None:
        assert_type(SnakSet.children_class, type[Snak])
        self.assertIs(SnakSet.children_class, Snak)

    def test_check(self) -> None:
        assert_type(SnakSet.check([ValueSnak('x', 'y')]), SnakSet)
        super()._test_check(
            SnakSet,
            success=[
                ([], SnakSet()),
                ((NoValueSnak('x'), ValueSnak('y', 'z')),
                 SnakSet(NoValueSnak('x'), ValueSnak('y', 'z'))),
            ],
            failure=[
                0,
                [0],
                [Quantity(0)],
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                ValueSet(0, 1, 2),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(SnakSet(NoValueSnak('x')), SnakSet)
        self._test__init__(
            SnakSet,
            self.assert_snak_set,
            success=[
                ([SomeValueSnak('x'), ValueSnak('y', 'z'), SomeValueSnak('x')],
                 SnakSet(SomeValueSnak('x'), ValueSnak('y', 'z'))),
            ],
            failure=[
                [Item('x'), NoValueSnak('x')],
                [ItemTemplate(Variable('x'))],
                [Variable('x', Text)],
            ])

    def test__contains__(self) -> None:
        self.assertNotIn(0, SnakSet())
        self.assertIn(
            NoValueSnak(Property('p')), SnakSet(NoValueSnak(Property('p'))))
        self.assertNotIn(
            NoValueSnak(Property('p')), SnakSet(NoValueSnak(Property('q'))))

    def test_union(self) -> None:
        assert_type(SnakSet().union(), SnakSet)
        self.assert_snak_set(SnakSet().union(SnakSet(), SnakSet()))
        self.assert_snak_set(
            SnakSet(SomeValueSnak('x')).union(
                SnakSet(SomeValueSnak('x'), NoValueSnak('y')),
                SnakSet(ValueSnak('z', 'w'))),
            NoValueSnak('y'), SomeValueSnak('x'), ValueSnak('z', 'w'))
        s1 = SnakSet(
            Property('p')(IRI('x')),
            Property('q')(IRI('y')))
        s2 = SnakSet(NoValueSnak(Property('p')))
        s3 = SnakSet()
        s4 = SnakSet(
            Property('q')(IRI('y')),
            Property('q')(IRI('z')))
        self.assertEqual(
            s1.union(s2, s3, s4),
            SnakSet(
                NoValueSnak(Property('p')),
                Property('p')(IRI('x')),
                Property('q')(IRI('y')),
                Property('q')(IRI('z'))))


if __name__ == '__main__':
    Test.main()
