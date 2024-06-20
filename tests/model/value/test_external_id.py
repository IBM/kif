# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    IRI,
    String,
)
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import assert_type

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_datatype_class(self) -> None:
        assert_type(ExternalId.datatype_class, type[ExternalIdDatatype])

    def test_datatype(self) -> None:
        assert_type(ExternalId.datatype, ExternalIdDatatype)
        self.assertIsInstance(ExternalId.datatype, ExternalIdDatatype)

    def test_template_class(self) -> None:
        assert_type(ExternalId.template_class, type[ExternalIdTemplate])

    def test_variable_class(self) -> None:
        assert_type(ExternalId.variable_class, type[ExternalIdVariable])

    def test_check(self) -> None:
        self.assert_raises_check_error(ExternalId, 0, ExternalId.check)
        self.assert_raises_check_error(ExternalId, {}, ExternalId.check)
        self.assert_raises_check_error(ExternalId, IRI('x'), ExternalId.check)
        # success
        assert_type(ExternalId.check(ExternalId('x')), ExternalId)
        self.assertEqual(ExternalId.check(ExternalId('x')), ExternalId('x'))
        self.assertEqual(ExternalId.check(String('x')), ExternalId('x'))
        self.assertEqual(ExternalId.check(URIRef('x')), ExternalId('x'))
        self.assertEqual(ExternalId.check(Literal('x')), ExternalId('x'))
        self.assertEqual(ExternalId.check('x'), ExternalId('x'))

    def test__init__(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got int', ExternalId, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got dict', ExternalId, {})
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected str, got IRI', ExternalId, IRI('x'))
        # success
        assert_type(ExternalId('x'), ExternalId)
        self.assert_external_id(ExternalId(ExternalId('x')), 'x')
        self.assert_external_id(ExternalId(String('x')), 'x')
        self.assert_external_id(ExternalId('x'), 'x')
        self.assert_external_id(ExternalId('x'), 'x')
        self.assert_external_id(ExternalId(URIRef('x')), 'x')
        self.assert_external_id(ExternalId(Literal('x')), 'x')
        self.assert_external_id(ExternalId('x'), 'x')


if __name__ == '__main__':
    Test.main()
