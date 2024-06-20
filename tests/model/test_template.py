# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    DataValue,
    DeepDataValue,
    Entity,
    ExternalId,
    IRI,
    Item,
    ItemDatatype,
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
    DatatypeVariable,
    DataValueTemplate,
    Decimal,
    DeepDataValueTemplate,
    EntityTemplate,
    ExternalIdTemplate,
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
    ShallowDataValueTemplate,
    SnakTemplate,
    SomeValueSnakTemplate,
    StatementTemplate,
    StringTemplate,
    StringVariable,
    Template,
    TextTemplate,
    TextVariable,
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

    # def test__new__(self):
    #     self.assert_test_is_defined_for_template_classes('__new__')

    def test__new__template(self):
        self.assert_abstract_class(Template)

    def test__new__value_template(self):
        self.assert_abstract_class(ValueTemplate)

    def test__new__entity_template(self):
        self.assert_abstract_class(EntityTemplate)

    def test__new__item_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            (ItemTemplate, 'Item'), 0)
        self.assert_item_template(ItemTemplate(x), Variable('x', IRI))
        self.assert_item_template(Item(x), IRI_Variable('x'))
        self.assert_item_template(ItemTemplate(IRI(x)), IRI(x))
        self.assert_item_template(Item(IRI(x)), IRI(x))
        self.assert_item(cast(Item, ItemTemplate(IRI('x'))), IRI('x'))

    def test__new__property_template(self):
        x, y = Variables('x', 'y')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce int into IRI',
            (PropertyTemplate, 'Property'), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected Datatype, got int',
            (PropertyTemplate, 'Property'), IRI('x'), 0)
        self.assert_property_template(
            PropertyTemplate(x), IRI_Variable('x'), None)
        self.assert_property_template(
            PropertyTemplate(x, Item.datatype),
            IRI_Variable('x'), ItemDatatype())
        self.assert_property_template(Property(x), Variable('x', IRI), None)
        self.assert_property_template(
            Property(x, y), IRI_Variable('x'), DatatypeVariable('y'))
        self.assert_property_template(
            PropertyTemplate(IRI(x)), IRI(x), None)
        self.assert_property_template(
            PropertyTemplate(IRI(x), Item), IRI(x), ItemDatatype())
        self.assert_property_template(Property(IRI(x)), IRI(x), None)
        self.assert_property_template(
            Property(IRI('x'), y), IRI('x'), Variable('y', Datatype))
        self.assert_property(
            cast(Property, PropertyTemplate(IRI('x'))), IRI('x'), None)
        self.assert_property(
            Property(IRI('x'), Item), IRI('x'), ItemDatatype())

    def test__new__lexeme_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            (LexemeTemplate, 'Lexeme'), 0)
        self.assert_lexeme_template(
            LexemeTemplate(x), IRI_Variable('x'))
        self.assert_lexeme_template(Lexeme(x), Variable('x', IRI))
        self.assert_lexeme_template(LexemeTemplate(IRI(x)), IRI(x))
        self.assert_lexeme_template(Lexeme(IRI(x)), IRI(x))
        self.assert_lexeme(
            cast(Lexeme, LexemeTemplate(IRI('x'))), IRI('x'))

    def test__new__data_value_template(self):
        self.assert_abstract_class(DataValueTemplate)

    def test__new__shallow_data_value_template(self):
        self.assert_abstract_class(ShallowDataValueTemplate)

    # def test__new__iri_template(self):
    #     x = Variable('x')
    #     self.assert_raises_bad_argument(
    #         TypeError, 1, None, 'expected str, got int',
    #         (IRI_Template, 'IRI'), 0)
    #     self.assert_iri_template(IRI_Template(x), StringVariable('x'))
    #     self.assert_iri_template(IRI(x), Variable('x', String))
    #     self.assert_iri(IRI(String('x')), 'x')

    def test__new__text_template(self):
        x, y = Variables('x', 'y')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into String',
            (TextTemplate, 'Text'), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce int into String',
            (TextTemplate, 'Text'), 'x', 0)
        self.assert_text_template(
            TextTemplate(x, y),
            StringVariable('x'), StringVariable('y'))
        self.assert_text_template(
            TextTemplate('x', y), 'x', StringVariable('y'))
        self.assert_text_template(
            TextTemplate(x, 'y'),
            StringVariable('x'), 'y')
        self.assert_text_template(
            TextTemplate(x), StringVariable('x'),
            Text.default_language)
        self.assert_text_template(
            Text(x, y), Variable('x', String), StringVariable('y'))
        self.assert_text(Text(String('x'), String('y')), 'x', 'y')

    def test__new__string_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (StringTemplate, 'String'), 0)
        self.assert_string_template(
            StringTemplate(x), StringVariable('x'))
        self.assert_string_template(String(x), Variable('x', String))
        self.assert_string(String('x'), 'x')

    def test__new__external_id_template(self):
        x = Variable('x')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int',
            (ExternalIdTemplate, 'ExternalId'), 0)
        self.assert_external_id_template(
            ExternalIdTemplate(x), StringVariable('x'))
        self.assert_external_id_template(
            ExternalId(x), Variable('x', String))
        self.assert_external_id(ExternalId('x'), 'x')

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
            'expected Value, got dict',
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

    def test__init__(self):
        self.assert_test_is_defined_for_template_classes('__init__')

    def test__init__template(self):
        self.assert_abstract_class(Template)

    def test__init__value_template(self):
        self.assert_abstract_class(ValueTemplate)

    def test__init__entity_template(self):
        self.assert_abstract_class(EntityTemplate)

    def test__init__item_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce ItemVariable into IRI_Variable',
            ItemTemplate, ItemVariable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce ItemTemplate into IRI_Template',
            ItemTemplate, ItemTemplate(Variable('x')))

    def test__init__property_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce PropertyVariable into IRI_Variable',
            PropertyTemplate, PropertyVariable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce PropertyTemplate into IRI_Template',
            PropertyTemplate, PropertyTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce IRI_Variable into DatatypeVariable",
            PropertyTemplate, IRI('x'), IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'expected Datatype, got PropertyTemplate',
            PropertyTemplate, 'x', PropertyTemplate(Variable('x')))

    def test__init__property_template_normalization(self):
        x = Variable('x')
        self.assertRaises(TypeError, PropertyTemplate, x, x)
        self.assert_property_template(
            PropertyTemplate(
                IRI(StringVariable('x')), Variable('y')),
            IRI_Template(StringVariable('x')), DatatypeVariable('y'))

    def test__init__lexeme_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce LexemeVariable into IRI_Variable',
            LexemeTemplate, Variable('x', Lexeme))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce LexemeTemplate into IRI_Template',
            LexemeTemplate, LexemeTemplate(Variable('x')))

    def test__init__data_value_template(self):
        self.assert_abstract_class(DataValueTemplate)

    def test__init__shallow_data_value_template(self):
        self.assert_abstract_class(ShallowDataValueTemplate)

    def test__init__iri_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into StringVariable",
            IRI_Template, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce StringTemplate into StringVariable',
            IRI_Template, StringTemplate(Variable('x')))

    def test__init__text_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce TextVariable into StringVariable",
            TextTemplate, TextVariable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce StringTemplate into String',
            TextTemplate, StringTemplate(Variable('x')))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            "cannot coerce TextVariable into StringVariable",
            TextTemplate, 'x', TextVariable('y'))
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce StringTemplate into String',
            TextTemplate, 'x', StringTemplate(Variable('y')))

    def test__init__text_template_normalization(self):
        x = Variable('x')
        self.assert_text_template(
            TextTemplate(x, x), StringVariable('x'), StringVariable('x'))
        self.assert_text_template(
            TextTemplate(
                Variable('x', ShallowDataValue),
                Variable('x', DataValue)),
            StringVariable('x'), StringVariable('x'))
        self.assert_text_template(
            TextTemplate(StringVariable('x'), StringVariable('x')),
            StringVariable('x'), StringVariable('x'))

    def test__init__string_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into StringVariable",
            StringTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce StringTemplate into StringVariable",
            StringTemplate, StringTemplate(Variable('x')))

    def test__init__external_id_template(self):
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            "cannot coerce IRI_Variable into StringVariable",
            ExternalIdTemplate, IRI_Variable('x'))
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI_Template into StringVariable',
            ExternalIdTemplate, IRI_Template(Variable('x')))

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
