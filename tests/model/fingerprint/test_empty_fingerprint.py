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
        assert_type(EmptyFingerprint.check(False), EmptyFingerprint)
        super()._test_check(
            EmptyFingerprint,
            success=[
                (EmptyFingerprint(), EmptyFingerprint()),
                (False, EmptyFingerprint()),
            ],
            failure=[
                AndFingerprint(EmptyFingerprint()),
                FullFingerprint(),
                Item(Variable('x')),
                ValueFingerprint(Item('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        assert_type(EmptyFingerprint(), EmptyFingerprint)
        super()._test__init__(
            EmptyFingerprint,
            self.assert_empty_fingerprint,
            success=[((), EmptyFingerprint())])

    def test_datatype_mask(self) -> None:
        assert_type(EmptyFingerprint().datatype_mask, Filter.DatatypeMask)
        self.assertEqual(
            EmptyFingerprint().datatype_mask, Filter.DatatypeMask(0))

    def test_match(self) -> None:
        assert_type(EmptyFingerprint().match(Item('x')), bool)
        self.assert_not_match(
            EmptyFingerprint(),
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
        assert_type(EmptyFingerprint().normalize(), Fingerprint)
        self.assertEqual(EmptyFingerprint().normalize(), EmptyFingerprint())
        self.assertEqual(EmptyFingerprint().normalize(0), EmptyFingerprint())


if __name__ == '__main__':
    Test.main()
