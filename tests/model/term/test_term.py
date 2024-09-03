# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    ItemVariable,
    itertools,
    Lexeme,
    OpenTerm,
    Property,
    PropertyVariable,
    Quantity,
    String,
    Term,
    Text,
    Theta,
    Time,
    Variable,
    Variables,
)
from kif_lib.typing import assert_type, Optional

from ...tests import TermTestCase


class Test(TermTestCase):

    def assert_unify(self, *eqs: tuple[Term, Term]) -> None:
        for input in [eqs, list(map(lambda eq: (eq[1], eq[0]), eqs))]:
            theta = Term.unification(*input)
            self.assertIsNotNone(theta, f'cannot unify {input}')
            assert theta is not None
            for (s, t) in input:
                if isinstance(s, OpenTerm):
                    si = s.instantiate(theta)
                else:
                    si = s
                if isinstance(t, OpenTerm):
                    ti = t.instantiate(theta)
                else:
                    ti = t
                self.assertEqual(si, ti, f'{s} != {t} via {theta}')

    def assert_does_not_unify(self, *eqs: tuple[Term, Term]) -> None:
        self.assertIsNone(Term.unification(*eqs))

    def test__init__(self) -> None:
        self.assert_abstract_class(Term)

    def test_unification(self) -> None:
        assert_type(Term.unification((Item('x'), Item('x'))), Optional[Theta])
        self.assert_unify(
            (Variable('x'), ItemVariable('y')),
            (Variable('y'), Item('z')))
        self.assert_does_not_unify(
            (Variable('x'), ItemVariable('y')),
            (PropertyVariable('y'), Item('z')))

    def test_unification_var_var(self) -> None:
        x, y = Variables('x', 'y')
        self.assert_unify((x, x))
        self.assert_unify((x, y))
        for xt, yt in itertools.permutations(self.ALL_VARIABLE_CLASSES, 2):
            if issubclass(xt, yt) or issubclass(yt, xt):
                self.assert_unify((x@xt, y@yt))
            else:
                self.assert_does_not_unify((x@xt, y@yt))

    def test_unification_term_term(self) -> None:
        # item
        self.assert_unify((Item('x'), Item('x')))
        self.assert_does_not_unify((Item('x'), Item('y')))
        self.assert_does_not_unify((Item('x'), Lexeme('x')))
        self.assert_does_not_unify((Item('x'), Property('x')))
        self.assert_does_not_unify((Item('x'), IRI('x')))
        self.assert_does_not_unify((Item('x'), Text('x')))
        self.assert_does_not_unify((Item('x'), String('x')))
        self.assert_does_not_unify((Item('x'), ExternalId('x')))
        self.assert_does_not_unify((Item('x'), Quantity(0)))
        self.assert_does_not_unify((Item('x'), Time('2024-09-03')))
        # property
        self.assert_unify((Property('x'), Property('x')))
        self.assert_unify((Property('x', Item), Property('x', Item)))
        self.assert_does_not_unify((Property('x'), Property('y')))
        self.assert_does_not_unify((Property('x'), Property('x', Item)))
        self.assert_does_not_unify(
            (Property('x', ExternalId), Property('x', String)))
        # lexeme
        self.assert_unify((Lexeme('x'), Lexeme('x')))
        self.assert_does_not_unify((Lexeme('x'), Lexeme('y')))
        # iri
        self.assert_unify((IRI('x'), IRI('x')))
        self.assert_does_not_unify((IRI('x'), IRI('y')))
        # text
        self.assert_unify((Text('x'), Text('x')))
        self.assert_unify((Text('x', 'a'), Text('x', 'a')))
        self.assert_does_not_unify((Text('x', 'a'), Text('x')))
        self.assert_does_not_unify((Text('x', 'a'), Text('x', 'b')))
        self.assert_does_not_unify((Text('x', 'a'), Text('y', 'b')))
        # string
        self.assert_unify((String('x'), String('x')))
        self.assert_does_not_unify((String('x'), String('y')))
        self.assert_does_not_unify((String('x'), ExternalId('x')))
        # external id
        self.assert_unify((ExternalId('x'), ExternalId('x')))
        self.assert_does_not_unify((ExternalId('x'), ExternalId('y')))
        self.assert_does_not_unify((ExternalId('x'), String('y')))
        # quantity
        self.assert_unify((Quantity(0), Quantity(0)))
        self.assert_unify((Quantity(0, Item('x')), Quantity(0, Item('x'))))
        self.assert_unify(
            (Quantity(0, Item('x'), -1), Quantity(0, Item('x'), -1)))
        self.assert_unify(
            (Quantity(0, Item('x'), -1, 1), Quantity(0, Item('x'), -1, 1)))
        self.assert_does_not_unify((Quantity(0), Quantity(1)))
        self.assert_does_not_unify((Quantity(0, Item('x')), Quantity(0)))
        self.assert_does_not_unify(
            (Quantity(0, Item('x')), Quantity(0, Item('y'))))
        self.assert_does_not_unify((Quantity(0, None, -1), Quantity(0)))
        self.assert_does_not_unify(
            (Quantity(0, None, -1), Quantity(0, None, -2)))
        self.assert_does_not_unify((Quantity(0, None, None, 1), Quantity(0)))
        self.assert_does_not_unify(
            (Quantity(0, None, None, 1), Quantity(0, None, None, 2)))
        # time
        self.assert_unify((Time('2024-09-03'), Time('2024-09-03')))
        self.assert_unify((Time('2024-09-03', 0), Time('2024-09-03', 0)))
        self.assert_unify((Time('2024-09-03', 0, 0), Time('2024-09-03', 0, 0)))
        self.assert_unify((
            Time('2024-09-03', 0, 0, Item('x')),
            Time('2024-09-03', 0, 0, Item('x'))))
        self.assert_does_not_unify((Time('2024-09-03'), Time('2024-09-02')))
        self.assert_does_not_unify(
            (Time('2024-09-03', 0), Time('2024-09-03')))
        self.assert_does_not_unify(
            (Time('2024-09-03', 0), Time('2024-09-03', 1)))
        self.assert_does_not_unify(
            (Time('2024-09-03', 0, 0), Time('2024-09-03', 0)))
        self.assert_does_not_unify(
            (Time('2024-09-03', 0, 0), Time('2024-09-03', 0, 1)))
        self.assert_does_not_unify(
            (Time('2024-09-03', 0, 0, Item('x')), Time('2024-09-03', 0, 0)))
        self.assert_does_not_unify(
            (Time('2024-09-03', 0, 0, Item('x')),
             Time('2024-09-03', 0, 0, Item('y'))))


if __name__ == '__main__':
    Test.main()
