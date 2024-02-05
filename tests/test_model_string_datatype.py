# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import String, StringDatatype

from .tests import kif_TestCase, main


class TestModelStringDatatype(kif_TestCase):

    def test_value_class(self):
        self.assert_datatype_value_class(StringDatatype, String, 'string')

    def test__from_rdflib(self):
        self.assert_string_datatype(
            StringDatatype._from_rdflib(NS.WIKIBASE.String))

    def test__to_rdflib(self):
        self.assertEqual(
            StringDatatype._to_rdflib(), NS.WIKIBASE.String)


if __name__ == '__main__':
    main()
