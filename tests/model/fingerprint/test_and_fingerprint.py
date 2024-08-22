# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

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
        assert_type(AndFingerprint.check(AndFingerprint()), AndFingerprint)
        super()._test_check(
            AndFingerprint,
            success=[
                (AndFingerprint(), AndFingerprint()),
                ([], AndFingerprint()),
                (set(), AndFingerprint()),
                ({'x', 'y'},
                 AndFingerprint(
                     ValueFingerprint(String('x')),
                     ValueFingerprint(String('y')))),
                ([('x', 'y')],
                 AndFingerprint(SnakFingerprint(Property('x')('y')))),
                ([FullFingerprint(), EmptyFingerprint()],
                 AndFingerprint(FullFingerprint(), EmptyFingerprint())),
                ((ConverseSnakFingerprint(('x', 'y')),),
                 AndFingerprint(ConverseSnakFingerprint(ValueSnak('x', 'y')))),
                (SnakSet(NoValueSnak('x'), SomeValueSnak('y')),
                 AndFingerprint(NoValueSnak('x'), SomeValueSnak('y')))
            ],
            failure=[
                'x',
                0,
                FullFingerprint(),
                Item(Variable('x')),
                OrFingerprint(EmptyFingerprint()),
                SnakFingerprint(NoValueSnak('x')),
                SnakFingerprint(SomeValueSnak('x')),
                SnakFingerprint(ValueSnak('x', 'y')),
                ValueFingerprint('x'),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(AndFingerprint(ValueSnak('x', Item('x'))), AndFingerprint)
        super()._test__init__(
            AndFingerprint,
            self.assert_and_fingerprint,
            success=[
                ([], AndFingerprint()),
                ([ValueSnak('x', 'y')], AndFingerprint(Property('x')('y'))),
                (['x', 'y', 0],
                 AndFingerprint(
                     ValueFingerprint(String('x')),
                     ValueFingerprint(String('y')),
                     ValueFingerprint(Quantity(0)))),
                ([FullFingerprint(), FullFingerprint()],
                 AndFingerprint(FullFingerprint(), FullFingerprint())),
                ([Item('x')],
                 AndFingerprint(ValueFingerprint(Item('x')))),
                ([None],
                 AndFingerprint(FullFingerprint())),
                ([True, False, None],
                 AndFingerprint(
                     FullFingerprint(),
                     EmptyFingerprint(),
                     FullFingerprint())),
                ([AndFingerprint(True, AndFingerprint(False))],
                 AndFingerprint(AndFingerprint(True, AndFingerprint(False)))),
            ],
            failure=[
                [Variable('x', Item)],
                [{}],
            ])

    def test_datatype_mask(self) -> None:
        assert_type(AndFingerprint().datatype_mask, Filter.DatatypeMask)
        self.assertEqual(
            AndFingerprint(Item('x'), Property('x')('y')).datatype_mask,
            Filter.ITEM & Filter.ENTITY)
        self.assertEqual(
            AndFingerprint(
                Item('x'), NoValueSnak('x'),
                ConverseSnakFingerprint(Property('x')(Item('y')))
            ).datatype_mask,
            Filter.ITEM & Filter.ENTITY & Filter.VALUE)
        self.assertEqual(
            AndFingerprint(Item('x'), FullFingerprint()).datatype_mask,
            Filter.ITEM)
        self.assertEqual(
            AndFingerprint(
                NoValueSnak('x'),
                OrFingerprint(Item('x'), Property('x'))).datatype_mask,
            Filter.ENTITY & (Filter.ITEM | Filter.PROPERTY))
        self.assertEqual(
            AndFingerprint(Item('x'), String('y')).datatype_mask,
            Filter.ITEM & Filter.STRING)

    def test_match(self) -> None:
        assert_type(AndFingerprint(SomeValueSnak('x')).match('x'), bool)
        self.assert_match(AndFingerprint(FullFingerprint()), Item('x'))
        self.assert_not_match(AndFingerprint(EmptyFingerprint()), Item('x'))
        self.assert_not_match(
            AndFingerprint(Item('x'), Item('y')), Item('x'))
        self.assert_not_match(
            AndFingerprint(IRI('x'), Property('y')('x')),
            IRI('x'), Item('x'))
        self.assert_match(
            AndFingerprint(Property('x')('y'), NoValueSnak('z')),
            Item('x'))
        self.assert_not_match(
            AndFingerprint(Property('x')('y'), NoValueSnak('z')),
            IRI('x'))
        self.assert_match(
            AndFingerprint(
                -ValueSnak('x', Item('y')),
                -ValueSnak('x', Item('z'))),
            IRI('x'))
        self.assert_not_match(
            AndFingerprint(FullFingerprint(), EmptyFingerprint()),
            Item('x'), Property('x'), Lexeme('x'), IRI('x'), Text('x'),
            String('x'), ExternalId('x'), Quantity(0), Time('2024-07-27'))
        self.assert_match(
            AndFingerprint(FullFingerprint()),
            Item('x'), Property('x'), Lexeme('x'), IRI('x'), Text('x'),
            String('x'), ExternalId('x'), Quantity(0), Time('2024-07-27'))

    def test_normalize(self) -> None:
        assert_type(AndFingerprint('x').normalize(), Fingerprint)
        top, bot = FullFingerprint(), EmptyFingerprint()
        self.assert_full_fingerprint(AndFingerprint().normalize())
        self.assert_full_fingerprint(AndFingerprint(top).normalize())
        self.assert_empty_fingerprint(AndFingerprint(top).normalize(0))
        self.assert_empty_fingerprint(AndFingerprint(bot).normalize())
        # ⊤ ∧ ⊤ -> ⊤
        self.assertEqual(AndFingerprint(top, top).normalize(), top)
        # ⊥ ∧ ⊥ -> ⊥
        self.assertEqual(AndFingerprint(bot, bot).normalize(), bot)
        # ⊥ ∧ x -> ⊥
        self.assertEqual(
            AndFingerprint(bot, Item('x')).normalize(),
            EmptyFingerprint())
        # ⊤ ∧ x -> x
        self.assertEqual(
            AndFingerprint(top, Item('x')).normalize(),
            ValueFingerprint(Item('x')))
        # A ∧ (B ∧ (C ∧ (D ∧ A))) -> A ∧ B ∧ C ∧ D
        A = ConverseSnakFingerprint(ValueSnak('x', Item('y')))
        B = SnakFingerprint(('x', 'y'))
        C = Property('x')('z')
        D = Property('y')('z')
        self.assertEqual(
            (A & (B & (C & (D & A)))).normalize(),
            AndFingerprint(A, B, C, D))
        # A ∧ (B ∧ ⊤) -> A ∧ B
        self.assertEqual((A & (B & top)).normalize(), A & B)
        # A ∧ (B ∧ ⊥) -> ⊥
        self.assertEqual((A & (B & bot)).normalize(), bot)
        # (B ∧ ⊤) ∧ A -> B ∧ A
        self.assertEqual(((B & top) & A).normalize(), B & A)
        # (B ∧ ⊥) ∧ A -> ⊥
        self.assertEqual(((B & bot) & A).normalize(), bot)
        # A ∧ (B ∨ (C ∧ D)) -> A ∧ (B ∨ (C ∧ D))
        self.assertEqual(
            (A & (B | (C & D))).normalize(),
            (A & (B | (C & D))))


if __name__ == '__main__':
    Test.main()
