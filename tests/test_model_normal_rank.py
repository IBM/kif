# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Normal, NormalRank, Rank

from .tests import kif_TestCase, main


class TestModelNormalRank(kif_TestCase):

    def test__init__(self):
        self.assert_normal_rank(NormalRank())
        self.assert_normal_rank(Normal)
        self.assertIs(Rank.normal, Normal)

    def test__from_rdflib(self):
        self.assertRaises(ValueError, Rank._from_rdflib, NS.WIKIBASE.Url)
        self.assert_normal_rank(Rank._from_rdflib(NS.WIKIBASE.NormalRank))

    def test__to_rdflib(self):
        self.assertEqual(NormalRank._to_rdflib(), NS.WIKIBASE.NormalRank)


if __name__ == '__main__':
    main()
