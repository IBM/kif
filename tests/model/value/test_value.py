# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from kif_lib import (
    Entity,
    ExternalId,
    IRI,
    Item,
    Lexeme,
    Property,
    Quantity,
    String,
    Text,
    Time,
    Value,
    ValueTemplate,
    ValueVariable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ValueTestCase


class Test(kif_ValueTestCase):

    def test_template_class(self) -> None:
        assert_type(Value.template_class, type[ValueTemplate])

    def test_variable_class(self) -> None:
        assert_type(Value.variable_class, type[ValueVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(Value, {}, Value.check)
        # success
        assert_type(Value.check(0), Value)
        self.assertEqual(Value.check('x'), String('x'))
        self.assertEqual(
            Value.check(datetime.datetime(
                2024, 6, 26, tzinfo=datetime.timezone.utc)),
            Time('2024-06-26'))
        self.assertEqual(Value.check(decimal.Decimal(0)), Quantity(0))
        self.assertEqual(Value.check(Item('x')), Item('x'))

    def test__init__(self):
        self.assert_abstract_class(Value)

    def test_value(self):
        self.assertEqual(Item('x').value, 'x')
        self.assertEqual(Property('x', Item).value, 'x')
        self.assertEqual(Lexeme('x').value, 'x')
        self.assertEqual(IRI('x').value, 'x')
        self.assertEqual(Text('x', 'y').value, 'x')
        self.assertEqual(String('x').value, 'x')
        self.assertEqual(ExternalId('x').value, 'x')
        self.assertEqual(Quantity(0, Item('x'), -1, 1).value, '0')
        self.assertEqual(
            Time('2024-06-27', 11, 0, Item('x')).value,
            '2024-06-27T00:00:00+00:00')

    def test_n3(self):
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

    def test__from_rdflib(self):
        from kif_lib.namespace import P, WD, WDT, XSD
        from kif_lib.rdflib import Literal, URIRef

        # item
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Item._from_rdflib, WD.P31)
        self.assert_item(Item._from_rdflib(Literal('x')), IRI('x'))
        self.assert_item(Item._from_rdflib(URIRef('x')), IRI('x'))
        self.assert_item(Item._from_rdflib(WD.Q5), IRI(WD.Q5))
        self.assert_item(Value._from_rdflib(WD.Q5), IRI(WD.Q5))
        self.assert_item(Item._from_rdflib(WDT.Q5, [WDT]), IRI(WD.Q5))
        self.assert_item(Entity._from_rdflib(WDT.Q5, [WDT]), IRI(WD.Q5))

        # property
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Property._from_rdflib, WD.Q5)
        self.assert_property(Property._from_rdflib(Literal('x')), IRI('x'))
        self.assert_property(Property._from_rdflib(URIRef('x')), IRI('x'))
        self.assert_property(Property._from_rdflib(WD.P31), IRI(WD.P31))
        self.assert_property(Value._from_rdflib(WD.P31), IRI(WD.P31))
        self.assert_property(
            Property._from_rdflib(P.P31, property_prefixes=[P]), IRI(WD.P31))
        self.assert_property(
            Entity._from_rdflib(P.P31, property_prefixes=[P]), IRI(WD.P31))

        # lexeme
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Lexeme._from_rdflib, WD.Q5)
        self.assert_lexeme(Lexeme._from_rdflib(Literal('x')), IRI('x'))
        self.assert_lexeme(Lexeme._from_rdflib(URIRef('x')), IRI('x'))
        self.assert_lexeme(Lexeme._from_rdflib(WD.L3873), IRI(WD.L3873))
        self.assert_lexeme(Value._from_rdflib(WD.L5), IRI(WD.L5))
        self.assert_lexeme(
            Lexeme._from_rdflib(WDT.L3873, lexeme_prefixes=[WDT]),
            IRI(WD.L3873))
        self.assert_lexeme(
            Entity._from_rdflib(WDT.L3873, lexeme_prefixes=[WDT]),
            IRI(WD.L3873))

        # iri
        self.assert_iri(IRI._from_rdflib(Literal('x')), 'x')
        self.assert_iri(IRI._from_rdflib(URIRef('x')), 'x')
        self.assert_iri(Value._from_rdflib(URIRef('x')), 'x')

        # text
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Text._from_rdflib, WD.Q5)
        self.assert_text(Text._from_rdflib(Literal('x')), 'x')
        self.assert_text(Value._from_rdflib(Literal('x', 'y')), 'x', 'y')
        self.assert_text(Text._from_rdflib(Literal('x', 'y')), 'x', 'y')

        # string
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', String._from_rdflib, WD.Q5)
        self.assert_string(String._from_rdflib(Literal('x')), 'x')
        self.assert_string(Value._from_rdflib(Literal('x')), 'x')

        # external id
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', ExternalId._from_rdflib, WD.Q5)
        self.assert_external_id(ExternalId._from_rdflib(Literal('x')), 'x')

        # quantity
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Quantity._from_rdflib, WD.Q5)
        self.assertRaisesRegex(
            TypeError, 'cannot coerce', Quantity._from_rdflib,
            Literal('2024-06-27T00:00:00', datatype=XSD.dateTime))
        self.assertRaisesRegex(
            ValueError, 'cannot coerce', Quantity._from_rdflib, Literal('x'))
        self.assert_quantity(Quantity._from_rdflib(Literal('0')), 0)
        self.assert_quantity(
            Value._from_rdflib(Literal('1.55', datatype=XSD.decimal)),
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
            ValueError, 'cannot coerce', Time._from_rdflib, Literal('x'))
        self.assert_time(
            Time._from_rdflib(Literal('2023-10-03T00:00:00')),
            datetime.datetime(2023, 10, 3, tzinfo=datetime.timezone.utc))
        self.assert_time(
            Value._from_rdflib(
                Literal('2023-10-03T00:00:00', datatype=XSD.dateTime)),
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
