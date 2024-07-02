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
    Snak,
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
        assert_type(ReferenceRecord.children_class, type[Snak])
        self.assertIs(ReferenceRecord.children_class, Snak)

    def test_check(self) -> None:
        assert_type(ReferenceRecord.check(
            [ValueSnak('x', 'y')]), ReferenceRecord)
        super()._test_check(
            ReferenceRecord,
            success=[
                ([], ReferenceRecord()),
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
                ValueSet(0, 1, 2),
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

    def test_union(self) -> None:
        assert_type(ReferenceRecord().union(), ReferenceRecord)
        self.assert_snak_set(ReferenceRecord().union(
            ReferenceRecord(), ReferenceRecord()))
        self.assert_snak_set(
            ReferenceRecord(SomeValueSnak('x')).union(
                ReferenceRecord(SomeValueSnak('x'), NoValueSnak('y')),
                ReferenceRecord(ValueSnak('z', 'w'))),
            NoValueSnak('y'), SomeValueSnak('x'), ValueSnak('z', 'w'))


if __name__ == '__main__':
    Test.main()
