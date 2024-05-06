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
    ExternalIdTemplate,
    IRI_Template,
    ItemTemplate,
    LexemeTemplate,
    NoValueSnakTemplate,
    PropertyTemplate,
    QuantityTemplate,
    SomeValueSnakTemplate,
    StatementTemplate,
    StringTemplate,
    Template,
    TextTemplate,
    TimeTemplate,
    ValueSnakTemplate,
)

from ..tests import kif_TestCase


class Test(kif_TestCase):

    def test__check_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._check_arg_template_class, 0)
        self.assertRaises(
            TypeError, Template._check_arg_template_class, int)
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

    def test__preprocess_arg_template_class(self):
        self.assertRaises(
            TypeError, Template._preprocess_arg_template_class, 0, 1)
        self.assertRaises(
            TypeError, Template._preprocess_arg_template_class, int, 1)
        self.assertIs(
            Template._preprocess_arg_template_class(ItemTemplate, 1),
            ItemTemplate)
        self.assertIs(
            Template._preprocess_arg_template_class(Item, 1),
            ItemTemplate)

    def test__preprocess_optional_arg_template_class(self):
        self.assertRaises(
            TypeError,
            Template._preprocess_optional_arg_template_class, 0, 1)
        self.assertRaises(
            TypeError,
            Template._preprocess_optional_arg_template_class, int, 1)
        self.assertIsNone(
            Template._preprocess_optional_arg_template_class(None, 1))
        self.assertEqual(
            Template._preprocess_optional_arg_template_class(
                None, 1, ItemTemplate), ItemTemplate)
        self.assertEqual(
            Template._preprocess_optional_arg_template_class(
                Item, 1, PropertyTemplate), ItemTemplate)

# -- __new__ ---------------------------------------------------------------

    def test___new__item_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or String or URIRef or str, got int',
            (ItemTemplate, 'Item'), 0)
        self.assert_item_template(ItemTemplate(x), Variable('x', IRI))
        self.assert_item_template(Item(x), Variable('x', IRI))
        self.assert_item_template(ItemTemplate(IRI(x)), IRI(x))
        self.assert_item_template(Item(IRI(x)), IRI(x))
        self.assert_item(ItemTemplate(IRI('x')), IRI('x'))

    def test__new__property_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or String or URIRef or str, got int',
            (PropertyTemplate, 'Property'), 0)
        self.assert_property_template(PropertyTemplate(x), Variable('x', IRI))
        self.assert_property_template(Property(x), Variable('x', IRI))
        self.assert_property_template(PropertyTemplate(IRI(x)), IRI(x))
        self.assert_property_template(Property(IRI(x)), IRI(x))
        self.assert_property(PropertyTemplate(IRI('x')), IRI('x'))

    def test__new__lexeme_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or String or URIRef or str, got int',
            (LexemeTemplate, 'Lexeme'), 0)
        self.assert_lexeme_template(LexemeTemplate(x), Variable('x', IRI))
        self.assert_lexeme_template(Lexeme(x), Variable('x', IRI))
        self.assert_lexeme_template(LexemeTemplate(IRI(x)), IRI(x))
        self.assert_lexeme_template(Lexeme(IRI(x)), IRI(x))
        self.assert_lexeme(LexemeTemplate(IRI('x')), IRI('x'))

    def test__new__iri_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (IRI_Template, 'IRI'), 0)
        self.assert_iri_template(IRI_Template(x), Variable('x', String))
        self.assert_iri_template(IRI(x), Variable('x', String))
        self.assert_iri(IRI(String('x')), 'x')

    def test__new__text_template(self):
        x, y = Variables('x', 'y')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (TextTemplate, 'Text'), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'expected str, got int',
            (TextTemplate, 'Text'), 'x', 0)
        self.assert_text_template(
            TextTemplate(x, y), Variable('x', String), Variable('y', String))
        self.assert_text_template(
            TextTemplate('x', y), 'x', Variable('y', String))
        self.assert_text_template(
            TextTemplate(x, 'y'), Variable('x', String), 'y')
        self.assert_text_template(
            TextTemplate(x), Variable('x', String), Text.default_language)
        self.assert_text_template(
            Text(x, y), Variable('x', String), Variable('y', String))
        self.assert_text(Text(String('x'), String('y')), 'x', 'y')

    def test__new__string_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (StringTemplate, 'String'), 0)
        self.assert_string_template(StringTemplate(x), Variable('x', String))
        self.assert_string_template(String(x), Variable('x', String))
        self.assert_string(String('x'), 'x')

    def test__new__external_id_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (ExternalIdTemplate, 'ExternalId'), 0)
        self.assert_external_id_template(
            ExternalIdTemplate(x), Variable('x', String))
        self.assert_external_id_template(
            ExternalId(x), Variable('x', String))
        self.assert_external_id(ExternalId('x'), 'x')

    def test__new__quantity_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            ValueError, 1, None, 'expected Decimal',
            (QuantityTemplate, 'Quantity'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected IRI or Item or String or URIRef or str, got int',
            (QuantityTemplate, 'Quantity'), 0, 0)
        self.assert_raises_bad_argument(
            ValueError, 3, None, 'expected Decimal',
            (QuantityTemplate, 'Quantity'), 0, None, 'x')
        self.assert_raises_bad_argument(
            ValueError, 4, None, 'expected Decimal',
            (QuantityTemplate, 'Quantity'), 0, None, None, 'x')
        self.assert_quantity_template(
            QuantityTemplate(x), Variable('x', Quantity), None, None, None)
        self.assert_quantity_template(
            QuantityTemplate(0, x), 0, Variable('x', Item), None, None)
        self.assert_quantity_template(
            QuantityTemplate(0, None, x),
            0, None, Variable('x', Quantity), None)
        self.assert_quantity_template(
            QuantityTemplate(0, None, None, x),
            0, None, None, Variable('x', Quantity))
        self.assert_quantity_template(
            QuantityTemplate(
                Variable('x'),
                Variable('y'),
                Variable('z'),
                Variable('w')),
            Variable('x', Quantity),
            Variable('y', Item),
            Variable('z', Quantity),
            Variable('w', Quantity))
        self.assert_quantity_template(
            Quantity(x), Variable('x', Quantity), None, None, None)
        self.assert_quantity_template(
            Quantity(0, Item(x)),
            0, ItemTemplate(Variable('x', IRI)), None, None)
        self.assert_quantity_template(
            Quantity(0, Item(IRI(x))),
            0, ItemTemplate(IRI_Template(Variable('x', String))), None, None)
        self.assert_quantity_template(
            Quantity(0, None, x), 0, None, Variable('x', Quantity), None)
        self.assert_quantity_template(
            Quantity(0, None, 0, x), 0, None, 0, Variable('x', Quantity))

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
            TypeError, 4, None,
            'expected IRI or Item or String or URIRef or str, got int',
            (TimeTemplate, 'Time'), '2024-05-06', None, None, 0)
        self.assert_time_template(
            TimeTemplate(x), Variable('x', Time), None, None, None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', Variable('x')),
            Time('2024-05-06').time, Variable('x', Quantity), None, None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', None, Variable('x')),
            Time('2024-05-06').time, None, Variable('x', Quantity), None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', None, None, x),
            Time('2024-05-06').time, None, None, Variable('x', Item))
        self.assert_time_template(
            TimeTemplate(
                Variable('x'),
                Variable('y'),
                Variable('z'),
                Variable('w')),
            Variable('x', Time),
            Variable('y', Quantity),
            Variable('z', Quantity),
            Variable('w', Item))
        self.assert_time_template(
            Time(x), Variable('x', Time), None, None, None)
        self.assert_time_template(
            Time('2024-05-06', x),
            Time('2024-05-06').time, Variable('x', Quantity), None, None)
        self.assert_time_template(
            Time('2024-05-06', None, x),
            Time('2024-05-06').time, None, Variable('x', Quantity), None)
        self.assert_time_template(
            Time('2024-05-06', None, None, x),
            Time('2024-05-06').time, None, None, Variable('x', Item))
        self.assert_time_template(
            Time('2024-05-06', None, None, Item(IRI(x))),
            Time('2024-05-06').time, None, None,
            ItemTemplate(IRI_Template(Variable('x', String))))

    def test__new__value_snak_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or Property or String or URIRef or str, got int',
            (ValueSnakTemplate, 'ValueSnak'), 0, Item('x'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected URIRef or Value or datetime or float or int or str, '
            'got dict',
            (ValueSnakTemplate, 'ValueSnak'), Property('x'), dict())
        self.assert_value_snak_template(
            ValueSnakTemplate(x, 0), Variable('x', Property), Quantity(0))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property(x), 0),
            PropertyTemplate(Variable('x', IRI)), Quantity(0))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property('p'), x),
            Property('p'), Variable('x', Value))
        self.assert_value_snak_template(
            ValueSnakTemplate(Property('p'), IRI_Template(x)),
            Property('p'), IRI(Variable('x', String)))
        self.assert_value_snak_template(
            ValueSnak(x, 0), Variable('x', Property), Quantity(0))
        self.assert_value_snak_template(
            ValueSnak(Property(x), 0),
            Property(Variable('x', IRI)), Quantity(0))
        self.assert_value_snak_template(
            ValueSnak(Property('p'), x), Property('p'), Variable('x', Value))
        self.assert_value_snak_template(
            ValueSnak(Property('p'), Time(x)),
            Property('p'), Time(Variable('x', Time)))
        self.assert_value_snak_template(
            PropertyTemplate(x)(String('s')),
            PropertyTemplate(x), String('s'))

    def test__new__some_value_snak_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or Property or String or URIRef or str, got int',
            (SomeValueSnakTemplate, 'SomeValueSnak'), 0)
        self.assert_some_value_snak_template(
            SomeValueSnakTemplate(x), Variable('x', Property))
        self.assert_some_value_snak_template(
            SomeValueSnakTemplate(Property(x)),
            PropertyTemplate(Variable('x', IRI)))
        self.assert_some_value_snak_template(
            SomeValueSnak(x), Variable('x', Property))
        self.assert_some_value_snak_template(
            SomeValueSnak(Property(x)),
            Property(Variable('x', IRI)))

    def test__new__no_value_snak_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or Property or String or URIRef or str, got int',
            (NoValueSnakTemplate, 'NoValueSnak'), 0)
        self.assert_no_value_snak_template(
            NoValueSnakTemplate(x), Variable('x', Property))
        self.assert_no_value_snak_template(
            NoValueSnakTemplate(Property(x)),
            PropertyTemplate(Variable('x', IRI)))
        self.assert_no_value_snak_template(
            NoValueSnak(x), Variable('x', Property))
        self.assert_no_value_snak_template(
            NoValueSnak(Property(x)),
            Property(Variable('x', IRI)))

    def test__new_statement_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected Entity, got int',
            (StatementTemplate, 'Statement'), 0, Property('p')(0))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected Snak, got int',
            (StatementTemplate, 'Statement'), Item('x'), 0)
        self.assert_statement_template(
            StatementTemplate(x, Property('p')(0)),
            Variable('x', Entity), Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Lexeme(x), Property('p')(0)),
            LexemeTemplate(Variable('x', IRI)), Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Item('x'), x), Item('x'), Variable('x', Snak))
        self.assert_statement_template(
            StatementTemplate(Item('x'), NoValueSnakTemplate(x)),
            Item('x'), NoValueSnakTemplate(Variable('x', Property)))
        self.assert_statement_template(
            Statement(Lexeme(x), Property('p')(0)),
            Lexeme(Variable('x', IRI)), Property('p')(Quantity(0)))
        self.assert_statement_template(
            StatementTemplate(Item('x'), x), Item('x'), Variable('x', Snak))
        self.assert_statement_template(
            StatementTemplate(Item('x'), NoValueSnak(x)),
            Item('x'), NoValueSnak(Variable('x', Property)))
        self.assert_statement_template(
            PropertyTemplate(x)(Item('i'), String('s')),
            Item('i'), PropertyTemplate(x)(String('s')))

# -- __init__ --------------------------------------------------------------

    def test__init__item_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce ItemVariable 'x' into IRI_Variable",
            ItemTemplate, Variable('x', Item))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI_Template, got ItemTemplate',
            ItemTemplate, ItemTemplate(Variable('x')))

    def test__init__property_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce PropertyVariable 'x' into IRI_Variable",
            PropertyTemplate, Variable('x', Property))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI_Template, got PropertyTemplate',
            PropertyTemplate, PropertyTemplate(Variable('x')))

    def test__init__lexeme_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce LexemeVariable 'x' into IRI_Variable",
            LexemeTemplate, Variable('x', Lexeme))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI_Template, got LexemeTemplate',
            LexemeTemplate, LexemeTemplate(Variable('x')))

    def test__init__iri_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into StringVariable",
            IRI_Template, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected Variable, got StringTemplate',
            IRI_Template, StringTemplate(Variable('x')))

    def test__init__text_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce TextVariable 'x' into StringVariable",
            TextTemplate, Variable('x', Text))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected str, got StringTemplate',
            TextTemplate, StringTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            Variable.CoercionError, 2, None,
            "cannot coerce TextVariable 'y' into StringVariable",
            TextTemplate, 'x', Variable('y', Text))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected str, got StringTemplate',
            TextTemplate, 'x', StringTemplate(Variable('y')))

    def test__init__text_template_normalization(self):
        x = Variable('x')
        self.assert_text_template(
            TextTemplate(x, x), Variable('x', String), Variable('x', String))
        self.assert_text_template(
            TextTemplate(
                Variable('x', ShallowDataValue),
                Variable('x', DataValue)),
            Variable('x', String), Variable('x', String))
        self.assert_text_template(
            TextTemplate(Variable('x', String), Variable('x', String)),
            Variable('x', String), Variable('x', String))

    def test__init__string_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into StringVariable",
            StringTemplate, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "expected Variable, got StringTemplate",
            StringTemplate, StringTemplate(Variable('x')))

    def test__init__external_id_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into StringVariable",
            ExternalIdTemplate, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected Variable, got IRI_Template',
            ExternalIdTemplate, IRI_Template(Variable('x')))

    def test__init__quantity_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into QuantityVariable",
            QuantityTemplate, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected Decimal or float or int or str, got QuantityTemplate',
            QuantityTemplate, QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            Variable.CoercionError, 2, None,
            "cannot coerce IRI_Variable 'x' into ItemVariable",
            QuantityTemplate, 0, Variable('x', IRI))
        self.assert_raises_bad_argument(
            Variable.CoercionError, 3, None,
            "cannot coerce IRI_Variable 'x' into QuantityVariable",
            QuantityTemplate, 0, None, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'expected Decimal or float or int or str, got QuantityTemplate',
            QuantityTemplate, 0, None, QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            Variable.CoercionError, 4, None,
            "cannot coerce IRI_Variable 'x' into QuantityVariable",
            QuantityTemplate, 0, None, None, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 4, None,
            'expected Decimal or float or int or str, got QuantityTemplate',
            QuantityTemplate, 0, None, None, QuantityTemplate(Variable('x')))

    def test__init__quantity_template_normalization(self):
        x = Variable('x')
        self.assertRaises(Variable.CoercionError, QuantityTemplate, x, x)
        self.assertRaises(Variable.CoercionError, Quantity, 0, x, x)
        self.assertRaises(
            Variable.CoercionError, QuantityTemplate, 0, x, None, x)
        self.assert_quantity_template(
            QuantityTemplate(x, None, x),
            Variable('x', Quantity), None, Variable('x', Quantity), None)
        self.assert_quantity_template(
            QuantityTemplate(x, None, x, Variable('x', DeepDataValue)),
            Variable('x', Quantity), None,
            Variable('x', Quantity), Variable('x', Quantity))
        self.assert_quantity_template(
            QuantityTemplate(
                x, None, Variable('x', DataValue),
                Variable('x', DeepDataValue)),
            Variable('x', Quantity), None,
            Variable('x', Quantity), Variable('x', Quantity))

    def test__init__time_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into TimeVariable",
            TimeTemplate, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected datetime or str, got TimeTemplate',
            TimeTemplate, TimeTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            Variable.CoercionError, 2, None,
            "cannot coerce IRI_Variable 'x' into QuantityVariable",
            TimeTemplate, '2024-05-06', Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected Decimal or Quantity or Time.Precision or '
            'float or int or str, got QuantityTemplate',
            TimeTemplate, Variable('t', Time),
            QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            Variable.CoercionError, 3, None,
            "cannot coerce IRI_Variable 'x' into QuantityVariable",
            TimeTemplate, '2024-05-06', None, Variable('x', IRI))
        self.assert_raises_bad_argument(
            TypeError, 3, None,
            'expected Decimal or Quantity or '
            'float or int or str, got QuantityTemplate',
            TimeTemplate, Variable('t', Time), None,
            QuantityTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            Variable.CoercionError, 4, None,
            "cannot coerce IRI_Variable 'x' into ItemVariable",
            TimeTemplate, '2024-05-06', None, None, Variable('x', IRI))

    def test__init__time_template_normalization(self):
        x = Variable('x')
        self.assertRaises(Variable.CoercionError, TimeTemplate, x, x)
        self.assertRaises(
            Variable.CoercionError, Time, '2024-05-06', x, x, x)
        self.assert_time_template(
            TimeTemplate('2024-05-06', x, x),
            Time('2024-05-06').time,
            Variable('x', Quantity), Variable('x', Quantity), None)
        self.assert_time_template(
            TimeTemplate('2024-05-06', x, Variable('x', DataValue)),
            Time('2024-05-06').time,
            Variable('x', Quantity), Variable('x', Quantity), None)

    def test__init__value_snak_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into PropertyVariable",
            ValueSnakTemplate, Variable('x', IRI), 0)
        self.assert_raises_bad_argument(
            Variable.CoercionError, 2, None,
            "cannot coerce SnakVariable 'x' into ValueVariable",
            ValueSnakTemplate, Property('p'), Variable('x', Snak))

    def test__init__value_snak_template_normalization(self):
        x = Variable('x')
        self.assertEqual(
            ValueSnak(x, x),
            ValueSnak(Variable('x', Property), Variable('x', Property)))

    def test__init__some_value_snak_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into PropertyVariable",
            SomeValueSnakTemplate, Variable('x', IRI))

    def test__init__no_value_snak_template(self):
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into PropertyVariable",
            NoValueSnakTemplate, Variable('x', IRI))

    def test__init__statement_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, None,
            "cannot coerce IRI_Variable 'x' into EntityVariable",
            StatementTemplate, Variable('x', IRI), x)
        self.assert_raises_bad_argument(
            Variable.CoercionError, 2, None,
            "cannot coerce IRI_Variable 'x' into SnakVariable",
            StatementTemplate, x, Variable('x', IRI))

    def test__init__statement_template_normalization(self):
        x = Variable('x')
        self.assertRaises(Variable.CoercionError, Statement, x, x)
        self.assertEqual(
            StatementTemplate(x, x(x)),
            StatementTemplate(Variable('x', Property), ValueSnak(
                Variable('x', Property), Variable('x', Property))))
        self.assertEqual(
            StatementTemplate(x, SomeValueSnak(x)),
            StatementTemplate(
                Variable('x', Property),
                SomeValueSnak(Variable('x', Property))))
        self.assertEqual(
            StatementTemplate(x, NoValueSnak(x)),
            StatementTemplate(
                Variable('x', Property),
                NoValueSnak(Variable('x', Property))))

# -- variables -------------------------------------------------------------

    def test_variables(self):
        x, y, z = Variables('x', 'y', 'z')
        self.assertEqual(
            Statement(x, ValueSnak(y, Quantity(123, x, z))).variables, {
                Variable('x', Item),
                Variable('y', Property),
                Variable('z', Quantity)})

# -- instantiate -----------------------------------------------------------

    def test_instantiate(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate IRI_Variable 'x' with Item",
            ItemTemplate(x).instantiate, {Variable('x', IRI): Item('x')})
        self.assertEqual(
            ItemTemplate(x).instantiate({Variable('x', IRI): IRI('x')}),
            Item(IRI('x')))


if __name__ == '__main__':
    Test.main()
