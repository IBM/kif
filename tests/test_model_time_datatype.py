# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, Time, TimeDatatype

from .tests import kif_TestCase, main


class TestModelTimeDatatype(kif_TestCase):

    def test_sanity(self):
        self.assertIs(Datatype.time, Time.datatype)
        self.assertEqual(Datatype.time, TimeDatatype())

    def test__from_rdflib(self):
        self.assert_time_datatype(TimeDatatype._from_rdflib(NS.WIKIBASE.Time))

    def test__to_rdflib(self):
        self.assertEqual(TimeDatatype._to_rdflib(), NS.WIKIBASE.Time)


if __name__ == '__main__':
    main()
