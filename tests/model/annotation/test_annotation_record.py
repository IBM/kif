# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    AnnotationRecord,
    Deprecated,
    DeprecatedRank,
    IRI,
    ItemTemplate,
    Lexeme,
    Normal,
    NoValueSnak,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
    SnakSet,
    SomeValueSnak,
    Text,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_check(self) -> None:
        assert_type(
            AnnotationRecord.check(AnnotationRecord()), AnnotationRecord)
        self._test_check(
            AnnotationRecord,
            success=[
                (AnnotationRecord(), AnnotationRecord()),
                (AnnotationRecord(), AnnotationRecord(rank=Normal)),
            ],
            failure=[
                'x',
                0,
                ItemTemplate(Variable('x')),
                Lexeme('x'),
                Property('x'),
                SnakSet(),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        assert_type(AnnotationRecord(), AnnotationRecord)
        self._test__init__(
            AnnotationRecord,
            self.assert_annotation_record,
            success=[
                ([], AnnotationRecord()),
                ([[NoValueSnak(Property('p')), Property('q')(IRI('x'))],
                  [ReferenceRecord(
                      NoValueSnak(Property('p')),
                      SomeValueSnak(Property('q'))),
                   ReferenceRecord(Property('p')(IRI('x')))],
                  Deprecated],
                 AnnotationRecord(
                     SnakSet(
                         NoValueSnak(Property('p')),
                         Property('q')(IRI('x'))),
                     ReferenceRecordSet(
                         ReferenceRecord(
                             NoValueSnak(Property('p')),
                             SomeValueSnak(Property('q'))),
                         ReferenceRecord(Property('p')(IRI('x')))),
                     DeprecatedRank())),
            ],
            failure=[
                [0, ReferenceRecordSet(), Normal],
                [ItemTemplate(Variable('x'))],
                [Lexeme('x')],
                [Normal],
                [Property('x')],
                [ReferenceRecordSet()],
                [SnakSet(), 0, Normal],
                [SnakSet(), ReferenceRecordSet(), 0],
                [Text('x')],
                [Variable('x', Text)],
            ])


if __name__ == '__main__':
    Test.main()
