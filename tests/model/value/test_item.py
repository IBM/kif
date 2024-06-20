# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    ItemDatatype,
    ItemTemplate,
    ItemVariable,
    Property,
    String,
)
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_datatype_class(self) -> None:
        assert_type(Item.datatype_class, type[ItemDatatype])

    def test_datatype(self) -> None:
        assert_type(Item.datatype, ItemDatatype)
        self.assertIsInstance(Item.datatype, ItemDatatype)

    def test_template_class(self) -> None:
        assert_type(Item.template_class, type[ItemTemplate])

    def test_variable_class(self) -> None:
        assert_type(Item.variable_class, type[ItemVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(IRI, 0, Item.check)
        self.assert_raises_check_error(IRI, {}, Item.check)
        self.assert_raises_check_error(IRI, Property('x'), Item.check)
        # success
        assert_type(Item.check(Item('x')), Item)
        self.assertEqual(Item.check(Item('x')), Item('x'))
        self.assertEqual(Item.check(IRI('x')), Item('x'))
        self.assertEqual(Item.check(String('x')), Item('x'))
        self.assertEqual(Item.check(ExternalId('x')), Item('x'))
        self.assertEqual(Item.check(URIRef('x')), Item('x'))
        self.assertEqual(Item.check(Literal('x')), Item('x'))
        self.assertEqual(Item.check('x'), Item('x'))

    def test__init__(self) -> None:
        self.assert_raises_check_error(String, 0, IRI, None, 1)
        self.assert_raises_check_error(String, {}, IRI, None, 1)
        # success
        assert_type(Item('x'), Item)
        self.assert_item(Item(Item('x')), IRI('x'))
        self.assert_item(Item(String('x')), IRI('x'))
        self.assert_item(Item(ExternalId('x')), IRI('x'))
        self.assert_item(Item(URIRef('x')), IRI('x'))
        self.assert_item(Item(Literal('x')), IRI('x'))
        self.assert_item(Item('x'), IRI('x'))


if __name__ == '__main__':
    Test.main()
