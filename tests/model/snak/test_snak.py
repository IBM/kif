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
from kif_lib.typing import assert_type

from ...tests import kif_SnakTestCase


class Test(kif_SnakTestCase):

    def test_template_class(self) -> None:
        assert_type(Snak.template_class, type[SnakTemplate])
        self.assertIs(Snak.template_class, SnakTemplate)

    def test_variable_class(self) -> None:
        assert_type(Snak.variable_class, type[SnakVariable])
        self.assertIs(Snak.variable_class, SnakVariable)

    def test_mask_check(self):
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Snak.Mask.check, 'abc')
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Snak.Mask.check, 8)
        self.assertEqual(Snak.Mask.check(0), Snak.Mask(0))
        self.assertEqual(Snak.Mask.check(Snak.VALUE_SNAK), Snak.VALUE_SNAK)
        self.assertEqual(Snak.Mask.check_optional(None, Snak.ALL), Snak.ALL)
        self.assertIsNone(Snak.Mask.check_optional(None))

    def test_check(self) -> None:
        assert_type(Snak.check(NoValueSnak('x')), Snak)
        super()._test_check(
            Snak,
            success=[
                (NoValueSnak('x'), NoValueSnak('x')),
                (SomeValueSnak('x'), SomeValueSnak('x')),
                (ValueSnak('x', 'y'), ValueSnak('x', 'y')),
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

    def test__init__(self):
        self.assert_abstract_class(Snak)


if __name__ == '__main__':
    Test.main()
