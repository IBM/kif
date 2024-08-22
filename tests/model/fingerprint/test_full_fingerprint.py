# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    Filter,
    IRI,
    Item,
    Lexeme,
    Property,
    Quantity,
    String,
    Text,
    Time,
    Variable,
)
from kif_lib.model import (
    AndFingerprint,
    EmptyFingerprint,
    Fingerprint,
    FullFingerprint,
    ValueFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import FingerprintTestCase


class Test(FingerprintTestCase):

    def test_check(self) -> None:
        assert_type(FullFingerprint.check(True), FullFingerprint)
        super()._test_check(
            FullFingerprint,
            success=[
                (FullFingerprint(), FullFingerprint()),
                (True, FullFingerprint()),
                (None, FullFingerprint()),
            ],
            failure=[
                AndFingerprint(FullFingerprint()),
                EmptyFingerprint(),
                Item(Variable('x')),
                ValueFingerprint(Item('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(FullFingerprint(), FullFingerprint)
        super()._test__init__(
            FullFingerprint,
            self.assert_full_fingerprint,
            success=[((), FullFingerprint())])

    def test_datatype_mask(self) -> None:
        assert_type(FullFingerprint().datatype_mask, Filter.DatatypeMask)
        self.assertEqual(FullFingerprint().datatype_mask, Filter.VALUE)

    def test_match(self) -> None:
        assert_type(FullFingerprint().match(Item('x')), bool)
        self.assert_match(
            FullFingerprint(),
            'x',
            0,
            Item('x'),
            Property('x'),
            Lexeme('x'),
            IRI('x'),
            Text('x'),
            String('x'),
            ExternalId('x'),
            Quantity(0),
            Time('2024-07-27'))

    def test_normalize(self) -> None:
        assert_type(FullFingerprint().normalize(), Fingerprint)
        self.assertEqual(FullFingerprint().normalize(), FullFingerprint())
        self.assertEqual(FullFingerprint().normalize(0), EmptyFingerprint())


if __name__ == '__main__':
    Test.main()
