# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, Entity, IRI
from kif_lib.error import MustBeImplementedInSubclass

from .tests import kif_TestCase, main


class TestDatatype(kif_TestCase):

    def test__preprocess_arg_datatype(self):
        self.assertRaises(TypeError, Datatype._preprocess_arg_datatype, 0, 1)
        self.assertRaises(
            ValueError, Datatype._preprocess_arg_datatype, 'x', 1)
        self.assertEqual(
            Datatype._preprocess_arg_datatype(Datatype.item, 1), Datatype.item)
        self.assertEqual(
            Datatype._preprocess_arg_datatype(Datatype.item._uri, 1),
            Datatype.item)
        self.assertEqual(
            Datatype._preprocess_arg_datatype(str(Datatype.item._uri), 1),
            Datatype.item)
        self.assertEqual(
            Datatype._preprocess_arg_datatype(IRI(Datatype.item._uri), 1),
            Datatype.item)

    def test_aliases(self):
        self.assert_item_datatype(Datatype.item)
        self.assert_property_datatype(Datatype.property)
        self.assert_lexeme_datatype(Datatype.lexeme)
        self.assert_iri_datatype(Datatype.iri)
        self.assert_text_datatype(Datatype.text)
        self.assert_string_datatype(Datatype.string)
        self.assert_external_id_datatype(Datatype.external_id)
        self.assert_quantity_datatype(Datatype.quantity)
        self.assert_time_datatype(Datatype.time)

    def test_from_value_class(self):
        self.assertRaisesRegex(
            TypeError, r'\(expected type, got int\)',
            Datatype.from_value_class, 0)
        self.assertRaisesRegex(
            TypeError, r'\(expected subclass of Value, got int\)',
            Datatype.from_value_class, int)
        self.assertRaisesRegex(
            ValueError, r'\(no datatype for Entity\)',
            Datatype.from_value_class, Entity)

    def test_to_value_class(self):
        self.assertRaises(
            MustBeImplementedInSubclass, Datatype.to_value_class)


if __name__ == '__main__':
    main()
