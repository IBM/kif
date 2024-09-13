# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DataValue,
    DataValueVariable,
    DeepDataValue,
    Entity,
    EntityVariable,
    ExternalId,
    ExternalIdVariable,
    IRI,
    Item,
    ItemVariable,
    KIF_Object,
    Lexeme,
    NoValueSnak,
    Property,
    PropertyVariable,
    Quantity,
    QuantityVariable,
    ShallowDataValue,
    Snak,
    SnakVariable,
    SomeValueSnak,
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    StringVariable,
    Term,
    Text,
    Time,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    ValueVariable,
    Variable,
    Variables,
)
from kif_lib.typing import assert_type, Iterator, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test__init__(self) -> None:
        assert_type(Variable('x'), Variable)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into String', Variable, {})
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce Item into String', Variable, Item)
        self.assert_raises_bad_argument(
            TypeError, 2, 'variable_class',
            'cannot coerce int into Variable', Variable, 'x', 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'variable_class',
            'cannot coerce int into Variable', Variable, 'x', int)
        self.assert_raises_bad_argument(
            TypeError, 2, 'variable_class',
            'cannot coerce KIF_Object into Variable',
            Variable, 'x', KIF_Object)
        self.assert_variable(Variable('x'), 'x')
        self.assert_variable(Variable('x', Variable), 'x')
        self.assert_value_variable(Variable('x', Value), 'x')
        self.assert_entity_variable(Variable('x', Entity), 'x')
        self.assert_item_variable(Variable('x', Item), 'x')
        self.assert_property_variable(Variable('x', Property), 'x')
        self.assert_lexeme_variable(Variable('x', Lexeme), 'x')
        self.assert_data_value_variable(Variable('x', DataValue), 'x')
        self.assert_shallow_data_value_variable(
            Variable('x', ShallowDataValue), 'x')
        self.assert_iri_variable(Variable('x', IRI), 'x')
        self.assert_text_variable(Variable('x', Text), 'x')
        self.assert_string_variable(Variable('x', String), 'x')
        self.assert_external_id_variable(Variable('x', ExternalId), 'x')
        self.assert_deep_data_value_variable(
            Variable('x', DeepDataValue), 'x')
        self.assert_quantity_variable(Variable('x', Quantity), 'x')
        self.assert_time_variable(Variable('x', Time), 'x')
        self.assert_snak_variable(Variable('x', Snak), 'x')
        self.assert_value_snak_variable(Variable('x', ValueSnak), 'x')
        self.assert_some_value_snak_variable(
            Variable('x', SomeValueSnak), 'x')
        self.assert_no_value_snak_variable(Variable('x', NoValueSnak), 'x')
        self.assert_statement_variable(Variable('x', Statement), 'x')
        # fresh vars
        assert_type(Variable(), Variable)
        x, y, z = Variable(), Variable(), Variable()
        self.assert_variable(x, x.name)
        self.assert_variable(y, y.name)
        self.assert_variable(z, z.name)
        self.assertIs(type(x), Variable)
        self.assertIs(type(y), Variable)
        self.assertIs(type(z), Variable)
        self.assertNotEqual(x, y)
        self.assertNotEqual(y, z)
        self.assertNotEqual(x, z)
        xi = Variable(None, Item)
        yp = Variable(None, Property)
        zq = Variable(None, Quantity)
        self.assert_item_variable(xi, xi.name)
        self.assert_property_variable(yp, yp.name)
        self.assert_quantity_variable(zq, zq.name)
        self.assertNotEqual(xi, yp)
        self.assertNotEqual(xi.name, yp.name)
        self.assertNotEqual(yp, zq)
        self.assertNotEqual(yp.name, zq.name)

    def test__call__(self) -> None:
        assert_type(Variable('p')('x'), ValueSnakTemplate)
        assert_type(Variable('p')(Item('x'), 'y'), StatementTemplate)
        self.assertRaises(TypeError, ItemVariable('p'), String('s'))
        self.assertEqual(
            PropertyVariable('p')(String('s')),
            ValueSnak(PropertyVariable('p'), String('s')))
        self.assertEqual(
            EntityVariable('p')(String('s')),
            ValueSnak(PropertyVariable('p'), String('s')))
        self.assertEqual(
            PropertyVariable('p')(Item('x'), String('s')),
            Statement(Item('x'), ValueSnak(
                PropertyVariable('p'), String('s'))))
        self.assertEqual(
            ValueVariable('p')(Item('x'), String('s')),
            Statement(Item('x'), ValueSnak(
                PropertyVariable('p'), String('s'))))

    def test__matmul__(self) -> None:
        assert_type(Variable()@Variable, Variable)
        x, y = Variable('x'), ItemVariable('y')
        self.assert_raises_bad_argument(
            TypeError, 1, 'variable_class',
            'cannot coerce ItemVariable into StatementVariable',
            (y.__matmul__, 'Variable.coerce'), StatementVariable)
        self.assert_variable(x, 'x')
        self.assert_variable(x@Variable, 'x')
        self.assert_item_variable(x@Item, 'x')
        self.assert_quantity_variable(x@QuantityVariable, 'x')
        self.assert_entity_variable(y@Entity, 'y')

    def test_get_variables(self) -> None:
        assert_type(ItemVariable('x').variables, Set[Variable])
        assert_type(Variable('x').get_variables(), Set[Variable])
        self.assertEqual(
            ItemVariable('x').get_variables(), {ItemVariable('x')})
        self.assertEqual(Variable('y').variables, {Variable('y')})

    def test_coerce(self) -> None:
        assert_type(Variable('x').coerce(), Variable)
        assert_type(ItemVariable('x').coerce(), ItemVariable)
        self.assert_raises_bad_argument(
            TypeError, 1, 'variable_class',
            'cannot coerce KIF_Object into Variable',
            ItemVariable('x').coerce, KIF_Object)
        self.assert_raises_bad_argument(
            TypeError, 1, 'variable_class',
            'cannot coerce SnakVariable into ItemVariable',
            SnakVariable('x').coerce, ItemVariable)
        self.assert_raises_bad_argument(
            TypeError, 1, 'variable_class',
            'cannot coerce DataValueVariable into ItemVariable',
            DataValueVariable('x').coerce, ItemVariable)
        self.assertEqual(
            Variable('x').coerce(ItemVariable),
            ItemVariable('x'))
        self.assertEqual(
            Variable('x').coerce(Item),
            ItemVariable('x'))
        self.assertEqual(
            ItemVariable('x').coerce(EntityVariable),
            ItemVariable('x'))
        self.assertEqual(
            ItemVariable('x').coerce(Entity),
            ItemVariable('x'))
        self.assertEqual(
            EntityVariable('x').coerce(ItemVariable),
            ItemVariable('x'))
        self.assertEqual(
            EntityVariable('x').coerce(Item),
            ItemVariable('x'))
        self.assertEqual(
            StringVariable('x').coerce(ExternalId),
            ExternalIdVariable('x'))
        self.assertEqual(
            ExternalIdVariable('x').coerce(StringVariable),
            ExternalIdVariable('x'))
        self.assertEqual(
            DataValueVariable('x').coerce(StringVariable),
            StringVariable('x'))
        self.assertEqual(
            StringVariable('x').coerce(DataValueVariable),
            StringVariable('x'))

    def test_instantiate(self) -> None:
        assert_type(Variable('x').instantiate({}), Optional[Term])
        self.assert_raises_bad_argument(
            TypeError, 1, 'theta', 'expected Mapping, got int',
            Variable('x').instantiate, 0)
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate ItemVariable 'x' with String",
            EntityVariable('x').instantiate,
            {ItemVariable('x'): String('x')})
        self.assertIsNone(Variable('x').instantiate({Variable('x'): None}))
        self.assertEqual(
            Variable('x').instantiate({Variable('x'): ItemVariable('x')}),
            ItemVariable('x'))
        self.assertEqual(
            Variable('x').instantiate({Variable('x'): Item('x')}),
            Item('x'))
        self.assertEqual(
            Variable('x').instantiate({Variable('x'): Item(Variable('x'))}),
            Item(Variable('x')))
        self.assertEqual(
            Variable('x').instantiate({Variable('y'): Item('x')}),
            Variable('x'))
        self.assertIsNone(
            ItemVariable('x').instantiate({ItemVariable('x'): None}))
        self.assertEqual(
            EntityVariable('x').instantiate(
                {EntityVariable('x'): ItemVariable('x')}),
            ItemVariable('x'))
        self.assertEqual(
            ItemVariable('x').instantiate({Variable('x'): Item('x')}),
            ItemVariable('x'))
        self.assertEqual(
            EntityVariable('x').instantiate({ItemVariable('x'): Item('x')}),
            Item('x'))
        self.assertEqual(
            EntityVariable('x').instantiate(
                {ItemVariable('x'): Item(Variable('x'))}),
            Item(Variable('x')))
        self.assertEqual(
            Variable('x').instantiate({EntityVariable('x'): Item('x')}),
            Item('x'))
        self.assertEqual(
            DataValueVariable('x').instantiate(
                {StringVariable('x'): ExternalId('x')}), ExternalId('x'))
        self.assertEqual(
            ItemVariable('x').instantiate(
                {PropertyVariable('x'): Property('x')}), ItemVariable('x'))
        self.assertEqual(
            DataValueVariable('x').instantiate(
                {StringVariable('x'): ExternalId('x')}, False),
            DataValueVariable('x'))

    def test_Variables(self) -> None:
        assert_type(Variables('x', 'y', 'z'), Iterator[Variable])
        a, b, c, d, e = Variables(
            'a', 'b', Item,
            'c', DataValueVariable,
            'd', String,
            'e')
        self.assert_item_variable(a, 'a')
        self.assert_item_variable(b, 'b')
        self.assert_data_value_variable(c, 'c')
        self.assert_string_variable(d, 'd')
        self.assert_variable(e, 'e')
        self.assertIs(e.__class__, Variable)
        # fresh vars
        assert_type(Variables(None, None, None), Iterator[Variable])
        a, b, c = Variables(None, None, None)
        self.assert_variable(a, a.name)
        self.assert_variable(b, b.name)
        self.assert_variable(c, c.name)
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, c)
        self.assertNotEqual(a, c)
        d, x, f, g = Variables(None, Item, Property, 'x', None, Lexeme, None)
        self.assert_item_variable(d, d.name)
        self.assert_lexeme_variable(x, 'x')
        self.assert_lexeme_variable(f, f.name)
        self.assert_variable(g, g.name)
        self.assertIs(type(g), Variable)
        self.assertEqual(len(set(map(Variable.get_name, [d, x, f, g]))), 4)


if __name__ == '__main__':
    Test.main()
