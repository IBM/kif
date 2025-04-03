# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    Property,
    QualifierRecord,
    Quantity,
    ReferenceRecord,
    Snak,
    SnakSet,
    SomeValueSnak,
    Text,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import ClosedTermSetTestCase


class Test(ClosedTermSetTestCase):

    def test_children_class(self) -> None:
        assert_type(ReferenceRecord.children_class, type[Snak])
        self.assertIs(ReferenceRecord.children_class, Snak)

    def test_check(self) -> None:
        assert_type(ReferenceRecord.check(
            [ValueSnak('x', 'y')]), ReferenceRecord)
        super()._test_check(
            ReferenceRecord,
            success=[
                ([], ReferenceRecord()),
                (QualifierRecord(), ReferenceRecord()),
                (ReferenceRecord(), ReferenceRecord()),
                (SnakSet(NoValueSnak('x'), SomeValueSnak('y')),
                 ReferenceRecord(NoValueSnak('x'), SomeValueSnak('y'))),
                ((NoValueSnak('x'), ValueSnak('y', 'z')),
                 ReferenceRecord(NoValueSnak('x'), ValueSnak('y', 'z'))),
            ],
            failure=[
                0,
                [0],
                [Quantity(0)],
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(ReferenceRecord(NoValueSnak('x')), ReferenceRecord)
        self._test__init__(
            ReferenceRecord,
            self.assert_reference_record,
            success=[
                ([SomeValueSnak('x'), ValueSnak('y', 'z'), SomeValueSnak('x')],
                 ReferenceRecord(SomeValueSnak('x'), ValueSnak('y', 'z'))),
            ],
            failure=[
                [Item('x'), NoValueSnak('x')],
                [ItemTemplate(Variable('x'))],
                [Variable('x', Text)],
            ])
        self.assertNotEqual(ReferenceRecord(), SnakSet())
        self.assertEqual(ReferenceRecord(), ReferenceRecord())
        self.assertEqual(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecord(NoValueSnak(Property('p'))))
        self.assertEqual(
            ReferenceRecord(
                SomeValueSnak(Property('q')),
                NoValueSnak(Property('p'))),
            ReferenceRecord(
                NoValueSnak(Property('p')),
                SomeValueSnak(Property('q')),
                NoValueSnak(Property('p'))))
        self.assertNotEqual(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecord(NoValueSnak(Property('q'))))

    def test__contains__(self) -> None:
        self.assertNotIn(0, ReferenceRecord())
        self.assertIn(
            NoValueSnak(Property('p')),
            ReferenceRecord(NoValueSnak(Property('p'))))
        self.assertNotIn(
            NoValueSnak(Property('p')),
            ReferenceRecord(NoValueSnak(Property('q'))))

    def test_union(self) -> None:
        assert_type(ReferenceRecord().union(), ReferenceRecord)
        self.assert_snak_set(ReferenceRecord().union(
            ReferenceRecord(), ReferenceRecord()))
        self.assert_snak_set(
            ReferenceRecord(SomeValueSnak('x')).union(
                ReferenceRecord(SomeValueSnak('x'), NoValueSnak('y')),
                ReferenceRecord(ValueSnak('z', 'w'))),
            NoValueSnak('y'), SomeValueSnak('x'), ValueSnak('z', 'w'))
        s1 = ReferenceRecord(
            Property('p')(IRI('x')),
            Property('q')(IRI('y')))
        s2 = ReferenceRecord(NoValueSnak(Property('p')))
        s3 = ReferenceRecord()
        s4 = SnakSet(
            Property('q')(IRI('y')),
            Property('q')(IRI('z')))
        self.assertEqual(
            s1.union(s2, s3, s4),  # type: ignore
            ReferenceRecord(
                NoValueSnak(Property('p')),
                Property('p')(IRI('x')),
                Property('q')(IRI('y')),
                Property('q')(IRI('z'))))


if __name__ == '__main__':
    Test.main()
