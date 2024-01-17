# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif import (
    Deprecated,
    IRI,
    Item,
    KIF_Object,
    Normal,
    NoValueSnak,
    Preferred,
    Property,
    Quantity,
    ReferenceRecord,
    SomeValueSnak,
    Statement,
    String,
    Time,
    ValueSnak,
)
from kif.model import Datetime, Decimal, UTC

from .tests import kif_TestCase, main


class TestModelKIF_Object(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, KIF_Object)

    def test_is(self):
        # is_kif_object
        self.assertTrue(Item('x').is_kif_object())
        self.assertTrue(Item('x').test_kif_object())
        # is_value
        self.assertTrue(Item('x').is_value())
        self.assertTrue(Item('x').test_value())
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertFalse(stmt.is_value())
        self.assertFalse(stmt.test_value())
        # is_entity
        self.assertTrue(Item('x').is_entity())
        self.assertTrue(Item('x').test_entity())
        self.assertFalse(String('x').is_entity())
        self.assertFalse(String('x').test_entity())
        # is_item
        self.assertTrue(Item('x').is_item())
        self.assertTrue(Item('x').test_item())
        self.assertFalse(String('x').is_item())
        self.assertFalse(String('x').test_item())
        # is_property
        self.assertTrue(Property('x').is_property())
        self.assertTrue(Property('x').test_property())
        self.assertFalse(Item('x').is_property())
        self.assertFalse(Item('x').test_property())
        # is_data_value
        self.assertTrue(IRI('x').is_data_value())
        self.assertTrue(IRI('x').test_data_value())
        self.assertFalse(Item('x').is_data_value())
        self.assertFalse(Item('x').test_data_value())
        # is_string
        self.assertTrue(String('x').is_string())
        self.assertTrue(String('x').test_string())
        self.assertFalse(Item('x').is_string())
        self.assertFalse(Item('x').test_string())
        # is_iri
        self.assertTrue(IRI('x').is_iri())
        self.assertTrue(IRI('x').test_iri())
        self.assertFalse(Item('x').is_iri())
        self.assertFalse(Item('x').test_iri())
        # is_deep_data_value
        self.assertTrue(Quantity(0).is_deep_data_value())
        self.assertTrue(Quantity(0).test_deep_data_value())
        self.assertFalse(String('x').is_deep_data_value())
        self.assertFalse(String('x').test_deep_data_value())
        # is_quantity
        self.assertTrue(Quantity(0).is_quantity())
        self.assertTrue(Quantity(0).test_quantity())
        self.assertFalse(String('x').is_quantity())
        self.assertFalse(String('x').test_quantity())
        # is_time
        self.assertTrue(Time('2023-09-18').is_time())
        self.assertTrue(Time('2023-09-18').test_time())
        self.assertFalse(String('2023-09-18').is_time())
        self.assertFalse(String('2023-09-18').test_time())
        # is_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertTrue(snak.is_snak())
        self.assertTrue(snak.test_snak())
        self.assertFalse(String('x').is_snak())
        self.assertFalse(String('x').test_snak())
        # is_value_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertTrue(snak.is_value_snak())
        self.assertTrue(snak.test_value_snak())
        self.assertFalse(String('x').is_value_snak())
        self.assertFalse(String('x').test_value_snak())
        # is_some_value_snak
        snak = SomeValueSnak(Property('x'))
        self.assertTrue(snak.is_some_value_snak())
        self.assertTrue(snak.test_some_value_snak())
        self.assertFalse(String('x').is_some_value_snak())
        self.assertFalse(String('x').test_some_value_snak())
        # is_no_value_snak
        snak = NoValueSnak(Property('x'))
        self.assertTrue(snak.is_no_value_snak())
        self.assertTrue(snak.test_no_value_snak())
        self.assertFalse(String('x').is_no_value_snak())
        self.assertFalse(String('x').test_no_value_snak())
        # is_reference_record
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertTrue(refr.is_reference_record())
        self.assertTrue(refr.test_reference_record())
        self.assertFalse(String('x').is_reference_record())
        self.assertFalse(String('x').test_reference_record())
        # is_rank
        self.assertTrue(Preferred.is_rank())
        self.assertTrue(Preferred.test_rank())
        self.assertFalse(String('x').is_rank())
        self.assertFalse(String('x').test_rank())
        # is_preferred_rank
        self.assertTrue(Preferred.is_preferred_rank())
        self.assertTrue(Preferred.test_preferred_rank())
        self.assertFalse(Normal.is_preferred_rank())
        self.assertFalse(Normal.test_preferred_rank())
        # is_normal_rank
        self.assertTrue(Normal.is_normal_rank())
        self.assertTrue(Normal.test_normal_rank())
        self.assertFalse(Preferred.is_normal_rank())
        self.assertFalse(Preferred.test_normal_rank())
        # is_deprecated_rank
        self.assertTrue(Deprecated.is_deprecated_rank())
        self.assertTrue(Deprecated.test_deprecated_rank())
        self.assertFalse(Preferred.is_deprecated_rank())
        self.assertFalse(Preferred.test_deprecated_rank())
        # is_statement
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertTrue(stmt.is_statement())
        self.assertTrue(stmt.test_statement())
        self.assertFalse(String('x').is_statement())
        self.assertFalse(String('x').test_statement())

    def test_check(self):
        # check_kif_object
        self.assertEqual(Item('x').check_kif_object(), Item('x'))
        # check_value
        self.assertEqual(Item('x').check_value(), Item('x'))
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertRaises(TypeError, stmt.check_value)
        # check_entity
        self.assertEqual(Item('x').check_entity(), Item('x'))
        self.assertRaises(TypeError, String('x').check_entity)
        # check_item
        self.assertEqual(Item('x').check_item(), Item('x'))
        self.assertRaises(TypeError, String('x').check_item)
        # check_property
        self.assertEqual(Property('x').check_property(), Property('x'))
        self.assertRaises(TypeError, Item('x').check_property)
        # check_data_value
        self.assertEqual(IRI('x').check_data_value(), IRI('x'))
        self.assertRaises(TypeError, Item('x').check_data_value)
        # check_string
        self.assertEqual(String('x').check_string(), String('x'))
        self.assertRaises(TypeError, Item('x').check_string)
        # check_iri
        self.assertEqual(IRI('x').check_iri(), IRI('x'))
        self.assertRaises(TypeError, Item('x').check_iri)
        # check_deep_data_value
        self.assertEqual(Quantity(0).check_deep_data_value(), Quantity(0))
        self.assertRaises(TypeError, String('x').check_deep_data_value)
        # check_quantity
        self.assertEqual(Quantity(0).check_quantity(), Quantity(0))
        self.assertRaises(TypeError, String('x').check_quantity)
        # check_time
        self.assertEqual(Time('2023-09-18').check_time(), Time('2023-09-18'))
        self.assertRaises(TypeError, String('2023-09-18').check_time)
        # check_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.check_snak(), snak)
        self.assertRaises(TypeError, String('x').check_snak)
        # check_value_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.check_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_value_snak)
        # check_some_value_snak
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.check_some_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_some_value_snak)
        # check_no_value_snak
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.check_no_value_snak(), snak)
        self.assertRaises(TypeError, String('x').check_no_value_snak)
        # check_reference_record
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertEqual(refr.check_reference_record(), refr)
        self.assertRaises(TypeError, String('x').check_reference_record)
        # check_rank
        self.assertEqual(Preferred.check_rank(), Preferred)
        self.assertRaises(TypeError, String('x').check_rank)
        # check_preferred_rank
        self.assertEqual(Preferred.check_preferred_rank(), Preferred)
        self.assertRaises(TypeError, Normal.check_preferred_rank)
        # check_normal_rank
        self.assertEqual(Normal.check_normal_rank(), Normal)
        self.assertRaises(TypeError, Preferred.check_normal_rank)
        # check_deprecated_rank
        self.assertEqual(Deprecated.check_deprecated_rank(), Deprecated)
        self.assertRaises(TypeError, Preferred.check_deprecated_rank)
        # check_statement
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(stmt.check_statement(), stmt)
        self.assertRaises(TypeError, String('x').check_statement)

    def test_unpack(self):
        # unpack_kif_object
        self.assertEqual(Item('x').unpack_kif_object(), (IRI('x'),))
        # unpack_value
        self.assertEqual(Item('x').unpack_value(), (IRI('x'),))
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertRaises(TypeError, stmt.unpack_value)
        # unpack_entity
        self.assertEqual(Item('x').unpack_entity(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_entity)
        # unpack_item
        self.assertEqual(Item('x').unpack_item(), (IRI('x'),))
        self.assertRaises(TypeError, String('x').unpack_item)
        # unpack_property
        self.assertEqual(Property('x').unpack_property(), (IRI('x'),))
        self.assertRaises(TypeError, Item('x').unpack_property)
        # unpack_data_value
        self.assertEqual(IRI('x').unpack_data_value(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_data_value)
        # unpack_string
        self.assertEqual(String('x').unpack_string(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_string)
        # unpack_iri
        self.assertEqual(IRI('x').unpack_iri(), ('x',))
        self.assertRaises(TypeError, Item('x').unpack_iri)
        # unpack_deep_data_value
        self.assertEqual(
            Quantity(0).unpack_deep_data_value(), (0, None, None, None))
        self.assertRaises(TypeError, String('x').unpack_deep_data_value)
        # unpack_quantity
        self.assertEqual(Quantity(0).unpack_quantity(),
                         (Decimal('0'), None, None, None))
        self.assertRaises(TypeError, String('x').unpack_quantity)
        # unpack_time
        self.assertEqual(
            Time('2023-09-18').unpack_time(),
            (Datetime(2023, 9, 18, tzinfo=UTC), None, None, None))
        self.assertRaises(TypeError, String('2023-09-18').unpack_time)
        # unpack_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.unpack_snak(), (Property('x'), Item('y')))
        self.assertRaises(TypeError, String('x').unpack_snak)
        # unpack_value_snak
        snak = ValueSnak(Property('x'), Item('y'))
        self.assertEqual(snak.unpack_value_snak(), (Property('x'), Item('y')))
        self.assertRaises(TypeError, String('x').unpack_value_snak)
        # unpack_some_value_snak
        snak = SomeValueSnak(Property('x'))
        self.assertEqual(snak.unpack_some_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_some_value_snak)
        # unpack_no_value_snak
        snak = NoValueSnak(Property('x'))
        self.assertEqual(snak.unpack_no_value_snak(), (Property('x'),))
        self.assertRaises(TypeError, String('x').unpack_no_value_snak)
        # unpack_reference_record
        refr = ReferenceRecord(NoValueSnak(Property('p')))
        self.assertEqual(
            refr.unpack_reference_record(), (NoValueSnak(Property('p')),))
        self.assertRaises(TypeError, String('x').unpack_reference_record)
        # unpack_rank
        self.assertEqual(Preferred.unpack_rank(), ())
        self.assertRaises(TypeError, String('x').unpack_rank)
        # unpack_preferred_rank
        self.assertEqual(Preferred.unpack_preferred_rank(), ())
        self.assertRaises(TypeError, Normal.unpack_preferred_rank)
        # unpack_normal_rank
        self.assertEqual(Normal.unpack_normal_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_normal_rank)
        # unpack_deprecated_rank
        self.assertEqual(Deprecated.unpack_deprecated_rank(), ())
        self.assertRaises(TypeError, Preferred.unpack_deprecated_rank)
        # unpack_statement
        stmt = Statement(Item('x'), NoValueSnak(Property('y')))
        self.assertEqual(
            stmt.unpack_statement(),
            (Item('x'), NoValueSnak(Property('y'))))
        self.assertRaises(TypeError, String('x').unpack_statement)


if __name__ == '__main__':
    main()
