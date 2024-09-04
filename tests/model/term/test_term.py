# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DatatypeVariable,
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemTemplate,
    ItemVariable,
    itertools,
    Lexeme,
    LexemeDatatype,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    OpenTerm,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    Term,
    Text,
    TextDatatype,
    TextTemplate,
    TextVariable,
    Theta,
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    ValueSnak,
    ValueSnakVariable,
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

    def test_unification_invalid_theta(self) -> None:
        x, y, z, w = Variables('x', 'y', 'z', 'w')
        A = QuantityTemplate(x, y, None, w)
        B = QuantityTemplate(y, z, x, w)
        theta = Term.unification((A, B))
        self.assertIsNotNone(theta)
        self.assertRaises(Term.InstantiationError, A.instantiate, theta)

    def test_unification_term_term(self) -> None:
        # datatype
        self.assert_unify((ItemDatatype(), ItemDatatype()))
        self.assert_unify((StringDatatype(), StringDatatype()))
        self.assert_does_not_unify((ItemDatatype(), Item('x')))
        self.assert_does_not_unify((PropertyDatatype(), Property('x')))
        self.assert_does_not_unify((LexemeDatatype(), Lexeme('x')))
        self.assert_does_not_unify((IRI_Datatype(), IRI('x')))
        self.assert_does_not_unify((TextDatatype(), Text('x')))
        self.assert_does_not_unify((StringDatatype(), String('x')))
        self.assert_does_not_unify((StringDatatype(), ExternalIdDatatype()))
        self.assert_does_not_unify((ExternalIdDatatype(), ExternalId('x')))
        self.assert_does_not_unify((QuantityDatatype(), Quantity(0)))
        self.assert_does_not_unify((TimeDatatype(), Time('2024-09-04')))
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
        # value snak
        self.assert_unify(
            (ValueSnak('x', 'y'), ValueSnak(Property('x'), String('y'))))
        self.assert_unify(
            (ValueSnak(Property('x', Quantity), 0),
             ValueSnak('x', Quantity(0))))
        self.assert_does_not_unify(
            (ValueSnak('x', 'y'), ValueSnak(Property('x', ExternalId), 'x')))
        self.assert_does_not_unify((ValueSnak('x', 'y'), ValueSnak('y', 'x')))
        self.assert_does_not_unify((ValueSnak('x', 'y'), Item('x')))
        self.assert_does_not_unify((ValueSnak('x', 'y'), SomeValueSnak('x')))
        self.assert_does_not_unify((ValueSnak('x', 'y'), NoValueSnak('x')))
        # some value snak
        self.assert_unify((SomeValueSnak('x'), SomeValueSnak('x')))
        self.assert_unify((SomeValueSnak('x'), SomeValueSnak(Property('x'))))
        self.assert_does_not_unify((SomeValueSnak('x'), SomeValueSnak('y')))
        self.assert_does_not_unify(
            (SomeValueSnak('x'), SomeValueSnak(Property('x', ExternalId))))
        self.assert_does_not_unify((SomeValueSnak('x'), Item('x')))
        self.assert_does_not_unify((SomeValueSnak('x'), ValueSnak('x', 'y')))
        self.assert_does_not_unify((SomeValueSnak('x'), NoValueSnak('x')))
        # no value snak
        self.assert_unify((NoValueSnak('x'), NoValueSnak('x')))
        self.assert_unify((NoValueSnak('x'), NoValueSnak(Property('x'))))
        self.assert_does_not_unify((NoValueSnak('x'), NoValueSnak('y')))
        self.assert_does_not_unify(
            (NoValueSnak('x'), NoValueSnak(Property('x', ExternalId))))
        self.assert_does_not_unify((NoValueSnak('x'), Item('x')))
        self.assert_does_not_unify((NoValueSnak('x'), ValueSnak('x', 'y')))
        self.assert_does_not_unify((NoValueSnak('x'), SomeValueSnak('x')))
        # statement
        self.assert_unify(
            (Statement(Item('x'), Property('y')('z')),
             Property('y')(Item('x'), 'z')))
        self.assert_unify(
            (Statement(Item('x'), Property('y', ExternalId)('z')),
             Property('y')(Item('x'), ExternalId('z'))))
        self.assert_unify(
            (Statement(Property('x'), NoValueSnak('y')),
             Statement(Property('x'), NoValueSnak(Property('y')))))
        self.assert_does_not_unify(
            (Property('x')(Item('y'), 0), Property('x')(Item('z'), 0)))
        self.assert_does_not_unify(
            (Property('x')(Item('y'), 0), Property('y')(Item('x'), 0)))
        self.assert_does_not_unify(
            (Property('x')(Item('y'), 0), Property('x')(Item('y'), 1)))
        self.assert_does_not_unify(
            (Property('x')(Item('y'), 0), Item('y')))
        self.assert_does_not_unify(
            (Property('x')(Item('y'), 0), ValueSnak('x', 'y')))

    def test_unification_tpl_tpl(self) -> None:
        x, y, z, w = Variables('x', 'y', 'z', 'w')
        # item
        self.assert_unify((ItemTemplate(x), ItemTemplate(y)))
        self.assert_unify((ItemTemplate(x), ItemTemplate(IRI(y))))
        self.assert_does_not_unify((ItemTemplate(x), LexemeTemplate(x)))
        # property
        self.assert_unify((PropertyTemplate(x), PropertyTemplate(y)))
        self.assert_unify((PropertyTemplate(x, y), PropertyTemplate(z)))
        self.assert_unify((PropertyTemplate(x, y), PropertyTemplate(y, z)))
        self.assert_unify((PropertyTemplate(x, y), PropertyTemplate(x, Item)))
        self.assert_does_not_unify(
            (PropertyTemplate(x, Property), PropertyTemplate(y, Item)))
        self.assert_does_not_unify((PropertyTemplate(x), ItemTemplate(x)))
        # lexeme
        self.assert_unify((LexemeTemplate(x), LexemeTemplate(y)))
        self.assert_unify((LexemeTemplate(x), LexemeTemplate(IRI(y))))
        self.assert_does_not_unify((LexemeTemplate(x), ItemTemplate(x)))
        # iri
        self.assert_unify((IRI_Template(x), IRI_Template(y)))
        self.assert_does_not_unify((IRI_Template(x), StringTemplate(y)))
        # text
        self.assert_unify((TextTemplate(x), TextTemplate(y)))
        self.assert_unify((TextTemplate(x, y), TextTemplate(y, z)))
        self.assert_unify((TextTemplate(y, y), TextTemplate(y, z)))
        self.assert_unify((TextTemplate('x', y), TextTemplate(y, 'x')))
        self.assert_does_not_unify(
            (TextTemplate('x', y), TextTemplate(y, 'z')))
        self.assert_does_not_unify(
            (TextTemplate('x', y), TextTemplate('z', y)))
        self.assert_does_not_unify((TextTemplate(x), ItemTemplate(x)))
        # string
        self.assert_unify((StringTemplate(x), StringTemplate(y)))
        self.assert_does_not_unify((StringTemplate(x), ExternalIdTemplate(y)))
        # external id
        self.assert_unify((ExternalIdTemplate(x), ExternalIdTemplate(y)))
        self.assert_does_not_unify((ExternalIdTemplate(x), StringTemplate(y)))
        # quantity
        self.assert_unify((QuantityTemplate(x), QuantityTemplate(y)))
        self.assert_unify((QuantityTemplate(0), QuantityTemplate(y)))
        self.assert_unify((QuantityTemplate(x, y), QuantityTemplate(y, x)))
        self.assert_unify((QuantityTemplate(x, 'y'), QuantityTemplate(x, y)))
        self.assert_unify((QuantityTemplate(x, None), QuantityTemplate(x, y)))
        self.assert_unify(
            (QuantityTemplate(x, y, z, w), QuantityTemplate(y, z, x, w)))
        self.assert_unify(
            (QuantityTemplate(x, y, None, w), QuantityTemplate(x, y, w, w)))
        self.assert_unify(
            (QuantityTemplate(x, y, z, 8.), QuantityTemplate(x, None, x, z)))
        self.assert_unify(
            (QuantityTemplate(x, 'y'), QuantityTemplate(x, Item(y))))
        self.assert_unify(
            (QuantityTemplate(x, 'y', None, None),
             QuantityTemplate(x, Item(y), z, w)))
        self.assert_does_not_unify(
            (QuantityTemplate(x, 'y'), QuantityTemplate(x, None)))
        self.assert_does_not_unify(
            (QuantityTemplate(x, 'y'), QuantityTemplate(x, Item('z'))))
        self.assert_does_not_unify(
            (QuantityTemplate(x, None, y, z), QuantityTemplate(y, 'x', z, x)))
        self.assert_does_not_unify(
            (QuantityTemplate(x, None, 8, 9), QuantityTemplate(y, 'x', z, 8)))
        self.assert_does_not_unify(
            (QuantityTemplate(x, None, x, x), QuantityTemplate(y, None, 8, 9)))
        # time
        self.assert_unify((TimeTemplate(x), TimeTemplate(y)))
        self.assert_unify((TimeTemplate('2024-09-04'), TimeTemplate(y)))
        self.assert_unify((TimeTemplate(x, y), TimeTemplate(y, x)))
        self.assert_unify((TimeTemplate(x, 0), TimeTemplate(x, y)))
        self.assert_unify((TimeTemplate(x, None), TimeTemplate(x, y)))
        self.assert_unify(
            (TimeTemplate(x, y, z, w), TimeTemplate(y, z, x, w)))
        self.assert_unify(
            (TimeTemplate(x, y, None, w), TimeTemplate(x, y, z, w)))
        self.assert_unify(
            (TimeTemplate(x, y, z, 'x'), TimeTemplate(x, None, z, w)))
        self.assert_unify(
            (TimeTemplate(x, None, None, 'y'),
             TimeTemplate(x, None, None, Item(y))))
        self.assert_unify(
            (TimeTemplate(x, 1, None, None),
             TimeTemplate(x, 1, z, w)))
        self.assert_does_not_unify((TimeTemplate(x, 0), TimeTemplate(x, None)))
        self.assert_does_not_unify(
            (TimeTemplate(x, 0), TimeTemplate(x, 1)))
        self.assert_does_not_unify(
            (TimeTemplate(x, None, y, z), TimeTemplate(y, 0, z, x)))
        self.assert_does_not_unify(
            (TimeTemplate(x, 1, 2, None), TimeTemplate(y, z, z, None)))
        # value snak
        # some value snak
        # no value snak
        # statement

    def test_unification_var_term(self) -> None:
        for tv in self.ALL_VARIABLE_CLASSES:
            # datatype
            self._test_unification_var_term(
                tv, DatatypeVariable, ItemDatatype(),
                ExternalIdDatatype(), StringDatatype())
            # item
            self._test_unification_var_term(tv, ItemVariable, Item('x'))
            # property
            self._test_unification_var_term(
                tv, PropertyVariable, Property('x'), Property('x', Item))
            # lexeme
            self._test_unification_var_term(tv, LexemeVariable, Lexeme('x'))
            # iri
            self._test_unification_var_term(tv, IRI_Variable, IRI('x'))
            # text
            self._test_unification_var_term(
                tv, TextVariable, Text('x'), Text('x', 'y'))
            # string
            self._test_unification_var_term(tv, StringVariable, String('x'))
            # external id
            self._test_unification_var_term(
                tv, ExternalIdVariable, ExternalId('x'))
            # quantity
            self._test_unification_var_term(
                tv, QuantityVariable, Quantity(0),
                Quantity(0, 'x'),
                Quantity(0, 'x', -1),
                Quantity(0, 'x', -1, 1))
            # time
            self._test_unification_var_term(
                tv, TimeVariable,
                Time('2024-09-04'),
                Time('2024-09-04', 0),
                Time('2024-09-04', 0, 0),
                Time('2024-09-04', 0, 0, 'x'))
            # value snak
            self._test_unification_var_term(
                tv, ValueSnakVariable, ValueSnak('x', 'y'))
            # some value snak
            self._test_unification_var_term(
                tv, SomeValueSnakVariable, SomeValueSnak('x'))
            # no value snak
            self._test_unification_var_term(
                tv, NoValueSnakVariable, NoValueSnak('x'))
            # statement
            self._test_unification_var_term(
                tv, StatementVariable,
                Statement(Item('x'), ValueSnak('y', 'z')),
                Statement(Item('x'), SomeValueSnak('y')),
                Statement(Item('x'), NoValueSnak('y')))

    def _test_unification_var_term(
            self,
            tv: type[Variable],
            variable_class: type[Variable],
            *terms: Term
    ) -> None:
        for term in terms:
            if issubclass(variable_class, tv):
                self.assert_unify((Variable('x', tv), term))
            elif issubclass(tv, variable_class):
                self.assert_unify((Variable('x', variable_class), term))
            else:
                self.assert_does_not_unify((Variable('x', tv), term))

    def test_unification_var_tpl(self) -> None:
        x, y = Variables('a', 'b')
        for tv in self.ALL_VARIABLE_CLASSES:
            # item
            self._test_unification_var_term(
                tv, ItemVariable, ItemTemplate(x))
            # property
            self._test_unification_var_term(
                tv, PropertyVariable,
                PropertyTemplate(x),
                PropertyTemplate(x, Item),
                PropertyTemplate('x', y),
                PropertyTemplate('x', y))
            # lexeme
            self._test_unification_var_term(
                tv, LexemeVariable, LexemeTemplate(x))
            # iri
            self._test_unification_var_term(tv, IRI_Variable, IRI_Template(x))
            # text
            self._test_unification_var_term(
                tv, TextVariable,
                TextTemplate(x),
                TextTemplate(x, 'y'),
                TextTemplate('x', y),
                TextTemplate(x, y))
            # string
            self._test_unification_var_term(
                tv, StringVariable, StringTemplate(x))
            # external id
            self._test_unification_var_term(
                tv, ExternalIdVariable, ExternalIdTemplate(x))
            # quantity
            self._test_unification_var_term(
                tv, QuantityVariable,
                QuantityTemplate(x),
                QuantityTemplate(0, x),
                QuantityTemplate(0, Item('x'), x),
                QuantityTemplate(0, Item('x'), 0, x))
            # time
            self._test_unification_var_term(
                tv, TimeVariable,
                TimeTemplate(x),
                TimeTemplate('2024-09-04', x),
                TimeTemplate('2024-09-04', 0, x),
                TimeTemplate('2024-09-04', 0, 0, x))
            # value snak
            self._test_unification_var_term(
                tv, ValueSnakVariable,
                ValueSnak(x, 'y'),
                ValueSnak('x', y),
                ValueSnak(PropertyTemplate(x), y),
                ValueSnak(PropertyTemplate(x), ItemTemplate(y)))
            # some value snak
            self._test_unification_var_term(
                tv, SomeValueSnakVariable,
                SomeValueSnakTemplate(x),
                SomeValueSnakTemplate(PropertyTemplate(x)),
                SomeValueSnakTemplate(PropertyTemplate(IRI_Template(x))))
            # no value snak
            self._test_unification_var_term(
                tv, NoValueSnakVariable,
                NoValueSnakTemplate(x),
                NoValueSnakTemplate(PropertyTemplate(x)),
                NoValueSnakTemplate(PropertyTemplate(IRI_Template(x))))
            # statement
            self._test_unification_var_term(
                tv, StatementVariable,
                StatementTemplate(x, ValueSnak('y', 'z')),
                StatementTemplate(ItemTemplate(x), NoValueSnak('y')),
                StatementTemplate(Property('x'), SomeValueSnak(Property(x))))
        # multiple equations
        self.assert_unify(
            (ItemVariable('x'), ItemTemplate(IRI_Variable('y'))),
            (IRI_Variable('y'), IRI_Template(StringVariable('z'))))
        self.assert_unify(
            (ItemVariable('x'), ItemTemplate(IRI_Variable('x'))),
            (IRI_Variable('x'), IRI_Template(StringVariable('x'))))
        self.assert_unify(
            (StringVariable('x'), StringVariable('y')),
            (IRI_Variable('z'), IRI_Template(StringVariable('x'))))
        # bad instantiations
        self.assert_does_not_unify(
            (StringVariable('x'), String(StringVariable('y'))),
            (IRI_Variable('z'), IRI_Template(StringVariable('x'))))
        # occur-check violations
        self.assert_does_not_unify(
            (StringVariable('x'), StringTemplate(StringVariable('x'))))

    def test_unification_var_var(self) -> None:
        x, y = Variables('x', 'y')
        self.assert_unify((x, x))
        self.assert_unify((x, y))
        for tu, tv in itertools.permutations(self.ALL_VARIABLE_CLASSES, 2):
            if issubclass(tu, tv) or issubclass(tv, tu):
                self.assert_unify((x@tu, y@tv))
            else:
                self.assert_does_not_unify((x@tu, y@tv))


if __name__ == '__main__':
    Test.main()
