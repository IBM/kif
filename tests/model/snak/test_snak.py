# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    NoValueSnak,
    Property,
    Snak,
    SnakTemplate,
    SnakVariable,
    SomeValueSnak,
    ValueSnak,
    Variable,
)
from kif_lib.model import (
    AndFingerprint,
    FullFingerprint,
    OrFingerprint,
    SnakFingerprint,
)
from kif_lib.typing import assert_type

from ...tests import kif_SnakTestCase


class Test(kif_SnakTestCase):

    def test_template_class(self) -> None:
        assert_type(Snak.template_class, type[SnakTemplate])
        self.assertIs(Snak.template_class, SnakTemplate)

    def test_variable_class(self) -> None:
        assert_type(Snak.variable_class, type[SnakVariable])
        self.assertIs(Snak.variable_class, SnakVariable)

    def test_check(self) -> None:
        assert_type(Snak.check(NoValueSnak('x')), Snak)
        super()._test_check(
            Snak,
            success=[
                (NoValueSnak('x'), NoValueSnak('x')),
                (SomeValueSnak('x'), SomeValueSnak('x')),
                (ValueSnak('x', 'y'), ValueSnak('x', 'y')),
                (('x', 'y'), ValueSnak('x', 'y')),
            ],
            failure=[
                'x',
                0,
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        self.assert_abstract_class(Snak)

    def test__and__(self) -> None:
        assert_type(ValueSnak('x', 'y') & NoValueSnak('z'), AndFingerprint)
        self.assert_and_fingerprint(
            ValueSnak('x', 'y') & NoValueSnak('z'),
            SnakFingerprint(ValueSnak('x', 'y')),
            SnakFingerprint(NoValueSnak('z')))

    def test__rand__(self) -> None:
        assert_type(True & NoValueSnak('z'), AndFingerprint)
        self.assert_and_fingerprint(
            True & NoValueSnak('z'),
            FullFingerprint(), SnakFingerprint(NoValueSnak('z')))

    def test__or__(self) -> None:
        assert_type(ValueSnak('x', 'y') | NoValueSnak('z'), OrFingerprint)
        self.assert_or_fingerprint(
            ValueSnak('x', 'y') | NoValueSnak('z'),
            SnakFingerprint(ValueSnak('x', 'y')),
            SnakFingerprint(NoValueSnak('z')))

    def test__ror__(self) -> None:
        assert_type(True | NoValueSnak('z'), OrFingerprint)
        self.assert_or_fingerprint(
            True | NoValueSnak('z'),
            FullFingerprint(), SnakFingerprint(NoValueSnak('z')))


if __name__ == '__main__':
    Test.main()
