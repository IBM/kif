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
    SnakSet,
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
    OrFingerprint,
    SnakFingerprint,
    ValueFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import FingerprintTestCase


class Test(FingerprintTestCase):

    def test_check(self) -> None:
        assert_type(OrFingerprint.check(OrFingerprint()), OrFingerprint)
        super()._test_check(
            OrFingerprint,
            success=[
                (OrFingerprint(), OrFingerprint()),
                ([], OrFingerprint()),
                (set(), OrFingerprint()),
                ({'x', 'y'},
                 OrFingerprint(
                     ValueFingerprint(String('x')),
                     ValueFingerprint(String('y')))),
                ([('x', 'y')],
                 OrFingerprint(SnakFingerprint(Property('x')('y')))),
                ([FullFingerprint(), EmptyFingerprint()],
                 OrFingerprint(FullFingerprint(), EmptyFingerprint())),
                ((ConverseSnakFingerprint(('x', 'y')),),
                 OrFingerprint(ConverseSnakFingerprint(ValueSnak('x', 'y')))),
                (SnakSet(NoValueSnak('x'), SomeValueSnak('y')),
                 OrFingerprint(NoValueSnak('x'), SomeValueSnak('y')))
            ],
            failure=[
                'x',
                0,
                AndFingerprint(EmptyFingerprint()),
                FullFingerprint(),
                Item(Variable('x')),
                SnakFingerprint(NoValueSnak('x')),
                SnakFingerprint(SomeValueSnak('x')),
                SnakFingerprint(ValueSnak('x', 'y')),
                ValueFingerprint('x'),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(OrFingerprint(ValueSnak('x', Item('x'))), OrFingerprint)
        super()._test__init__(
            OrFingerprint,
            self.assert_or_fingerprint,
            success=[
                ([], OrFingerprint()),
                ([ValueSnak('x', 'y')], OrFingerprint(Property('x')('y'))),
                (['x', 'y', 0],
                 OrFingerprint(
                     ValueFingerprint(String('x')),
                     ValueFingerprint(String('y')),
                     ValueFingerprint(Quantity(0)))),
                ([FullFingerprint(), FullFingerprint()],
                 OrFingerprint(FullFingerprint(), FullFingerprint())),
                ([Item('x')],
                 OrFingerprint(ValueFingerprint(Item('x')))),
                ([None],
                 OrFingerprint(FullFingerprint())),
                ([True, False, None],
                 OrFingerprint(
                     FullFingerprint(),
                     EmptyFingerprint(),
                     FullFingerprint())),
                ([AndFingerprint(True, OrFingerprint(False))],
                 OrFingerprint(AndFingerprint(True, OrFingerprint(False)))),
            ],
            failure=[
                [Variable('x', Item)],
                [{}],
            ])

    def test_datatype_mask(self) -> None:
        assert_type(OrFingerprint().datatype_mask, Filter.DatatypeMask)
        self.assertEqual(
            OrFingerprint(
                Item('x'), Quantity(0, Item('x')),
                EmptyFingerprint()).datatype_mask,
            Filter.ITEM | Filter.QUANTITY)
        self.assertEqual(
            OrFingerprint(
                Item('x'), NoValueSnak('x'), ExternalId('x')).datatype_mask,
            Filter.ITEM | Filter.ENTITY | Filter.EXTERNAL_ID)
        self.assertEqual(
            OrFingerprint(Item('x'), FullFingerprint()).datatype_mask,
            Filter.VALUE)

    def test_match(self) -> None:
        assert_type(OrFingerprint(SomeValueSnak('x')).match('x'), bool)
        fp = OrFingerprint(
            Item('x'), Quantity(0, Item('y')), EmptyFingerprint())
        self.assert_match(
            fp, Item('x'), Quantity(0, Item('y')),
            Quantity(0, Item('y'), 1, 2))
        self.assert_not_match(
            fp, Item('y'), Quantity(1), Quantity(0, Item('x')))
        self.assert_match(
            OrFingerprint(FullFingerprint(), EmptyFingerprint()),
            Item('x'), Property('x'), Lexeme('x'), IRI('x'), Text('x'),
            String('x'), ExternalId('x'), Quantity(0), Time('2024-07-27'))
        self.assert_not_match(
            OrFingerprint(EmptyFingerprint()),
            Item('x'), Property('x'), Lexeme('x'), IRI('x'), Text('x'),
            String('x'), ExternalId('x'), Quantity(0), Time('2024-07-27'))

    def test_normalize(self) -> None:
        assert_type(OrFingerprint('x').normalize(), Fingerprint)
        top, bot = FullFingerprint(), EmptyFingerprint()
        self.assert_full_fingerprint(OrFingerprint().normalize())
        self.assert_full_fingerprint(OrFingerprint(top).normalize())
        self.assert_empty_fingerprint(OrFingerprint(top).normalize(0))
        self.assert_empty_fingerprint(OrFingerprint(bot).normalize())
        # ⊤ ∨ ⊤ -> ⊤
        self.assertEqual(OrFingerprint(top, top).normalize(), top)
        # ⊥ ∨ ⊥ -> ⊥
        self.assertEqual(OrFingerprint(bot, bot).normalize(), bot)
        # ⊤ ∨ x -> ⊤
        self.assertEqual(
            OrFingerprint(top, Item('x')).normalize(),
            FullFingerprint())
        # ⊥ ∨ x -> x
        self.assertEqual(
            OrFingerprint(bot, Item('x')).normalize(),
            ValueFingerprint(Item('x')))
        # A ∨ (B ∨ (C ∨ (D ∨ A))) -> A ∨ B ∨ C ∨ D
        A = ConverseSnakFingerprint(ValueSnak('x', Item('y')))
        B = SnakFingerprint(('x', 'y'))
        C = ValueFingerprint(Quantity(0))
        D = ValueFingerprint(String('A'))
        self.assertEqual(
            (A | (B | (C | (D | A)))).normalize(),
            OrFingerprint(A, B, C, D))
        # A ∨ (B ∨ ⊤) -> ⊤
        self.assertEqual((A | (B | top)).normalize(), top)
        # A ∨ (B ∨ ⊥) -> A ∨ B
        self.assertEqual((A | (B | bot)).normalize(), A | B)
        # (B ∨ ⊤) ∨ A -> ⊤
        self.assertEqual(((B | top) | A).normalize(), top)
        # (B ∨ ⊥) ∨ A -> B ∨ A
        self.assertEqual(((B | bot) | A).normalize(), B | A)
        # A ∨ (B ∧ (C ∨ D)) -> A ∨ (B ∧ (C ∨ D))
        self.assertEqual(
            (A | (B & (C | D))).normalize(),
            (A | (B & (C | D))))


if __name__ == '__main__':
    Test.main()
