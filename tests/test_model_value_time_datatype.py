# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, Time, TimeDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueTimeDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_time_datatype(TimeDatatype._from_rdflib(WIKIBASE.Time))

    def test__to_rdflib(self):
        self.assertEqual(TimeDatatype._to_rdflib(), WIKIBASE.Time)

    def test_from_value_class(self):
        self.assert_time_datatype(Datatype.from_value_class(Time))


if __name__ == '__main__':
    TestModelValueTimeDatatype.main()
