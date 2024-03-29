# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, String, StringDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueStringDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_string_datatype(
            StringDatatype._from_rdflib(WIKIBASE.String))

    def test__to_rdflib(self):
        self.assertEqual(StringDatatype._to_rdflib(), WIKIBASE.String)

    def test_from_value_class(self):
        self.assert_string_datatype(Datatype.from_value_class(String))

    def test_to_value_class(self):
        self.assertIs(StringDatatype().to_value_class(), String)


if __name__ == '__main__':
    TestModelValueStringDatatype.main()
