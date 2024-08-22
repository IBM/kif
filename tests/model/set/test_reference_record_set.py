# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    Property,
    Quantity,
    ReferenceRecord,
    ReferenceRecordSet,
    SnakSet,
    SomeValueSnak,
    Text,
    ValueSet,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import KIF_ObjectSetTestCase


class Test(KIF_ObjectSetTestCase):

    def test_children_class(self) -> None:
        assert_type(
            ReferenceRecordSet.children_class,
            type[ReferenceRecord])
        self.assertIs(ReferenceRecordSet.children_class, ReferenceRecord)

    def test_check(self) -> None:
        assert_type(
            ReferenceRecordSet.check([ReferenceRecord(ValueSnak('x', 'y'))]),
            ReferenceRecordSet)
        super()._test_check(
            ReferenceRecordSet,
            success=[
                ([], ReferenceRecordSet()),
                ([ReferenceRecord(NoValueSnak('x'), ValueSnak('y', 'z')),
                  ReferenceRecord()],
                 ReferenceRecordSet(
                    ReferenceRecord(NoValueSnak('x'), ValueSnak('y', 'z')),
                    ReferenceRecord())),
                ([SnakSet()],
                 ReferenceRecordSet(ReferenceRecord()))
            ],
            failure=[
                0,
                [0],
                [Quantity(0)],
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                ReferenceRecord(NoValueSnak('x')),
                SnakSet(),
                ValueSet(0, 1, 2),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(
            ReferenceRecordSet(ReferenceRecord(NoValueSnak('x'))),
            ReferenceRecordSet)
        self._test__init__(
            ReferenceRecordSet,
            self.assert_reference_record_set,
            success=[
                ([ReferenceRecord(SomeValueSnak('x'), ValueSnak('y', 'z')),
                  ReferenceRecord(),
                  SnakSet(SomeValueSnak('x')),
                  ReferenceRecord()],
                 ReferenceRecordSet(
                     ReferenceRecord(SomeValueSnak('x'), ValueSnak('y', 'z')),
                     ReferenceRecord(),
                     ReferenceRecord(SomeValueSnak('x'))))
            ],
            failure=[
                [Item('x'), NoValueSnak('x')],
                [ItemTemplate(Variable('x'))],
                [ReferenceRecordSet()],
                [SomeValueSnak('x')],
                [Variable('x')],
                [Variable('x', Text)],
            ])

    def test__contains__(self) -> None:
        self.assertNotIn(0, ReferenceRecordSet())
        self.assertIn(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecordSet(ReferenceRecord(NoValueSnak(Property('p')))))
        self.assertNotIn(
            ReferenceRecord(NoValueSnak(Property('p'))),
            ReferenceRecordSet(ReferenceRecord(NoValueSnak(Property('q')))))

    def test_union(self) -> None:
        assert_type(ReferenceRecordSet().union(), ReferenceRecordSet)
        self.assert_reference_record_set(
            ReferenceRecordSet().union(
                ReferenceRecordSet(), ReferenceRecordSet()))
        self.assert_reference_record_set(
            ReferenceRecordSet(SnakSet(SomeValueSnak('x'))).union(
                ReferenceRecordSet(
                    ReferenceRecord(SomeValueSnak('x')),
                    SnakSet(NoValueSnak('y'))),
                ReferenceRecordSet(
                    ReferenceRecord(ValueSnak('z', 'w')))),
            ReferenceRecord(NoValueSnak('y')),
            ReferenceRecord(SomeValueSnak('x')),
            ReferenceRecord(ValueSnak('z', 'w')))
        s1 = ReferenceRecordSet(
            ReferenceRecord(Property('p')(IRI('x'))),
            ReferenceRecord(Property('q')(IRI('y'))))
        s2 = ReferenceRecordSet(ReferenceRecord(NoValueSnak(Property('p'))))
        s3 = ReferenceRecordSet()
        s4 = ReferenceRecordSet(
            ReferenceRecord(Property('q')(IRI('y'))),
            ReferenceRecord(Property('q')(IRI('z'))))
        self.assertEqual(
            s1.union(s2, s3, s4),
            ReferenceRecordSet(
                *map(ReferenceRecord, [
                    NoValueSnak(Property('p')),
                    Property('p')(IRI('x')),
                    Property('q')(IRI('y')),
                    Property('q')(IRI('z'))])))


if __name__ == '__main__':
    Test.main()
