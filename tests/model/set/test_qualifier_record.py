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
    QualifierRecordVariable,
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

from ...tests import ClosedTermSetTestCase


class Test(ClosedTermSetTestCase):

    def test_children_class(self) -> None:
        assert_type(QualifierRecord.children_class, type[Snak])
        self.assertIs(QualifierRecord.children_class, Snak)

    def test_variable_class(self) -> None:
        assert_type(
            QualifierRecord.variable_class, type[QualifierRecordVariable])
        self.assertIs(QualifierRecord.variable_class, QualifierRecordVariable)

    def test_check(self) -> None:
        assert_type(QualifierRecord.check(
            [ValueSnak('x', 'y')]), QualifierRecord)
        super()._test_check(
            QualifierRecord,
            success=[
                ([], QualifierRecord()),
                (QualifierRecord(), QualifierRecord()),
                (ReferenceRecord(), QualifierRecord()),
                (SnakSet(NoValueSnak('x'), SomeValueSnak('y')),
                 QualifierRecord(NoValueSnak('x'), SomeValueSnak('y'))),
                ((NoValueSnak('x'), ValueSnak('y', 'z')),
                 QualifierRecord(NoValueSnak('x'), ValueSnak('y', 'z'))),
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
        assert_type(QualifierRecord(NoValueSnak('x')), QualifierRecord)
        self._test__init__(
            QualifierRecord,
            self.assert_qualifier_record,
            success=[
                ([SomeValueSnak('x'), ValueSnak('y', 'z'), SomeValueSnak('x')],
                 QualifierRecord(SomeValueSnak('x'), ValueSnak('y', 'z'))),
            ],
            failure=[
                [Item('x'), NoValueSnak('x')],
                [ItemTemplate(Variable('x'))],
                [Variable('x', Text)],
            ])
        self.assertNotEqual(QualifierRecord(), SnakSet())
        self.assertEqual(QualifierRecord(), QualifierRecord())
        self.assertEqual(
            QualifierRecord(NoValueSnak(Property('p'))),
            QualifierRecord(NoValueSnak(Property('p'))))
        self.assertEqual(
            QualifierRecord(
                SomeValueSnak(Property('q')),
                NoValueSnak(Property('p'))),
            QualifierRecord(
                NoValueSnak(Property('p')),
                SomeValueSnak(Property('q')),
                NoValueSnak(Property('p'))))
        self.assertNotEqual(
            QualifierRecord(NoValueSnak(Property('p'))),
            QualifierRecord(NoValueSnak(Property('q'))))

    def test__contains__(self) -> None:
        self.assertNotIn(0, QualifierRecord())
        self.assertIn(
            NoValueSnak(Property('p')),
            QualifierRecord(NoValueSnak(Property('p'))))
        self.assertNotIn(
            NoValueSnak(Property('p')),
            QualifierRecord(NoValueSnak(Property('q'))))

    def test_union(self) -> None:
        assert_type(QualifierRecord().union(), QualifierRecord)
        self.assert_snak_set(QualifierRecord().union(
            QualifierRecord(), QualifierRecord()))
        self.assert_snak_set(
            QualifierRecord(SomeValueSnak('x')).union(
                QualifierRecord(SomeValueSnak('x'), NoValueSnak('y')),
                QualifierRecord(ValueSnak('z', 'w'))),
            NoValueSnak('y'), SomeValueSnak('x'), ValueSnak('z', 'w'))
        s1 = QualifierRecord(
            Property('p')(IRI('x')),
            Property('q')(IRI('y')))
        s2 = QualifierRecord(NoValueSnak(Property('p')))
        s3 = QualifierRecord()
        s4 = SnakSet(
            Property('q')(IRI('y')),
            Property('q')(IRI('z')))
        self.assertEqual(
            s1.union(s2, s3, s4),  # type: ignore
            QualifierRecord(
                NoValueSnak(Property('p')),
                Property('p')(IRI('x')),
                Property('q')(IRI('y')),
                Property('q')(IRI('z'))))


if __name__ == '__main__':
    Test.main()
