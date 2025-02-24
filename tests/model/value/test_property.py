# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime

from kif_lib import (
    Context,
    DatatypeVariable,
    Entity,
    ExternalId,
    IRI,
    IRI_Variable,
    Item,
    ItemDatatype,
    itertools,
    Lexeme,
    NoValueSnak,
    PreferredRank,
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    QualifierRecord,
    Quantity,
    QuantityDatatype,
    ReferenceRecord,
    ReferenceRecordSet,
    SomeValueSnak,
    Statement,
    String,
    Term,
    Text,
    Theta,
    Time,
    Value,
    ValueSnak,
    Variable,
)
from kif_lib.model import TDatatype, TValue
from kif_lib.typing import (
    Any,
    assert_type,
    cast,
    ClassVar,
    Iterable,
    Optional,
    Set,
)

from ...tests import EntityTestCase


class Test(EntityTestCase):

    def assert_register(self, prop: Property, **kwargs: Any) -> None:
        res = prop.register(**kwargs)
        dt = prop.context.entities.get_range(prop)
        self.assertEqual(res, Property(prop.iri, dt))

    def assert_unregister(self, prop: Property, **kwargs: Any) -> None:
        self.assertTrue(prop.unregister(**kwargs))

    def test_datatype_class(self) -> None:
        assert_type(Property.datatype_class, type[PropertyDatatype])
        self.assertIs(Property.datatype_class, PropertyDatatype)

    def test_datatype(self) -> None:
        assert_type(Property.datatype, PropertyDatatype)
        self.assert_property_datatype(Property.datatype)

    def test_template_class(self) -> None:
        assert_type(Property.template_class, type[PropertyTemplate])
        self.assertIs(Property.template_class, PropertyTemplate)

    def test_variable_class(self) -> None:
        assert_type(Property.variable_class, type[PropertyVariable])
        self.assertIs(Property.variable_class, PropertyVariable)

    def test_check(self) -> None:
        assert_type(Property.check(Property('x')), Property)
        self._test_check(
            Property,
            success=[
                ('x', Property('x')),
                (ExternalId('x'), Property('x')),
            ],
            failure=[
                Item('x'),
                Lexeme('x'),
                PropertyTemplate(Variable('x')),
                Text('x'),
                Variable('x', Text)
            ])

    def test__init__(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce Item into Datatype',
            Property, 'x', Item('y'))
        # success
        assert_type(Property('x'), Property)
        self._test__init__(
            Property,
            self.assert_property,
            success=[
                (['x', String('y')], Property('x', 'y')),  # type: ignore
            ],
            failure=[
                ['x', Item('y')],
                ['x', Text('y')],
                [Item('x')],
                [Lexeme('x')],
                [PropertyTemplate(Variable('x'))],
                [Text('x')],
                [Variable('x', Text)],
            ])
        self.assert_property(Property('x'), IRI('x'), None)
        self.assert_property(
            Property('x', Item), IRI('x'), Item.datatype)
        self.assert_property(
            Property('x', Item.datatype_class), IRI('x'), Item.datatype)
        self.assert_property(
            Property('x', Item.datatype), IRI('x'), Item.datatype)

    _test__call__entities: ClassVar[list[Entity]] = [
        Item('x'),
        Lexeme('z'),
        Property('y', Item.datatype)
    ]

    _test__call__values: ClassVar[list[tuple[TValue, TDatatype]]] = [
        ('x', String),
        (0, Quantity),
        (datetime.datetime(2024, 6, 24, tzinfo=datetime.timezone.utc), Time),
        (ExternalId('x'), ExternalId),
        (IRI('x'), IRI),
        (Item('x'), Item),
        (Property('x'), Property),
        (Quantity(0), Quantity),
        (String('x'), String),
        (Text('x', 'y'), Text),
        (Time('2024-06-24'), Time),
    ]

    def test__call__(self) -> None:
        # statement
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce int into Entity',
            (Property('x'), 'Statement'), 0, 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce str into Entity',
            (Property('x'), 'Statement'), 'x', 'x')
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce IRI into Entity',
            (Property('x'), 'Statement'), IRI('x'), 'x')
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (Property('x'), 'ValueSnak'), Item('x'), {})
        # success
        assert_type(Property('p')(Item('x'), IRI('y')), Statement)
        it = itertools.product(
            self._test__call__entities, self._test__call__values)
        for e, (v, dt) in it:
            self.assert_statement(
                Property('p')(e, v), e, ValueSnak(Property('p'), v))
            self.assert_statement(
                cast(Statement, PropertyTemplate('p')(e, v)),
                e, ValueSnak(Property('p'), v))
            self.assert_annotated_statement(
                Property('p')(e, v, [Property('p')(0)]),
                e, ValueSnak(Property('p'), v),
                QualifierRecord(Property('p')(0)))
            self.assert_annotated_statement(
                Property('p')(e, v, None, [[Property('p')(0)]]),
                e, ValueSnak(Property('p'), v),
                references=ReferenceRecordSet(
                    ReferenceRecord(Property('p')(0))))
            self.assert_annotated_statement(
                Property('p')(e, v, None, None, PreferredRank()),
                e, ValueSnak(Property('p'), v),
                rank=PreferredRank())
        # value snak
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value',
            (Property('x'), 'ValueSnak'), {})
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce ValueSnak into Value',
            (Property('x'), 'ValueSnak'),
            ValueSnak(Property('p'), Item('x')))
        # success
        assert_type(Property('p')(String('x')), ValueSnak)
        for v, dt in self._test__call__values:
            self.assert_value_snak(
                Property('p')(v), Property('p', dt), Value.check(v))
            self.assert_value_snak(
                cast(ValueSnak, PropertyTemplate('p')(v)),
                Property('p', dt), Value.check(v))

    def test_no_value(self) -> None:
        # statement
        assert_type(Property('x').no_value(Item('y')), Statement)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into Entity',
            (Property('x').no_value, 'Statement'), {})
        self.assert_statement(
            Property('x').no_value(Item('y')),
            Item('y'), NoValueSnak(Property('x', None)))
        self.assert_annotated_statement(
            Property('x').no_value(Item('y'), rank=PreferredRank()),
            Item('y'), NoValueSnak(Property('x', None)),
            rank=PreferredRank())
        # no value snak
        assert_type(Property('x').no_value(), NoValueSnak)
        self.assert_no_value_snak(Property('x').no_value(), Property('x'))
        self.assert_no_value_snak(
            Property('x', Item).no_value(), Property('x', Item))
        self.assert_no_value_snak(
            Property('x', Quantity).no_value(), Property('x', Quantity))

    def test_some_value(self) -> None:
        # statement
        assert_type(Property('x').some_value(Item('y')), Statement)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'cannot coerce dict into Entity',
            (Property('x').some_value, 'Statement'), {})
        self.assert_statement(
            Property('x').some_value(Item('y')),
            Item('y'), SomeValueSnak(Property('x', None)))
        self.assert_annotated_statement(
            Property('x').some_value(Item('y'), rank=PreferredRank()),
            Item('y'), SomeValueSnak(Property('x', None)),
            rank=PreferredRank())
        # some value snak
        assert_type(Property('x').some_value(), SomeValueSnak)
        self.assert_some_value_snak(Property('x').some_value(), Property('x'))
        self.assert_some_value_snak(
            Property('x', Item).some_value(), Property('x', Item))
        self.assert_some_value_snak(
            Property('x', Quantity).some_value(), Property('x', Quantity))

    def test_variables(self) -> None:
        assert_type(Property('x').variables, Set[Variable])
        self._test_variables(Property, (Property('x', Item), set()))

    def test_instantiate(self) -> None:
        assert_type(Item('x').instantiate({}), Term)
        self._test_instantiate(
            Property,
            success=[
                (Property('x', Item),
                 Property('x', Item),
                 {IRI_Variable('x'): IRI('y')})
            ])

    def test_match(self) -> None:
        assert_type(Property('x').match(Variable('x')), Optional[Theta])
        self._test_match(
            Property,
            success=[
                (Property('x'),
                 Property(Variable('x'), Variable('y')),
                 {IRI_Variable('x'): IRI('x'),
                  DatatypeVariable('y'): None}),
                (Property('x', Quantity),
                 Property('x', Variable('y')),
                 {DatatypeVariable('y'): QuantityDatatype()}),
            ],
            failure=[
                (Property('x'), Property('x', Item)),
                (Property('x', Quantity), Property(Variable('x'), Item)),
            ])

    def test_display(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            (Property('x').display, 'Property.get_label'), 0)
        with Context():
            assert_type(Property('x').display(), str)
            self.assertEqual(Property('x').display(), 'x')
            self.assertEqual(Property('x').display('pt'), 'x')
            self.assert_register(
                Property('x'), labels=['abc@en', Text('abc@pt', 'pt')])
            self.assertEqual(Property('x').display(), 'abc@en')
            self.assertEqual(Property('x').display('en'), 'abc@en')
            self.assertEqual(Property('x').display('pt'), 'abc@pt')
            self.assertEqual(Property('x').display('fr'), 'x')

    def test_describe(self) -> None:
        with Context():
            assert_type(
                Property('x').describe(), Optional[Property.Descriptor])
            self.assertIsNone(Property('x').describe())
            self.assert_register(
                Property('x'), label='abc', alias=Text('abc', 'pt'),
                descriptions=[Text('def', 'fr'), Text('def', 'jp')],
                range=Item, inverse=Property('y'))
            self.assertEqual(
                Property('x').describe(),
                {'labels': {'en': Text('abc')},
                 'aliases': {'pt': {Text('abc', 'pt')}},
                 'descriptions': {
                     'fr': Text('def', 'fr'), 'jp': Text('def', 'jp')},
                 'range': ItemDatatype(),
                 'inverse': Property('y')})
        self.assertIsNone(Property('x').describe())

    def test_get_label(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            Property('x').get_label, 0)
        with Context():
            assert_type(Property('x').get_label(), Optional[Text])
            self.assertIsNone(Property('x').get_label())
            self.assert_register(Property('x'), label='abc')
            self.assertEqual(Property('x').get_label('en'), Text('abc'))
            self.assertEqual(Property('x').get_label(), Text('abc'))
            self.assertEqual(Property('x').label, Text('abc'))
            self.assertEqual(Property('x', Item).label, Text('abc'))
        self.assertIsNone(Property('x').label)

    def test_get_aliases(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            Property('x').get_aliases, 0)
        with Context():
            assert_type(Property('x').get_aliases(), Optional[Set[Text]])
            self.assertIsNone(Property('x').get_aliases())
            self.assert_register(Property('x'), alias='abc')
            self.assert_register(Property('x'), aliases=[
                'def', Text('abc', 'pt'), Text('def', 'fr')])
            self.assertEqual(Property('x').get_aliases('en'), {
                Text('abc'), Text('def')})
            self.assertEqual(
                Property('x').get_aliases('pt'), {Text('abc', 'pt')})
            self.assertEqual(
                Property('x').aliases, {Text('abc'), Text('def')})
            self.assertEqual(
                Property('x', Item).aliases, {Text('abc'), Text('def')})
            self.assertIsNone(Property('x').get_label('jp'))
        self.assertIsNone(Property('x').label)

    def test_get_description(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'language', 'cannot coerce int into String',
            Property('x').get_description, 0)
        with Context():
            assert_type(Property('x').get_description(), Optional[Text])
            self.assertIsNone(Property('x').get_description())
            self.assert_register(Property('x'), description='abc')
            self.assertEqual(
                Property('x').get_description('en'), Text('abc'))
            self.assertEqual(Property('x').get_description(), Text('abc'))
            self.assertEqual(Property('x').description, Text('abc'))
            self.assertEqual(Property('x', Item).description, Text('abc'))
        self.assertIsNone(Property('x').description)

    def test_get_inverse(self) -> None:
        with Context():
            assert_type(Property('x').get_inverse(), Optional[Property])
            self.assertIsNone(Property('x').get_inverse())
            self.assert_register(Property('x'), inverse=Property('y'))
            self.assertEqual(Property('x').get_inverse(), Property('y'))
            self.assert_register(Property('x'), inverse=Property('z'))
            self.assertEqual(Property('x').get_inverse(), Property('z'))
        self.assertIsNone(Property('x').inverse)

    def test_Properties(self) -> None:
        assert_type(Properties('a', 'b', 'c'), Iterable[Property])
        self._test_Entities(
            Properties,
            self.assert_property,
            failure=[
                Item('x'),
                Lexeme('x'),
                Property('x'),
                PropertyTemplate(Variable('x')),
                Text('x'),
                Variable('x', Text),
            ])


if __name__ == '__main__':
    Test.main()
