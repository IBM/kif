# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    String,
    Text,
    TextDatatype,
    TextTemplate,
    TextVariable,
)
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_datatype_class(self) -> None:
        assert_type(Text.datatype_class, type[TextDatatype])

    def test_datatype(self) -> None:
        assert_type(Text.datatype, TextDatatype)
        self.assertIsInstance(Text.datatype, TextDatatype)

    def test_template_class(self) -> None:
        assert_type(Text.template_class, type[TextTemplate])

    def test_variable_class(self) -> None:
        assert_type(Text.variable_class, type[TextVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(Text, 0, Text.check)
        self.assert_raises_check_error(Text, {}, Text.check)
        # success
        assert_type(Text.check(Text('x')), Text)
        self.assertEqual(Text.check(Text('x')), Text('x'))
        self.assertEqual(Text.check(Text('x')), Text('x'))
        self.assertEqual(Text.check(String('x')), Text('x'))
        self.assertEqual(Text.check(ExternalId('x')), Text('x'))
        self.assertEqual(Text.check(URIRef('x')), Text('x'))
        self.assertEqual(Text.check(Literal('x')), Text('x'))
        self.assertEqual(Text.check('x'), Text('x'))

    def test__init__(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into String',
            Text, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce dict into String',
            Text, {})
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce int into String',
            Text, 'x', 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce dict into String',
            Text, 'x', {})
        self.assert_raises_bad_argument(
            TypeError, 2, None, 'cannot coerce Text into String',
            Text, 'x', Text('y'))
        # success
        assert_type(Text('x'), Text)
        self.assert_text(Text(Text('x')), 'x')
        self.assert_text(Text(Text('x'), String('y')), 'x', 'y')
        self.assert_text(Text(String('x')), 'x')
        self.assert_text(Text(String('x'), ExternalId('y')), 'x', 'y')
        self.assert_text(Text(ExternalId('x')), 'x')
        self.assert_text(Text(ExternalId('x'), URIRef('y')), 'x', 'y')
        self.assert_text(Text(URIRef('x')), 'x')
        self.assert_text(Text(URIRef('x'), Literal('y')), 'x', 'y')
        self.assert_text(Text(Literal('x')), 'x')
        self.assert_text(Text(Literal('x'), 'y'), 'x', 'y')
        self.assert_text(Text('x', 'y'), 'x', 'y')


if __name__ == '__main__':
    Test.main()
