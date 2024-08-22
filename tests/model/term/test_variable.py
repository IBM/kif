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
    StatementTemplate,
    String,
    Term,
    Text,
    Time,
    Value,
    ValueSnak,
    ValueSnakTemplate,
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
from kif_lib.typing import assert_type, Iterator, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test__init__(self) -> None:
        assert_type(Variable('x'), Variable)
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

    def test_get_variables(self) -> None:
        assert_type(ItemVariable('x').variables, Set[Variable])
        assert_type(Variable('x').get_variables(), Set[Variable])
        self.assertEqual(
            ItemVariable('x').get_variables(), {ItemVariable('x')})
        self.assertEqual(Variable('y').variables, {Variable('y')})

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


if __name__ == '__main__':
    Test.main()
