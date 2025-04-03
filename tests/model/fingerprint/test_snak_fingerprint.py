# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    AliasProperty,
    DescriptionProperty,
    Filter,
    IRI,
    Item,
    LabelProperty,
    LanguageProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexicalCategoryProperty,
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
        assert_type(SnakFingerprint.check(NoValueSnak('x')), SnakFingerprint)
        super()._test_check(
            SnakFingerprint,
            success=[
                (SnakFingerprint(ValueSnak(Property('x'), 'y')),
                 SnakFingerprint(Property('x')('y'))),
                (SnakFingerprint(SomeValueSnak('x')),
                 SnakFingerprint(SomeValueSnak('x'))),
                (SnakFingerprint(NoValueSnak('x')),
                 SnakFingerprint(NoValueSnak('x'))),
                (SnakFingerprint(('x', 'y')),
                 SnakFingerprint(Property('x')('y'))),
                (ValueSnak('x', 'y'),
                 SnakFingerprint(Property('x')('y'))),
                (('x', 'y'),
                 SnakFingerprint(Property('x')('y'))),
                (SomeValueSnak('x'),
                 SnakFingerprint(SomeValueSnak('x'))),
                (NoValueSnak('x'),
                 SnakFingerprint(NoValueSnak('x'))),
            ],
            failure=[
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
        assert_type(SnakFingerprint(NoValueSnak('x')), SnakFingerprint)
        super()._test__init__(
            SnakFingerprint,
            self.assert_snak_fingerprint,
            success=[
                ([ValueSnak('x', 'y')], SnakFingerprint(Property('x')('y'))),
                ([('x', 'y')], SnakFingerprint(Property('x')('y'))),
                ([SomeValueSnak('x')], SnakFingerprint(SomeValueSnak('x'))),
                ([NoValueSnak('x')], SnakFingerprint(NoValueSnak('x'))),
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
            SnakFingerprint(ValueSnak('x', 'y')).datatype_mask,
            Filter.DatatypeMask)
        snaks = [Property('x')(Item('y')), Property('x')('y'),
                 SomeValueSnak('x'), NoValueSnak('x')]
        for fp in map(SnakFingerprint, snaks):
            self.assertEqual(fp.datatype_mask, Filter.ENTITY)

    def test_match(self) -> None:
        assert_type(SnakFingerprint(SomeValueSnak('x')).match('x'), bool)
        snaks = [ValueSnak('x', 'y'), SomeValueSnak('x'), NoValueSnak('x')]
        for fp in map(SnakFingerprint, snaks):
            self.assert_match(fp, Item('z'), Property('z'), Lexeme('z'))
            self.assert_not_match(
                fp, IRI('z'), Text('z'), String('z'), Text('z'),
                Quantity(0), Time('2024-07-27'),
                # Snak fingerprints should not match pseudo properties.
                LabelProperty(), AliasProperty(), DescriptionProperty(),
                LemmaProperty(), LexicalCategoryProperty(),
                LanguageProperty())

    def test_normalize(self) -> None:
        assert_type(SnakFingerprint(('x', 'y')).normalize(), Fingerprint)
        snaks = [ValueSnak('x', 'y'), SomeValueSnak('x'), NoValueSnak('x')]
        for snak in snaks:
            fp = SnakFingerprint(snak)
            self.assert_snak_fingerprint(
                fp.normalize(), snak)
            self.assert_snak_fingerprint(
                fp.normalize(Filter.ENTITY), snak)
            self.assert_snak_fingerprint(
                fp.normalize(Filter.ITEM), snak)
            self.assert_empty_fingerprint(
                fp.normalize(Filter.DEEP_DATA_VALUE))
            self.assert_empty_fingerprint(
                fp.normalize(Filter.IRI))


if __name__ == '__main__':
    Test.main()
