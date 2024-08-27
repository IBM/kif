# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    Filter,
    IRI,
    Item,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    SomeValueSnak,
    String,
    Text,
    Time,
    ValueSnak,
    Variable,
)
from kif_lib.model import (
    AndFingerprint,
    ConverseSnakFingerprint,
    EmptyFingerprint,
    Fingerprint,
    FullFingerprint,
    SnakFingerprint,
    ValueFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import FingerprintTestCase


class Test(FingerprintTestCase):

    def test_check(self) -> None:
        assert_type(ConverseSnakFingerprint.check(
            ValueSnak('x', Item('y'))), ConverseSnakFingerprint)
        super()._test_check(
            ConverseSnakFingerprint,
            success=[
                (ConverseSnakFingerprint(ValueSnak(Property('x'), Item('y'))),
                 ConverseSnakFingerprint(Property('x')(Item('y')))),
                (ConverseSnakFingerprint(ValueSnak(Property('x'), 'y')),
                 ConverseSnakFingerprint(Property('x')('y'))),
                (ConverseSnakFingerprint(('x', Item('y'))),
                 ConverseSnakFingerprint(Property('x')(Item('y')))),
                (ValueSnak('x', Item('y')),
                 ConverseSnakFingerprint(Property('x')(Item('y')))),
                (('x', Item('y')),
                 ConverseSnakFingerprint(Property('x')(Item('y')))),
                (ConverseSnakFingerprint(SomeValueSnak('x')),
                 ConverseSnakFingerprint(SomeValueSnak('x'))),
                (SomeValueSnak('x'),
                 ConverseSnakFingerprint(SomeValueSnak('x'))),
                (ConverseSnakFingerprint(NoValueSnak('x')),
                 ConverseSnakFingerprint(NoValueSnak('x'))),
                (NoValueSnak('x'),
                 ConverseSnakFingerprint(NoValueSnak('x'))),
            ],
            failure=[
                SnakFingerprint(ValueSnak('x', 'y')),
                SnakFingerprint(NoValueSnak('x')),
                SnakFingerprint(SomeValueSnak('x')),
                AndFingerprint(EmptyFingerprint()),
                FullFingerprint(),
                Item(Variable('x')),
                ValueFingerprint('x'),
                Variable('x'),
                {},
                'x',
                0,
            ])

    def test__init__(self) -> None:
        assert_type(ConverseSnakFingerprint(
            ValueSnak('x', Item('x'))), ConverseSnakFingerprint)
        super()._test__init__(
            ConverseSnakFingerprint,
            self.assert_converse_snak_fingerprint,
            success=[
                ([ValueSnak('x', 'y')],
                 ConverseSnakFingerprint(Property('x')('y'))),
                ([('x', 'y')],
                 ConverseSnakFingerprint(Property('x')('y'))),
                ([SomeValueSnak('x')],
                 ConverseSnakFingerprint(SomeValueSnak('x'))),
                ([NoValueSnak('x')],
                 ConverseSnakFingerprint(NoValueSnak('x'))),
            ],
            failure=[
                ['x'],
                [FullFingerprint()],
                [Item('x')],
                [None],
                [Variable('x', Item)],
                [{}],
            ])

    def test_datatype_mask(self) -> None:
        assert_type(
            ConverseSnakFingerprint(ValueSnak('x', 'y')).datatype_mask,
            Filter.DatatypeMask)
        self.assertEqual(
            ConverseSnakFingerprint(Property('x')(Item('y'))).datatype_mask,
            Filter.VALUE)
        snaks = [Property('x')('y'), SomeValueSnak('x'), NoValueSnak('x')]
        for fp in map(ConverseSnakFingerprint, snaks):
            self.assertEqual(fp.datatype_mask, Filter.DatatypeMask(0))

    def test_match(self) -> None:
        assert_type(ConverseSnakFingerprint(
            SomeValueSnak('x')).match('x'), bool)
        self.assert_match(
            ConverseSnakFingerprint(ValueSnak('x', Item('y'))),
            Item('z'), Property('z'), Lexeme('z'), IRI('z'), Text('z'),
            String('z'), ExternalId('z'), Quantity(0), Time('2024-07-27'))
        snaks = [ValueSnak('x', 'y'), SomeValueSnak('x'), NoValueSnak('x')]
        for fp in map(ConverseSnakFingerprint, snaks):
            self.assert_not_match(
                fp, Item('z'), Property('z'), Lexeme('z'), IRI('z'),
                Text('z'), String('z'), ExternalId('z'),
                Quantity(0), Time('2024-07-27'))

    def test_normalize(self) -> None:
        assert_type(ConverseSnakFingerprint(
            ('x', 'y')).normalize(), Fingerprint)
        self.assert_converse_snak_fingerprint(
            ConverseSnakFingerprint(ValueSnak('x', Item('y'))).normalize(),
            Property('x')(Item('y')))
        self.assert_empty_fingerprint(
            ConverseSnakFingerprint(ValueSnak('x', Item('y'))).normalize(0))
        snaks = [ValueSnak('x', 'y'), SomeValueSnak('x'), NoValueSnak('x')]
        for snak in snaks:
            fp = ConverseSnakFingerprint(snak)
            self.assert_empty_fingerprint(fp.normalize())
            self.assert_empty_fingerprint(fp.normalize(Filter.ENTITY))
            self.assert_empty_fingerprint(fp.normalize(Filter.ITEM))
            self.assert_empty_fingerprint(
                fp.normalize(Filter.DEEP_DATA_VALUE))
            self.assert_empty_fingerprint(
                fp.normalize(Filter.IRI))


if __name__ == '__main__':
    Test.main()
