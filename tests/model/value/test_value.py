# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import decimal

from kif_lib import (
    Datatype,
    DataValue,
    DeepDataValue,
    Entity,
    ExternalId,
    IRI,
    Item,
    Lexeme,
    Property,
    Quantity,
    ShallowDataValue,
    String,
    Text,
    Time,
    Value,
    ValueTemplate,
    ValueVariable,
    Variable,
)
from kif_lib.model import AndFingerprint, OrFingerprint, ValueFingerprint
from kif_lib.typing import assert_type, cast

from ...tests import ValueTestCase


class Test(ValueTestCase):

    def test_template_class(self) -> None:
        assert_type(Value.template_class, type[ValueTemplate])
        self.assertIs(Value.template_class, ValueTemplate)

    def test_variable_class(self) -> None:
        assert_type(Value.variable_class, type[ValueVariable])
        self.assertIs(Value.variable_class, ValueVariable)

    def test_check(self) -> None:
        assert_type(Value.check(0), Value)
        super()._test_check(
            Value,
            success=[
                ('x', String('x')),
                (0, Quantity(0)),
                (1.0, Quantity(1.0)),
                (datetime.datetime(
                    2024, 6, 26, tzinfo=datetime.timezone.utc),
                 Time(datetime.datetime(
                     2024, 6, 26, tzinfo=datetime.timezone.utc))),
                (decimal.Decimal(0), Quantity(0)),
                (ExternalId('x'), ExternalId('x')),
                (IRI('x'), IRI('x')),
                (Item('x'), Item('x')),
                (Lexeme('x'), Lexeme('x')),
                (Property('x', Item), Property('x', Item)),
                (Text('x', 'y'), Text('x', 'y')),
            ],
            failure=[
                Datatype(Item),
                IRI(Variable('x')),
                Variable('x'),
                {},
            ])

    def test__init__(self) -> None:
        self.assert_abstract_class(Value)

    def test__and__(self) -> None:
        assert_type(String('x') & Quantity(0), AndFingerprint)
        self.assert_and_fingerprint(
            String('x') & Quantity(0),
            ValueFingerprint(String('x')),
            ValueFingerprint(Quantity(0)))

    def test__rand__(self) -> None:
        assert_type('x' & Quantity(0), AndFingerprint)
        self.assert_and_fingerprint(
            'x' & Quantity(0),
            ValueFingerprint(String('x')),
            ValueFingerprint(Quantity(0)))

    def test__or__(self) -> None:
        assert_type(String('x') | Quantity(0), OrFingerprint)
        self.assert_or_fingerprint(
            String('x') | Quantity(0),
            ValueFingerprint(String('x')),
            ValueFingerprint(Quantity(0)))

    def test__ror__(self) -> None:
        assert_type('x' | Quantity(0), OrFingerprint)
        self.assert_or_fingerprint(
            'x' | Quantity(0),
            ValueFingerprint(String('x')),
            ValueFingerprint(Quantity(0)))

    def test_n3(self) -> None:
        self.assertEqual(Item('x').n3(), '<x>')
        self.assertEqual(Property('x', Item).n3(), '<x>')
        self.assertEqual(Lexeme('x').n3(), '<x>')
        self.assertEqual(IRI('x').n3(), '<x>')
        self.assertEqual(Text('x', 'y').n3(), '"x"@y')
        self.assertEqual(String('x').n3(), '"x"')
        self.assertEqual(ExternalId('x').n3(), '"x"')
        self.assertEqual(
            Quantity(0, Item('x'), -1, 1).n3(),
            '"0"^^<http://www.w3.org/2001/XMLSchema#decimal>')
        self.assertEqual(
            Time('2024-06-27', 11, 0, Item('x')).n3(),
            '"2024-06-27T00:00:00+00:00"'
            '^^<http://www.w3.org/2001/XMLSchema#dateTime>')

    def test__from_rdflib(self) -> None:
        from kif_lib.namespace import P, WD, WDT, XSD
        from kif_lib.rdflib import Literal, URIRef

        # item
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Item._from_rdflib, WD.P31)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', DataValue._from_rdflib, WD.Q31)
        self.assert_item(Item._from_rdflib(Literal('x')), IRI('x'))
        self.assert_item(Item._from_rdflib(URIRef('x')), IRI('x'))
        self.assert_item(Item._from_rdflib(WD.Q5), IRI(WD.Q5))
        self.assert_item(cast(Item, Value._from_rdflib(WD.Q5)), IRI(WD.Q5))
        self.assert_item(Item._from_rdflib(WDT.Q5, [WDT]), IRI(WD.Q5))
        self.assert_item(
            cast(Item, Entity._from_rdflib(WDT.Q5, [WDT])), IRI(WD.Q5))

        # property
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Property._from_rdflib, WD.Q5)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', ShallowDataValue._from_rdflib, WD.P5)
        self.assert_property(Property._from_rdflib(Literal('x')), IRI('x'))
        self.assert_property(Property._from_rdflib(URIRef('x')), IRI('x'))
        self.assert_property(Property._from_rdflib(WD.P31), IRI(WD.P31))
        self.assert_property(
            cast(Property, Value._from_rdflib(WD.P31)), IRI(WD.P31))
        self.assert_property(
            Property._from_rdflib(P.P31, property_prefixes=[P]), IRI(WD.P31))
        self.assert_property(
            cast(Property, Entity._from_rdflib(P.P31, property_prefixes=[P])),
            IRI(WD.P31))

        # lexeme
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Lexeme._from_rdflib, WD.Q5)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', DeepDataValue._from_rdflib, WD.L5)
        self.assert_lexeme(Lexeme._from_rdflib(Literal('x')), IRI('x'))
        self.assert_lexeme(Lexeme._from_rdflib(URIRef('x')), IRI('x'))
        self.assert_lexeme(Lexeme._from_rdflib(WD.L3873), IRI(WD.L3873))
        self.assert_lexeme(
            cast(Lexeme, Value._from_rdflib(WD.L5)), IRI(WD.L5))
        self.assert_lexeme(
            Lexeme._from_rdflib(WDT.L3873, lexeme_prefixes=[WDT]),
            IRI(WD.L3873))
        self.assert_lexeme(
            cast(Lexeme, Entity._from_rdflib(
                WDT.L3873, lexeme_prefixes=[WDT])),
            IRI(WD.L3873))

        # iri
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Entity._from_rdflib, URIRef('x'))
        self.assert_iri(IRI._from_rdflib(Literal('x')), 'x')
        self.assert_iri(IRI._from_rdflib(URIRef('x')), 'x')
        self.assert_iri(cast(IRI, Value._from_rdflib(URIRef('x'))), 'x')
        self.assert_iri(cast(IRI, DataValue._from_rdflib(URIRef('x'))), 'x')
        self.assert_iri(
            cast(IRI, ShallowDataValue._from_rdflib(URIRef('x'))), 'x')

        # text
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Text._from_rdflib, WD.Q5)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce',
            DeepDataValue._from_rdflib, Literal('x', 'y'))
        self.assert_text(Text._from_rdflib(Literal('x')), 'x')
        self.assert_text(
            cast(Text, Value._from_rdflib(Literal('x', 'y'))), 'x', 'y')
        self.assert_text(
            cast(Text, DataValue._from_rdflib(Literal('x', 'y'))), 'x', 'y')
        self.assert_text(
            cast(Text, ShallowDataValue._from_rdflib(
                Literal('x', 'y'))), 'x', 'y')
        self.assert_text(Text._from_rdflib(Literal('x', 'y')), 'x', 'y')

        # string
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', String._from_rdflib, WD.Q5)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Entity._from_rdflib, Literal('x'))
        self.assert_string(String._from_rdflib(Literal('x')), 'x')
        self.assert_string(
            cast(String, Value._from_rdflib(Literal('x'))), 'x')
        self.assert_string(
            cast(String, DataValue._from_rdflib(Literal('x'))), 'x')
        self.assert_string(
            cast(String, ShallowDataValue._from_rdflib(Literal('x'))), 'x')

        # external id
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', ExternalId._from_rdflib, WD.Q5)
        self.assert_external_id(
            cast(ExternalId, ExternalId._from_rdflib(Literal('x'))), 'x')

        # quantity
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Quantity._from_rdflib, WD.Q5)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Quantity._from_rdflib,
            Literal('2024-06-27T00:00:00', datatype=XSD.dateTime))
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', ShallowDataValue._from_rdflib,
            Literal('0', datatype=XSD.decimal))
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Quantity._from_rdflib, Literal('x'))
        self.assert_quantity(
            Quantity._from_rdflib(Literal('0')), decimal.Decimal(0))
        self.assert_quantity(
            cast(Quantity, Value._from_rdflib(
                Literal('1.55', datatype=XSD.decimal))),
            decimal.Decimal('1.55'))
        self.assert_quantity(
            cast(Quantity, DataValue._from_rdflib(
                Literal('1.55', datatype=XSD.decimal))),
            decimal.Decimal('1.55'))
        self.assert_quantity(
            cast(Quantity, DeepDataValue._from_rdflib(
                Literal('1.55', datatype=XSD.decimal))),
            decimal.Decimal('1.55'))
        self.assert_quantity(
            Quantity._from_rdflib(Literal('-8', datatype=XSD.decimal)),
            decimal.Decimal('-8'))

        # time
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Time._from_rdflib, WD.Q5)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Time._from_rdflib,
            Literal('0', datatype=XSD.decimal))
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Entity._from_rdflib,
            Literal('0', datatype=XSD.decimal))
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Time._from_rdflib, Literal('x'))
        self.assert_time(
            Time._from_rdflib(Literal('2023-10-03T00:00:00')),
            datetime.datetime(2023, 10, 3, tzinfo=datetime.timezone.utc))
        self.assert_time(
            cast(Time, Value._from_rdflib(
                Literal('2023-10-03T00:00:00', datatype=XSD.dateTime))),
            datetime.datetime(2023, 10, 3, tzinfo=datetime.timezone.utc))
        self.assert_time(
            cast(Time, DataValue._from_rdflib(
                Literal('2023-10-03T00:00:00', datatype=XSD.dateTime))),
            datetime.datetime(2023, 10, 3, tzinfo=datetime.timezone.utc))
        self.assert_time(
            cast(Time, DeepDataValue._from_rdflib(
                Literal('2023-10-03T00:00:00', datatype=XSD.dateTime))),
            datetime.datetime(2023, 10, 3, tzinfo=datetime.timezone.utc))
        self.assert_time(
            Time._from_rdflib(Literal('2023-10-03', datatype=XSD.date)),
            datetime.datetime(2023, 10, 3, tzinfo=datetime.timezone.utc))
        self.assert_time(
            Time._from_rdflib(
                Literal('2023-10-03T11:11:11', datatype=XSD.dateTime)),
            datetime.datetime(
                2023, 10, 3, 11, 11, 11, tzinfo=datetime.timezone.utc))


if __name__ == '__main__':
    Test.main()
