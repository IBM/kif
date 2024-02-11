# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Literal, URIRef

import kif_lib.namespace as NS
import kif_lib.vocabulary as wd
from kif_lib import IRI, Item, Quantity
from kif_lib.model import Decimal

from .tests import kif_TestCase, main


class TestQuantity(kif_TestCase):

    def test__init__(self):
        self.assertRaises(ValueError, Quantity, 'abc', 0)
        self.assertRaises(TypeError, Quantity, 0, 'x', 'abc')
        self.assertRaises(TypeError, Quantity, 0, 'x', None, 'abc')
        self.assert_quantity(Quantity(1), 1)
        self.assert_quantity(Quantity(-1), '-1')
        self.assert_quantity(Quantity(1.), '1.0')
        self.assert_quantity(Quantity(Decimal('-0.1')), '-0.1')
        self.assert_quantity(Quantity(-.1), -.1)
        self.assert_quantity(Quantity('+1'), '1')
        self.assert_quantity(Quantity(1., Item('x')), '1.0', Item('x'))
        self.assert_quantity(
            Quantity(1., Item('ms')), '1.0', Item(IRI('ms')))
        self.assert_quantity(Quantity('1.', None, '8'), '1.0', None, '8')
        self.assert_quantity(
            Quantity(1., Item('ms'), 8), '1.0', Item('ms'), '8')
        self.assert_quantity(
            Quantity(1., None, None, 20), '1.0', None, None, '20')
        self.assert_quantity(
            Quantity(1., Item('abc'), None, 20),
            '1.0', Item('abc'), None, '20')
        self.assert_quantity(
            Quantity(1., Item('abc'), -1.5, 20),
            '1.0', Item('abc'), '-1.5', '20')

    def test_get_unit(self):
        self.assertEqual(Quantity(0, Item('x')).get_unit(), Item('x'))
        self.assertEqual(Quantity(0).get_unit(Item('x')), Item('x'))
        self.assertEqual(Quantity(0).get_unit(Item(IRI('x'))), Item('x'))
        self.assertIsNone(Quantity(0).get_unit())

    def test_get_lower_bound(self):
        self.assertEqual(
            Quantity(0, None, 1).get_lower_bound(), Decimal('1'))
        self.assertEqual(
            Quantity(0, None).get_lower_bound(Decimal('1.')), Decimal('1.'))
        self.assertIsNone(Quantity(0, None).get_lower_bound())

    def test_get_upper_bound(self):
        self.assertEqual(
            Quantity(0, None, 1, 2).get_upper_bound(), Decimal('2'))
        self.assertEqual(Quantity(0).get_upper_bound(2), Decimal(2))
        self.assertIsNone(Quantity(0, None).get_upper_bound())

    def test__from_rdflib(self):
        # bad argument: uri
        self.assertRaises(TypeError, Quantity._from_rdflib, URIRef('x'))
        # bad argument: untyped literal
        self.assertRaises(TypeError, Quantity._from_rdflib, Literal('x'))
        # bad argument: ill-typed literal
        self.assertRaises(
            TypeError, Quantity._from_rdflib, Literal(
                '2023-10-03', datatype=NS.XSD.dateTime))
        # good arguments
        self.assert_quantity(
            Quantity._from_rdflib(Literal('1.55', datatype=NS.XSD.decimal)),
            Decimal('1.55'))
        self.assert_quantity(
            Quantity._from_rdflib(Literal('-8', datatype=NS.XSD.decimal)),
            Decimal('-8'))

    def test__to_rdflib(self):
        self.assertEqual(
            Quantity(-1, wd.kilogram)._to_rdflib(),
            Literal('-1', datatype=NS.XSD.decimal))


if __name__ == '__main__':
    main()
