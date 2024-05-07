# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    DeepDataValue,
    Entity,
    ExternalId,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    ShallowDataValue,
    Snak,
    SomeValueSnak,
    Statement,
    String,
    Text,
    Time,
    Value,
    ValueSnak,
    Variable,
    Variables,
)
from kif_lib.model import (
    DataValueVariable,
    EntityVariable,
    ItemVariable,
    PropertyVariable,
    StringVariable,
    ValueVariable,
)

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test__check_arg_variable_class(self):
        self.assertRaises(
            TypeError, Variable._check_arg_variable_class, 0)
        self.assertRaises(
            TypeError, Variable._check_arg_variable_class, int)
        self.assertRaises(
            ValueError, Variable._check_arg_variable_class, KIF_Object)
        self.assertIs(
            Variable._check_arg_variable_class(Variable), Variable)
        self.assertIs(
            Variable._check_arg_variable_class(ItemVariable), ItemVariable)
        self.assertIs(
            Variable._check_arg_variable_class(Item), ItemVariable)

    def test__check_optional_arg_variable_class(self):
        self.assertRaises(
            TypeError, Variable._check_optional_arg_variable_class, 0)
        self.assertIsNone(
            Variable._check_optional_arg_variable_class(None))
        self.assertIs(
            Variable._check_optional_arg_variable_class(None, Variable),
            Variable)
        self.assertIs(
            Variable._check_optional_arg_variable_class(
                Item, PropertyVariable), ItemVariable)

    def test__preprocess_arg_variable_class(self):
        self.assertRaises(
            TypeError, Variable._preprocess_arg_variable_class, 0, 1)
        self.assertRaises(
            TypeError, Variable._preprocess_arg_variable_class, int, 1)
        self.assertIs(
            Variable._preprocess_arg_variable_class(ItemVariable, 1),
            ItemVariable)
        self.assertIs(
            Variable._preprocess_arg_variable_class(Item, 1),
            ItemVariable)

    def test__preprocess_optional_arg_variable_class(self):
        self.assertRaises(
            TypeError,
            Variable._preprocess_optional_arg_variable_class, 0, 1)
        self.assertRaises(
            TypeError,
            Variable._preprocess_optional_arg_variable_class, int, 1)
        self.assertIsNone(
            Variable._preprocess_optional_arg_variable_class(None, 1))
        self.assertEqual(
            Variable._preprocess_optional_arg_variable_class(
                None, 1, ItemVariable), ItemVariable)
        self.assertEqual(
            Variable._preprocess_optional_arg_variable_class(
                Item, 1, PropertyVariable), ItemVariable)

    def test__preprocess_arg_variable(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce PropertyVariable 'x' into ItemVariable",
            (ItemVariable._preprocess_arg_variable, 'ItemVariable'),
            PropertyVariable('x'), 1)
        self.assertEqual(
            Variable._preprocess_arg_variable(Variable('x'), 1),
            Variable('x'))
        self.assertEqual(
            ItemVariable._preprocess_arg_variable(Variable('x'), 1),
            ItemVariable('x'))
        self.assertEqual(
            Variable._preprocess_arg_variable(ItemVariable('x'), 1),
            ItemVariable('x'))

    def test__new__(self):
        self.assert_raises_bad_argument(
            TypeError, 2, 'variable_class',
            'expected type, got int', Variable, 'x', 0)
        self.assert_raises_bad_argument(
            TypeError, 2, 'variable_class',
            'expected subclass of KIF_Object, got int', Variable, 'x', int)
        self.assert_raises_bad_argument(
            ValueError, 2, 'variable_class',
            'no variable class for KIF_Object', Variable, 'x', KIF_Object)
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

    def test__init__(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int', Variable, 0)
        self.assert_variable(Variable('x'), 'x')

    def test__call__(self):
        self.assertRaises(ValueError, ItemVariable('p'), String('s'))
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

    def test_coerce(self):
        self.assert_raises_bad_argument(
            TypeError, 1, 'variable_class', 'expected type, got int',
            Variable('x').coerce, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, 'variable_class',
            'expected subclass of KIF_Object, got int',
            Variable('x').coerce, int)
        self.assert_raises_bad_argument(
            ValueError, 1, 'variable_class',
            'no variable class for KIF_Object',
            Variable('x').coerce, KIF_Object)
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, 'variable_class',
            "cannot coerce ItemVariable 'x' into PropertyVariable",
            (ItemVariable('x').coerce, 'Variable.coerce'),
            Property)
        self.assertEqual(Variable('x').coerce(Item), ItemVariable('x'))
        self.assertEqual(EntityVariable('x').coerce(Item), ItemVariable('x'))
        self.assertEqual(ItemVariable('x').coerce(Entity), ItemVariable('x'))

    def test_instantiate(self):
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

    def test_variables(self):
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


if __name__ == '__main__':
    Test.main()
