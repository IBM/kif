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

from ...tests import kif_ObjectSetTestCase


class Test(kif_ObjectSetTestCase):

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


if __name__ == '__main__':
    Test.main()
