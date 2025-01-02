# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Item, Property, Quantity, String, Term, Variable
from kif_lib.typing import assert_type

from ...tests import TermTestCase


class Test(TermTestCase):

    def test__init__(self) -> None:
        self.assert_abstract_class(Term)

    def test_generalize(self) -> None:
        assert_type(Item('x').generalize(), Item)
        self.assertEqual(Item('x'), Item('x'))
        self.assertEqual(
            Quantity(0).generalize(prefix='x'),
            Quantity(0, Variable('x0'), Variable('x1'), Variable('x2')))
        self.assertEqual(
            Quantity(0).generalize(exclude=['x1'], prefix='x'),
            Quantity(0, Variable('x0'), Variable('x2'), Variable('x3')))
        self.assertEqual(len(Quantity(0).generalize().variables), 3)

    def test_rename(self) -> None:
        assert_type(Variable('x').rename(), Variable)
        self.assertEqual(Variable('x').rename(), Variable('x0'))
        self.assertEqual(Variable('x').rename(
            rename=lambda _: iter(('y',))), Variable('y'))
        self.assertEqual(String('x').rename(), String('x'))
        self.assertEqual(
            Item(Variable('x0')).rename(
                [Property(Variable('x1')), 'x2']), Item(Variable('x3')))


if __name__ == '__main__':
    Test.main()
