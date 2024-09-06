# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DatatypeVariable,
    Entity,
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
    Value,
    ValueSnak,
    ValueSnakVariable,
    Variable,
    Variables,
)
from kif_lib.typing import assert_type, Optional

from ...tests import TermTestCase


class Test(TermTestCase):

    def assert_U(self, *eqs: tuple[Term, Term]) -> None:
        for input in [eqs, list(map(lambda eq: (eq[1], eq[0]), eqs))]:
            theta = Term.unify(*input)
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

    def assert_X(self, *eqs: tuple[Term, Term]) -> None:
        self.assertIsNone(Term.unify(*eqs))

    def test_unify(self) -> None:
        assert_type(Term.unify((Item('x'), Item('x'))), Optional[Theta])
        self.assert_U(
            (Variable('x'), ItemVariable('y')),
            (Variable('y'), Item('z')))
        self.assert_X(
            (Variable('x'), ItemVariable('y')),
            (PropertyVariable('y'), Item('z')))

    def test_unify_invalid_theta(self) -> None:
        x, y, z, w = Variables('x', 'y', 'z', 'w')
        A = QuantityTemplate(x, y, None, w)
        B = QuantityTemplate(y, z, x, w)
        theta = Term.unify((A, B))
        self.assertIsNotNone(theta)
        self.assertRaises(Term.InstantiationError, A.instantiate, theta)

    def test_unify_term_term(self) -> None:
        # datatype
        self.assert_U((ItemDatatype(), ItemDatatype()))
        self.assert_U((StringDatatype(), StringDatatype()))
        self.assert_X((ItemDatatype(), Item('x')))
        self.assert_X((PropertyDatatype(), Property('x')))
        self.assert_X((LexemeDatatype(), Lexeme('x')))
        self.assert_X((IRI_Datatype(), IRI('x')))
        self.assert_X((TextDatatype(), Text('x')))
        self.assert_X((StringDatatype(), String('x')))
        self.assert_X((StringDatatype(), ExternalIdDatatype()))
        self.assert_X((ExternalIdDatatype(), ExternalId('x')))
        self.assert_X((QuantityDatatype(), Quantity(0)))
        self.assert_X((TimeDatatype(), Time('2024-09-04')))
        # item
        self.assert_U((Item('x'), Item('x')))
        self.assert_X((Item('x'), Item('y')))
        self.assert_X((Item('x'), Lexeme('x')))
        self.assert_X((Item('x'), Property('x')))
        self.assert_X((Item('x'), IRI('x')))
        self.assert_X((Item('x'), Text('x')))
        self.assert_X((Item('x'), String('x')))
        self.assert_X((Item('x'), ExternalId('x')))
        self.assert_X((Item('x'), Quantity(0)))
        self.assert_X((Item('x'), Time('2024-09-03')))
        # property
        self.assert_U((Property('x'), Property('x')))
        self.assert_U((Property('x', Item), Property('x', Item)))
        self.assert_X((Property('x'), Property('y')))
        self.assert_X((Property('x'), Property('x', Item)))
        self.assert_X((Property('x', ExternalId), Property('x', String)))
        # lexeme
        self.assert_U((Lexeme('x'), Lexeme('x')))
        self.assert_X((Lexeme('x'), Lexeme('y')))
        # iri
        self.assert_U((IRI('x'), IRI('x')))
        self.assert_X((IRI('x'), IRI('y')))
        # text
        self.assert_U((Text('x'), Text('x')))
        self.assert_U((Text('x', 'a'), Text('x', 'a')))
        self.assert_X((Text('x', 'a'), Text('x')))
        self.assert_X((Text('x', 'a'), Text('x', 'b')))
        self.assert_X((Text('x', 'a'), Text('y', 'b')))
        # string
        self.assert_U((String('x'), String('x')))
        self.assert_X((String('x'), String('y')))
        self.assert_X((String('x'), ExternalId('x')))
        # external id
        self.assert_U((ExternalId('x'), ExternalId('x')))
        self.assert_X((ExternalId('x'), ExternalId('y')))
        self.assert_X((ExternalId('x'), String('y')))
        # quantity
        self.assert_U((Quantity(0), Quantity(0)))
        self.assert_U((Quantity(0, Item('x')), Quantity(0, Item('x'))))
        self.assert_U((Quantity(0, 'x', -1), Quantity(0, 'x', -1)))
        self.assert_U((Quantity(0, 'x', -1, 1), Quantity(0, 'x', -1, 1)))
        self.assert_X((Quantity(0), Quantity(1)))
        self.assert_X((Quantity(0, Item('x')), Quantity(0)))
        self.assert_X((Quantity(0, 'x'), Quantity(0, 'y')))
        self.assert_X((Quantity(0, None, -1), Quantity(0)))
        self.assert_X((Quantity(0, None, -1), Quantity(0, None, -2)))
        self.assert_X((Quantity(0, None, None, 1), Quantity(0)))
        self.assert_X((Quantity(0, None, None, 1), Quantity(0, None, None, 2)))
        # time
        self.assert_U((Time('2024-09-03'), Time('2024-09-03')))
        self.assert_U((Time('2024-09-03', 0), Time('2024-09-03', 0)))
        self.assert_U((Time('2024-09-03', 0, 0), Time('2024-09-03', 0, 0)))
        self.assert_U((
            Time('2024-09-03', 0, 0, Item('x')),
            Time('2024-09-03', 0, 0, Item('x'))))
        self.assert_X((Time('2024-09-03'), Time('2024-09-02')))
        self.assert_X((Time('2024-09-03', 0), Time('2024-09-03')))
        self.assert_X((Time('2024-09-03', 0), Time('2024-09-03', 1)))
        self.assert_X((Time('2024-09-03', 0, 0), Time('2024-09-03', 0)))
        self.assert_X((Time('2024-09-03', 0, 0), Time('2024-09-03', 0, 1)))
        self.assert_X(
            (Time('2024-09-03', 0, 0, 'x'), Time('2024-09-03', 0, 0)))
        self.assert_X(
            (Time('2024-09-03', 0, 0, 'x'), Time('2024-09-03', 0, 0, 'y')))
        # value snak
        self.assert_U(
            (ValueSnak('x', 'y'), ValueSnak(Property('x'), String('y'))))
        self.assert_U(
            (ValueSnak(Property('x', Quantity), 0),
             ValueSnak('x', Quantity(0))))
        self.assert_X(
            (ValueSnak('x', 'y'), ValueSnak(Property('x', ExternalId), 'x')))
        self.assert_X((ValueSnak('x', 'y'), ValueSnak('y', 'x')))
        self.assert_X((ValueSnak('x', 'y'), Item('x')))
        self.assert_X((ValueSnak('x', 'y'), SomeValueSnak('x')))
        self.assert_X((ValueSnak('x', 'y'), NoValueSnak('x')))
        # some value snak
        self.assert_U((SomeValueSnak('x'), SomeValueSnak('x')))
        self.assert_U((SomeValueSnak('x'), SomeValueSnak(Property('x'))))
        self.assert_X((SomeValueSnak('x'), SomeValueSnak('y')))
        self.assert_X(
            (SomeValueSnak('x'), SomeValueSnak(Property('x', ExternalId))))
        self.assert_X((SomeValueSnak('x'), Item('x')))
        self.assert_X((SomeValueSnak('x'), ValueSnak('x', 'y')))
        self.assert_X((SomeValueSnak('x'), NoValueSnak('x')))
        # no value snak
        self.assert_U((NoValueSnak('x'), NoValueSnak('x')))
        self.assert_U((NoValueSnak('x'), NoValueSnak(Property('x'))))
        self.assert_X((NoValueSnak('x'), NoValueSnak('y')))
        self.assert_X(
            (NoValueSnak('x'), NoValueSnak(Property('x', ExternalId))))
        self.assert_X((NoValueSnak('x'), Item('x')))
        self.assert_X((NoValueSnak('x'), ValueSnak('x', 'y')))
        self.assert_X((NoValueSnak('x'), SomeValueSnak('x')))
        # statement
        self.assert_U(
            (Statement(Item('x'), Property('y')('z')),
             Property('y')(Item('x'), 'z')))
        self.assert_U(
            (Statement(Item('x'), Property('y', ExternalId)('z')),
             Property('y')(Item('x'), ExternalId('z'))))
        self.assert_U(
            (Statement(Property('x'), NoValueSnak('y')),
             Statement(Property('x'), NoValueSnak(Property('y')))))
        self.assert_X(
            (Property('x')(Item('y'), 0), Property('x')(Item('z'), 0)))
        self.assert_X(
            (Property('x')(Item('y'), 0), Property('y')(Item('x'), 0)))
        self.assert_X(
            (Property('x')(Item('y'), 0), Property('x')(Item('y'), 1)))
        self.assert_X((Property('x')(Item('y'), 0), Item('y')))
        self.assert_X((Property('x')(Item('y'), 0), ValueSnak('x', 'y')))

    def test_unify_tpl_tpl(self) -> None:
        x, y, z, w = Variables('x', 'y', 'z', 'w')
        x1, y1, z1, w1 = Variables('x1', 'y1', 'z1', 'w1')
        # item
        self.assert_U((ItemTemplate(x), ItemTemplate(y)))
        self.assert_U((ItemTemplate(x), ItemTemplate(IRI(y))))
        self.assert_X((ItemTemplate(x), LexemeTemplate(x)))
        # property
        self.assert_U((PropertyTemplate(x), PropertyTemplate(y)))
        self.assert_U((PropertyTemplate(x, y), PropertyTemplate(z)))
        self.assert_U((PropertyTemplate(x, y), PropertyTemplate(y, z)))
        self.assert_U((PropertyTemplate(x, y), PropertyTemplate(x, Item)))
        self.assert_X(
            (PropertyTemplate(x, Property), PropertyTemplate(y, Item)))
        self.assert_X((PropertyTemplate(x), ItemTemplate(x)))
        # lexeme
        self.assert_U((LexemeTemplate(x), LexemeTemplate(y)))
        self.assert_U((LexemeTemplate(x), LexemeTemplate(IRI(y))))
        self.assert_X((LexemeTemplate(x), ItemTemplate(x)))
        # iri
        self.assert_U((IRI_Template(x), IRI_Template(y)))
        self.assert_X((IRI_Template(x), StringTemplate(y)))
        # text
        self.assert_U((TextTemplate(x), TextTemplate(y)))
        self.assert_U((TextTemplate(x, y), TextTemplate(y, z)))
        self.assert_U((TextTemplate(y, y), TextTemplate(y, z)))
        self.assert_U((TextTemplate('x', y), TextTemplate(y, 'x')))
        self.assert_X((TextTemplate('x', y), TextTemplate(y, 'z')))
        self.assert_X((TextTemplate('x', y), TextTemplate('z', y)))
        self.assert_X((TextTemplate(x), ItemTemplate(x)))
        # string
        self.assert_U((StringTemplate(x), StringTemplate(y)))
        self.assert_X((StringTemplate(x), ExternalIdTemplate(y)))
        # external id
        self.assert_U((ExternalIdTemplate(x), ExternalIdTemplate(y)))
        self.assert_X((ExternalIdTemplate(x), StringTemplate(y)))
        # quantity
        self.assert_U((QuantityTemplate(x), QuantityTemplate(y)))
        self.assert_U((QuantityTemplate(0), QuantityTemplate(y)))
        self.assert_U((QuantityTemplate(x, y), QuantityTemplate(y, x)))
        self.assert_U((QuantityTemplate(x, 'y'), QuantityTemplate(x, y)))
        self.assert_U((QuantityTemplate(x, None), QuantityTemplate(x, y)))
        self.assert_U(
            (QuantityTemplate(x, y, z, w), QuantityTemplate(y, z, x, w)))
        self.assert_U(
            (QuantityTemplate(x, y, None, w), QuantityTemplate(x, y, w, w)))
        self.assert_U(
            (QuantityTemplate(x, y, z, 8.), QuantityTemplate(x, None, x, z)))
        self.assert_U(
            (QuantityTemplate(x, 'y'), QuantityTemplate(x, Item(y))))
        self.assert_U(
            (QuantityTemplate(x, 'y', None, None),
             QuantityTemplate(x, Item(y), z, w)))
        self.assert_X(
            (QuantityTemplate(x, 'y'), QuantityTemplate(x, None)))
        self.assert_X(
            (QuantityTemplate(x, 'y'), QuantityTemplate(x, Item('z'))))
        self.assert_X(
            (QuantityTemplate(x, None, y, z), QuantityTemplate(y, 'x', z, x)))
        self.assert_X(
            (QuantityTemplate(x, None, 8, 9), QuantityTemplate(y, 'x', z, 8)))
        self.assert_X(
            (QuantityTemplate(x, None, x, x), QuantityTemplate(y, None, 8, 9)))
        # time
        self.assert_U((TimeTemplate(x), TimeTemplate(y)))
        self.assert_U((TimeTemplate('2024-09-04'), TimeTemplate(y)))
        self.assert_U((TimeTemplate(x, y), TimeTemplate(y, x)))
        self.assert_U((TimeTemplate(x, 0), TimeTemplate(x, y)))
        self.assert_U((TimeTemplate(x, None), TimeTemplate(x, y)))
        self.assert_U(
            (TimeTemplate(x, y, z, w), TimeTemplate(y, z, x, w)))
        self.assert_U(
            (TimeTemplate(x, y, None, w), TimeTemplate(x, y, z, w)))
        self.assert_U(
            (TimeTemplate(x, y, z, 'x'), TimeTemplate(x, None, z, w)))
        self.assert_U(
            (TimeTemplate(x, None, None, 'y'),
             TimeTemplate(x, None, None, Item(y))))
        self.assert_U(
            (TimeTemplate(x, 1, None, None),
             TimeTemplate(x, 1, z, w)))
        self.assert_X((TimeTemplate(x, 0), TimeTemplate(x, None)))
        self.assert_X(
            (TimeTemplate(x, 0), TimeTemplate(x, 1)))
        self.assert_X(
            (TimeTemplate(x, None, y, z), TimeTemplate(y, 0, z, x)))
        self.assert_X(
            (TimeTemplate(x, 1, 2, None), TimeTemplate(y, z, z, None)))
        # value snak
        self.assert_U((ValueSnak(x, y), ValueSnak(x, y)))
        self.assert_U((ValueSnak(x, y), ValueSnak(y, x)))
        self.assert_U((ValueSnak(x, y@Entity), ValueSnak(x, y@Lexeme)))
        self.assert_U((ValueSnak(x, y@Value), ValueSnak(x, Item('x'))))
        self.assert_U((
            ValueSnak(Property('x'), y), ValueSnak(x, Property('x'))))
        self.assert_U(
            (ValueSnak(Property('x'), x), ValueSnak(x, Property('x'))))
        self.assert_U((ValueSnak(Property(x), y), ValueSnak(Property(y), x)))
        self.assert_U(
            (ValueSnak(Property(x, y), z), ValueSnak(Property(x1, y1), z1)))
        self.assert_U(
            (ValueSnak(Property(x, y), z), ValueSnak(x1, Property(x, y))))
        self.assert_U(
            (ValueSnak(Property(x, y), Property(z, y)),
             ValueSnak(Property(x, y), Property(z, Property))))
        self.assert_U((ValueSnak(x, Quantity(0, 'x')), ValueSnak(x, y)))
        self.assert_U(
            (ValueSnak(x, Quantity(0, 'x')), ValueSnak(x, Quantity(0, y))))
        self.assert_U(
            (ValueSnak(x, Quantity(y, 'x', 0)),
             ValueSnak(x, Quantity(0, z, y))))
        self.assert_X((ValueSnak(Property(x), y), ValueSnak(y, x)))
        self.assert_X((ValueSnak(x, y@Item), ValueSnak(x, y@Quantity)))
        # some value snak
        self.assert_U((SomeValueSnak(x), SomeValueSnak(y)))
        self.assert_U(
            (SomeValueSnak(Property(x, y)),
             SomeValueSnak(Property(x, Item))))
        self.assert_X(
            (SomeValueSnak(Property(x, Quantity)),
             SomeValueSnak(Property(x, Item))))
        # no value snak
        self.assert_U((NoValueSnak(x), NoValueSnak(y)))
        self.assert_U(
            (NoValueSnak(Property(x, y)),
             NoValueSnak(Property(x, Item))))
        self.assert_X(
            (NoValueSnak(Property(x, Quantity)),
             NoValueSnak(Property(x, Item))))
        # statement
        self.assert_U((Statement(x, y), Statement(x, y)))
        self.assert_U((Statement(x, y), Statement(y, x)))
        self.assert_U((Statement(x, ValueSnak(y, z)), Statement(z, x)))
        self.assert_U(
            (Statement(x, ValueSnak(Property(y, z), w)),
             Statement(x1, ValueSnak(Property(y1, z1), w1))))
        self.assert_U(
            (Statement(x, ValueSnak(Property(y, z), Quantity(0, x))),
             Statement(x1, ValueSnak(Property(y1, z1), Quantity(0, 'x', w1)))))
        self.assert_X(
            (Statement(x, ValueSnak(Property(y, z), Quantity(0, 'y'))),
             Statement(x1, ValueSnak(Property(y1, z1), Quantity(0, 'x')))))
        self.assert_X(
            (Statement(x, ValueSnak(y, Quantity(z))),
             Statement(z, SomeValueSnak(x))))

    def test_unify_var_term(self) -> None:
        for tv in self.ALL_VARIABLE_CLASSES:
            # datatype
            self._test_unify_var_term(
                tv, DatatypeVariable, ItemDatatype(),
                ExternalIdDatatype(), StringDatatype())
            # item
            self._test_unify_var_term(tv, ItemVariable, Item('x'))
            # property
            self._test_unify_var_term(
                tv, PropertyVariable, Property('x'), Property('x', Item))
            # lexeme
            self._test_unify_var_term(tv, LexemeVariable, Lexeme('x'))
            # iri
            self._test_unify_var_term(tv, IRI_Variable, IRI('x'))
            # text
            self._test_unify_var_term(
                tv, TextVariable, Text('x'), Text('x', 'y'))
            # string
            self._test_unify_var_term(tv, StringVariable, String('x'))
            # external id
            self._test_unify_var_term(
                tv, ExternalIdVariable, ExternalId('x'))
            # quantity
            self._test_unify_var_term(
                tv, QuantityVariable, Quantity(0),
                Quantity(0, 'x'),
                Quantity(0, 'x', -1),
                Quantity(0, 'x', -1, 1))
            # time
            self._test_unify_var_term(
                tv, TimeVariable,
                Time('2024-09-04'),
                Time('2024-09-04', 0),
                Time('2024-09-04', 0, 0),
                Time('2024-09-04', 0, 0, 'x'))
            # value snak
            self._test_unify_var_term(
                tv, ValueSnakVariable, ValueSnak('x', 'y'))
            # some value snak
            self._test_unify_var_term(
                tv, SomeValueSnakVariable, SomeValueSnak('x'))
            # no value snak
            self._test_unify_var_term(
                tv, NoValueSnakVariable, NoValueSnak('x'))
            # statement
            self._test_unify_var_term(
                tv, StatementVariable,
                Statement(Item('x'), ValueSnak('y', 'z')),
                Statement(Item('x'), SomeValueSnak('y')),
                Statement(Item('x'), NoValueSnak('y')))

    def _test_unify_var_term(
            self,
            tv: type[Variable],
            variable_class: type[Variable],
            *terms: Term
    ) -> None:
        for term in terms:
            if issubclass(variable_class, tv):
                self.assert_U((Variable('x', tv), term))
            elif issubclass(tv, variable_class):
                self.assert_U((Variable('x', variable_class), term))
            else:
                self.assert_X((Variable('x', tv), term))

    def test_unify_var_tpl(self) -> None:
        x, y = Variables('a', 'b')
        for tv in self.ALL_VARIABLE_CLASSES:
            # item
            self._test_unify_var_term(
                tv, ItemVariable, ItemTemplate(x))
            # property
            self._test_unify_var_term(
                tv, PropertyVariable,
                PropertyTemplate(x),
                PropertyTemplate(x, Item),
                PropertyTemplate('x', y),
                PropertyTemplate('x', y))
            # lexeme
            self._test_unify_var_term(
                tv, LexemeVariable, LexemeTemplate(x))
            # iri
            self._test_unify_var_term(tv, IRI_Variable, IRI_Template(x))
            # text
            self._test_unify_var_term(
                tv, TextVariable,
                TextTemplate(x),
                TextTemplate(x, 'y'),
                TextTemplate('x', y),
                TextTemplate(x, y))
            # string
            self._test_unify_var_term(
                tv, StringVariable, StringTemplate(x))
            # external id
            self._test_unify_var_term(
                tv, ExternalIdVariable, ExternalIdTemplate(x))
            # quantity
            self._test_unify_var_term(
                tv, QuantityVariable,
                QuantityTemplate(x),
                QuantityTemplate(0, x),
                QuantityTemplate(0, Item('x'), x),
                QuantityTemplate(0, Item('x'), 0, x))
            # time
            self._test_unify_var_term(
                tv, TimeVariable,
                TimeTemplate(x),
                TimeTemplate('2024-09-04', x),
                TimeTemplate('2024-09-04', 0, x),
                TimeTemplate('2024-09-04', 0, 0, x))
            # value snak
            self._test_unify_var_term(
                tv, ValueSnakVariable,
                ValueSnak(x, 'y'),
                ValueSnak('x', y),
                ValueSnak(PropertyTemplate(x), y),
                ValueSnak(PropertyTemplate(x), ItemTemplate(y)))
            # some value snak
            self._test_unify_var_term(
                tv, SomeValueSnakVariable,
                SomeValueSnakTemplate(x),
                SomeValueSnakTemplate(PropertyTemplate(x)),
                SomeValueSnakTemplate(PropertyTemplate(IRI_Template(x))))
            # no value snak
            self._test_unify_var_term(
                tv, NoValueSnakVariable,
                NoValueSnakTemplate(x),
                NoValueSnakTemplate(PropertyTemplate(x)),
                NoValueSnakTemplate(PropertyTemplate(IRI_Template(x))))
            # statement
            self._test_unify_var_term(
                tv, StatementVariable,
                StatementTemplate(x, ValueSnak('y', 'z')),
                StatementTemplate(ItemTemplate(x), NoValueSnak('y')),
                StatementTemplate(Property('x'), SomeValueSnak(Property(x))))
        # multiple equations
        self.assert_U(
            (ItemVariable('x'), ItemTemplate(IRI_Variable('y'))),
            (IRI_Variable('y'), IRI_Template(StringVariable('z'))))
        self.assert_U(
            (ItemVariable('x'), ItemTemplate(IRI_Variable('x'))),
            (IRI_Variable('x'), IRI_Template(StringVariable('x'))))
        self.assert_U(
            (StringVariable('x'), StringVariable('y')),
            (IRI_Variable('z'), IRI_Template(StringVariable('x'))))
        # bad instantiations
        self.assert_X(
            (StringVariable('x'), String(StringVariable('y'))),
            (IRI_Variable('z'), IRI_Template(StringVariable('x'))))
        # occur-check violations
        self.assert_X(
            (StringVariable('x'), StringTemplate(StringVariable('x'))))

    def test_unify_var_var(self) -> None:
        x, y = Variables('x', 'y')
        self.assert_U((x, x))
        self.assert_U((x, y))
        for tu, tv in itertools.permutations(self.ALL_VARIABLE_CLASSES, 2):
            if issubclass(tu, tv) or issubclass(tv, tu):
                self.assert_U((x@tu, y@tv))
            else:
                self.assert_X((x@tu, y@tv))


if __name__ == '__main__':
    Test.main()
