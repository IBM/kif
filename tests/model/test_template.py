# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    DeepDataValue,
    Entity,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    Snak,
    SomeValueSnak,
    Statement,
    String,
    Time,
    Value,
    ValueSnak,
    Variable,
    Variables,
)
from kif_lib.model import (
    DataValueTemplate,
    Decimal,
    DeepDataValueTemplate,
    EntityTemplate,
    IRI_Template,
    IRI_Variable,
    ItemTemplate,
    ItemVariable,
    LexemeTemplate,
    NoValueSnakTemplate,
    PropertyTemplate,
    PropertyVariable,
    QuantityTemplate,
    QuantityVariable,
    SnakTemplate,
    SomeValueSnakTemplate,
    StatementTemplate,
    StringVariable,
    Template,
    TimeTemplate,
    TimeVariable,
    ValueSnakTemplate,
    ValueTemplate,
    ValueVariable,
)
from kif_lib.typing import cast

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test__check_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._check_arg_template_class, 0)
        self.assertRaises(
            ValueError, Template._check_arg_template_class, int)
        self.assertRaises(
            ValueError, Template._check_arg_template_class, KIF_Object)
        self.assertIs(
            Template._check_arg_template_class(Template), Template)
        self.assertIs(
            Template._check_arg_template_class(ItemTemplate), ItemTemplate)
        self.assertIs(
            Template._check_arg_template_class(Item), ItemTemplate)

    def test__check_optional_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._check_optional_arg_template_class, 0)
        self.assertIsNone(
            Template._check_optional_arg_template_class(None))
        self.assertIs(
            Template._check_optional_arg_template_class(None, Template),
            Template)
        self.assertIs(
            Template._check_optional_arg_template_class(
                Item, PropertyTemplate), ItemTemplate)

# -- __new__ ---------------------------------------------------------------

    def test__new__template(self):
        self.assert_abstract_class(Template)

    def test__new__value_template(self):
        self.assert_abstract_class(ValueTemplate)

    def test__new__entity_template(self):
        self.assert_abstract_class(EntityTemplate)

    def test__new__data_value_template(self):
        self.assert_abstract_class(DataValueTemplate)

    def test__new__deep_data_value_template(self):
        self.assert_abstract_class(DeepDataValueTemplate)

    def test__new__quantity_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            ValueError, 1, None, 'expected Decimal',
            (QuantityTemplate, 'Quantity'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce int into IRI',
            (QuantityTemplate, 'Quantity'), 0, 0)
        self.assert_raises_bad_argument(
            ValueError, 3, None, 'expected Decimal',
            (QuantityTemplate, 'Quantity'), 0, None, 'x')
        self.assert_raises_bad_argument(
            ValueError, 4, None, 'expected Decimal',
            (QuantityTemplate, 'Quantity'), 0, None, None, 'x')
        self.assert_quantity_template(
            QuantityTemplate(x),
            QuantityVariable('x'), None, None, None)
        self.assert_quantity_template(
            QuantityTemplate(0, x), Decimal(0),
            ItemVariable('x'), None, None)
        self.assert_quantity_template(
            QuantityTemplate(0, None, x),
            Decimal(0), None, QuantityVariable('x'), None)
        self.assert_quantity_template(
            QuantityTemplate(0, None, None, x),
            Decimal(0), None, None, QuantityVariable('x'))
        self.assert_quantity_template(
            QuantityTemplate(
                Variable('x'),
                Variable('y'),
                Variable('z'),
                Variable('w')),
            QuantityVariable('x'),
            ItemVariable('y'),
            QuantityVariable('z'),
            QuantityVariable('w'))
        self.assert_quantity_template(
            Quantity(x), Variable('x', Quantity), None, None, None)
        self.assert_quantity_template(
            Quantity(0, Item(x)), Decimal(0),
            Item(Variable('x', IRI)), None, None)
        self.assert_quantity_template(
            Quantity(0, Item(IRI(x))), Decimal(0),
            ItemTemplate(IRI(Variable('x', String))), None, None)
        self.assert_quantity_template(
            Quantity(0, None, x), Decimal(0),
            None, Variable('x', Quantity), None)
        self.assert_quantity_template(
            Quantity(0, None, 0, x),
            Decimal(0), None, Decimal(0), Variable('x', Quantity))
        self.assert_quantity(
            cast(Quantity, QuantityTemplate(0, None, 0, None)),
            Decimal(0), None, Decimal(0), None)

    def test__new__time_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            ValueError, 1, None, 'expected datetime',
            (TimeTemplate, 'Time'), 'x')
        self.assert_raises_bad_argument(
            ValueError, 2, None,
            'expected Time.Precision',
            (TimeTemplate, 'Time'), '2024-05-06', 'x')
        self.assert_raises_bad_argument(
            ValueError, 3, None,
            'expected timezone',
            (TimeTemplate, 'Time'), '2024-05-06', None, 'x')
        self.assert_raises_bad_argument(
            TypeError, 4, None, 'cannot coerce int into IRI',
            (TimeTemplate, 'Time'), '2024-05-06', None, None, 0)
        self.assert_time_template(
            TimeTemplate(x),
            TimeVariable('x'),
            None, None, None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', Variable('x')),
            Time('2024-05-06').time,
            QuantityVariable('x'), None, None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', None, Variable('x')),
            Time('2024-05-06').time,
            None, QuantityVariable('x'), None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', None, None, x),
            Time('2024-05-06').time,
            None, None, ItemVariable('x'))
        self.assert_time_template(
            TimeTemplate(
                Variable('x'),
                Variable('y'),
                Variable('z'),
                Variable('w')),
            TimeVariable('x'),
            QuantityVariable('y'),
            QuantityVariable('z'),
            ItemVariable('w'))
        self.assert_time_template(
            Time(x), Variable('x', Time), None, None, None)
        self.assert_time_template(
            Time('2024-05-06', x),
            Time('2024-05-06').time,
            Variable('x', Quantity), None, None)
        self.assert_time_template(
            Time('2024-05-06', None, x),
            Time('2024-05-06').time,
            None, Variable('x', Quantity), None)
        self.assert_time_template(
            Time('2024-05-06', None, None, x),
            Time('2024-05-06').time,
            None, None, Variable('x', Item))
        self.assert_time_template(
            Time('2024-05-06', None, None, Item(IRI(x))),
            Time('2024-05-06').time, None, None,
            Item(IRI(Variable('x'))))
        self.assert_time(
            cast(Time, TimeTemplate('2024-05-06', None, None, None)),
            Time('2024-05-06').time, None, None, None)

    def test__new__snak_template(self):
        self.assert_abstract_class(SnakTemplate)

    def test__new__value_snak_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            (ValueSnakTemplate, 'ValueSnak'), 0, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (ValueSnakTemplate, 'ValueSnak'), Property('x'), dict())
        self.assert_value_snak_template(
            ValueSnakTemplate(x, Quantity(0)),
            Variable('x', Property), Quantity(0))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property(x), Quantity(0)),
            Property(Variable('x', IRI)), Quantity(0))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property('p'), x),
            Property('p'), ValueVariable('x'))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property('p'), IRI_Template(x)),
            Property('p'), IRI(StringVariable('x')))
        self.assert_value_snak_template(
            ValueSnak(x, Quantity(0)),
            Variable('x', Property), Quantity(0))
        self.assert_value_snak_template(
            ValueSnak(Property(x), Quantity(0)),
            Property(Variable('x', IRI)), Quantity(0))
        self.assert_value_snak_template(
            ValueSnak(Property('p'), x),
            Property('p'), Variable('x', Value))
        self.assert_value_snak_template(
            cast(ValueSnakTemplate, ValueSnak(Property('p'), Time(x))),
            Property('p'), Time(Variable('x', Time)))
        self.assert_value_snak_template(
            PropertyTemplate(x)(String('s')),
            Property(x), String('s'))
        self.assert_value_snak(
            cast(ValueSnak, ValueSnakTemplate(Property('p'), Item('x'))),
            Property('p'), Item('x'))

    def test__new__some_value_snak_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            (SomeValueSnakTemplate, 'SomeValueSnak'), 0)
        self.assert_some_value_snak_template(
            SomeValueSnakTemplate(x),
            PropertyVariable('x'))
        self.assert_some_value_snak_template(
            SomeValueSnakTemplate(Property(x)),
            PropertyTemplate(IRI_Variable('x')))
        self.assert_some_value_snak_template(
            cast(SomeValueSnakTemplate, SomeValueSnak(x)),
            PropertyVariable('x'))
        self.assert_some_value_snak_template(
            SomeValueSnak(Property(x)),
            Property(Variable('x', IRI)))
        self.assert_some_value_snak(
            cast(SomeValueSnak, SomeValueSnakTemplate(Property('x'))),
            Property('x'))

    def test__new__no_value_snak_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            (NoValueSnakTemplate, 'NoValueSnak'), 0)
        self.assert_no_value_snak_template(
            NoValueSnakTemplate(x), PropertyVariable('x'))
        self.assert_no_value_snak_template(
            NoValueSnakTemplate(Property(x)),
            PropertyTemplate(IRI_Variable('x')))
        self.assert_no_value_snak_template(
            NoValueSnak(x), PropertyVariable('x'))
        self.assert_no_value_snak_template(
            NoValueSnak(Property(x)),
            Property(Variable('x', IRI)))
        self.assert_no_value_snak(
            cast(NoValueSnak, NoValueSnakTemplate(Property('x'))),
            Property('x'))

    def test__new__statement_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce int into Entity',
            (StatementTemplate, 'Statement'), 0, Property('p')(0))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce int into Snak',
            (StatementTemplate, 'Statement'), Item('x'), 0)
        self.assert_statement_template(
            StatementTemplate(x, Property('p')(0)),
            Variable('x', Entity), Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Lexeme(x), Property('p')(0)),
            LexemeTemplate(IRI_Variable('x')),
            Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Item('x'), x), Item('x'), Variable('x', Snak))
        self.assert_statement_template(
            StatementTemplate(Item('x'), NoValueSnakTemplate(x)),
            Item('x'), NoValueSnakTemplate(PropertyVariable('x')))
        self.assert_statement_template(
            Statement(Lexeme(x), Property('p')(0)),
            Lexeme(IRI_Variable('x')), Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Item('x'), x), Item('x'), Variable('x', Snak))
        self.assert_statement_template(
            StatementTemplate(Item('x'), NoValueSnak(x)),
            Item('x'), NoValueSnak(PropertyVariable('x')))
        self.assert_statement_template(
            PropertyTemplate(x)(Item('i'), String('s')),
            Item('i'), PropertyTemplate(x)(String('s')))
        self.assert_statement(
            cast(Statement, PropertyTemplate('x')(Item('i'), String('s'))),
            Item('i'), Property('x')(String('s')))

# -- __init__ --------------------------------------------------------------

    def test__init__template(self):
        self.assert_abstract_class(Template)

    def test__init__value_template(self):
        self.assert_abstract_class(ValueTemplate)

    def test__init__entity_template(self):
        self.assert_abstract_class(EntityTemplate)

    def test__init__data_value_template(self):
        self.assert_abstract_class(DataValueTemplate)

    def test__init__deep_data_value_template(self):
        self.assert_abstract_class(DeepDataValueTemplate)

    def test__init__quantity_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            QuantityTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected Decimal or float or int or str, got QuantityTemplate',
            QuantityTemplate, QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce IRI_Variable into ItemVariable",
            QuantityTemplate, 0, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            QuantityTemplate, 0, None, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'expected Decimal or float or int or str, got QuantityTemplate',
            QuantityTemplate, 0, None, QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            QuantityTemplate, 0, None, None, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            'expected Decimal or float or int or str, got QuantityTemplate',
            QuantityTemplate, 0, None, None, QuantityTemplate(Variable('x')))

    def test__init__quantity_template_normalization(self):
        x = Variable('x')
        self.assertRaises(TypeError, QuantityTemplate, x, x)
        self.assertRaises(TypeError, Quantity, 0, x, x)
        self.assertRaises(
            TypeError, QuantityTemplate, 0, x, None, x)
        self.assert_quantity_template(
            QuantityTemplate(x, None, x),
            QuantityVariable('x'), None, QuantityVariable('x'), None)
        self.assert_quantity_template(
            QuantityTemplate(x, None, x, Variable('x', DeepDataValue)),
            QuantityVariable('x'), None,
            QuantityVariable('x'), QuantityVariable('x'))
        self.assert_quantity_template(
            QuantityTemplate(
                x, None, Variable('x', DataValue),
                Variable('x', DeepDataValue)),
            QuantityVariable('x'), None,
            QuantityVariable('x'), QuantityVariable('x'))

    def test__init__time_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into TimeVariable",
            TimeTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected datetime or str, got TimeTemplate',
            TimeTemplate, TimeTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            TimeTemplate, '2024-05-06', IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected Decimal or Quantity or Time.Precision or '
            'float or int or str, got QuantityTemplate',
            TimeTemplate, Variable('t', Time),
            QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            "cannot coerce IRI_Variable into QuantityVariable",
            TimeTemplate, '2024-05-06', None, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'expected Decimal or Quantity or '
            'float or int or str, got QuantityTemplate',
            TimeTemplate, Variable('t', Time), None,
            QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            "cannot coerce IRI_Variable into ItemVariable",
            TimeTemplate, '2024-05-06', None, None, IRI_Variable('x'))

    def test__init__time_template_normalization(self):
        x = Variable('x')
        self.assertRaises(TypeError, TimeTemplate, x, x)
        self.assertRaises(
            TypeError, Time, '2024-05-06', x, x, x)
        self.assert_time_template(
            TimeTemplate('2024-05-06', x, x),
            Time('2024-05-06').time,
            QuantityVariable('x'), QuantityVariable('x'), None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', x, Variable('x', DataValue)),
            Time('2024-05-06').time,
            QuantityVariable('x'), QuantityVariable('x'), None)

    def test__init__snak_template(self):
        self.assert_abstract_class(Snak)

    def test__init__value_snak_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into PropertyVariable",
            ValueSnakTemplate, IRI_Variable('x'), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce SnakVariable into ValueVariable",
            ValueSnakTemplate, Property('p'), Variable('x', Snak))

    def test__init__value_snak_template_normalization(self):
        x = Variable('x')
        self.assertEqual(
            ValueSnak(x, x),
            ValueSnak(PropertyVariable('x'), PropertyVariable('x')))

    def test__init__some_value_snak_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into PropertyVariable",
            SomeValueSnakTemplate, IRI_Variable('x'))

    def test__init__no_value_snak_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into PropertyVariable",
            NoValueSnakTemplate, IRI_Variable('x'))

    def test__init__statement_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into EntityVariable",
            StatementTemplate, IRI_Variable('x'), x)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce IRI_Variable into SnakVariable",
            StatementTemplate, x, IRI_Variable('x'))

    def test__init__statement_template_normalization(self):
        x = Variable('x')
        self.assertRaises(TypeError, Statement, x, x)
        self.assertEqual(
            StatementTemplate(x, x(x)),
            StatementTemplate(PropertyVariable('x'), ValueSnak(
                PropertyVariable('x'), PropertyVariable('x'))))
        self.assertEqual(
            StatementTemplate(x, SomeValueSnak(x)),
            StatementTemplate(
                PropertyVariable('x'),
                SomeValueSnak(PropertyVariable('x'))))
        self.assertEqual(
            StatementTemplate(x, NoValueSnak(x)),
            StatementTemplate(
                PropertyVariable('x'),
                NoValueSnak(PropertyVariable('x'))))

# -- variables -------------------------------------------------------------

    def test_variables(self):
        x, y, z = Variables('x', 'y', 'z')
        self.assertEqual(
            cast(StatementTemplate, Statement(
                x, ValueSnak(y, Quantity(123, x, z)))).variables, {
                ItemVariable('x'),
                PropertyVariable('y'),
                QuantityVariable('z')})

# -- instantiate -----------------------------------------------------------

    def test_instantiate(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate IRI_Variable 'x' with Item",
            ItemTemplate(x).instantiate, {IRI_Variable('x'): Item('x')})
        self.assertEqual(
            ItemTemplate(x).instantiate({IRI_Variable('x'): IRI('x')}),
            Item(IRI('x')))


if __name__ == '__main__':
    Test.main()
