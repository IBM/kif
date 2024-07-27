# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    Fingerprint,
    Item,
    NoValueSnak,
    Property,
    Quantity,
    SnakSet,
    SomeValueSnak,
    String,
    ValueSnak,
    Variable,
)
from kif_lib.model import (
    AndFingerprint,
    ConverseSnakFingerprint,
    EmptyFingerprint,
    FullFingerprint,
    OrFingerprint,
    SnakFingerprint,
    ValueFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import kif_FingerprintTestCase


class Test(kif_FingerprintTestCase):

    def test_check(self) -> None:
        assert_type(Fingerprint.check(None), Fingerprint)
        super()._test_check(
            Fingerprint,
            success=[
                (['x', 'y'], AndFingerprint('x', 'y')),
                ({'y', 'x'}, AndFingerprint('x', 'y')),
                (SnakSet(NoValueSnak('x'), ValueSnak(Property('x'), 'y')),
                 AndFingerprint(NoValueSnak('x'), Property('x')('y'))),
                (ValueFingerprint('x'), ValueFingerprint(String('x'))),
                (('x', 'y'), SnakFingerprint(Property('x')('y'))),
                (SomeValueSnak('x'), SnakFingerprint(SomeValueSnak('x'))),
                (ConverseSnakFingerprint(('x', Item('y'))),
                 ConverseSnakFingerprint(
                     ValueSnak(Property('x'), Item('y')))),
                (None, FullFingerprint()),
                (True, FullFingerprint()),
                (FullFingerprint(), FullFingerprint()),
                (False, EmptyFingerprint()),
                (EmptyFingerprint(), EmptyFingerprint()),
                (0, ValueFingerprint(Quantity(0))),
                ('x', ValueFingerprint(String('x'))),
                (ExternalId('x'), ValueFingerprint(ExternalId('x'))),
            ],
            failure=[
                Item(Variable('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        self.assert_abstract_class(Fingerprint)

    def test__and__(self) -> None:
        assert_type(FullFingerprint() & FullFingerprint(), Fingerprint)
        self.assertEqual(
            FullFingerprint() & ValueFingerprint('x'),
            AndFingerprint(FullFingerprint(), ValueFingerprint(String('x'))))
        self.assertEqual(
            False & ValueFingerprint('x') & SnakFingerprint(('x', 'y')),
            AndFingerprint(
                AndFingerprint(
                    EmptyFingerprint(),
                    ValueFingerprint(String('x'))),
                ('x', 'y')))

    def test__or__(self) -> None:
        assert_type(FullFingerprint() | FullFingerprint(), Fingerprint)
        self.assertEqual(
            FullFingerprint() | ValueFingerprint('x'),
            OrFingerprint(FullFingerprint(), ValueFingerprint(String('x'))))
        print(False | ValueFingerprint('x') | SnakFingerprint(('x', 'y')))
        self.assertEqual(
            False | ValueFingerprint('x') | SnakFingerprint(('x', 'y')),
            OrFingerprint(
                OrFingerprint(
                    EmptyFingerprint(),
                    ValueFingerprint(String('x'))),
                ('x', 'y')))

    def test_is_full(self) -> None:
        assert_type(FullFingerprint().is_full(), bool)
        self.assertTrue(FullFingerprint().is_full())
        self.assertFalse(EmptyFingerprint().is_full())
        self.assertFalse(ValueFingerprint('x').is_full())
        self.assertFalse(SnakFingerprint(('x', 'y')).is_full())
        self.assertFalse((FullFingerprint() & FullFingerprint()).is_full())

    def test_is_empty(self) -> None:
        assert_type(EmptyFingerprint().is_empty(), bool)
        self.assertTrue(EmptyFingerprint().is_empty())
        self.assertFalse(FullFingerprint().is_empty())
        self.assertFalse(ValueFingerprint('x').is_empty())
        self.assertFalse(SnakFingerprint(('x', 'y')).is_empty())
        self.assertFalse((EmptyFingerprint() & EmptyFingerprint()).is_empty())


if __name__ == '__main__':
    Test.main()
