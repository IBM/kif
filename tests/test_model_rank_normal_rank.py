# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Normal, NormalRank, Rank
from kif_lib.namespace import WIKIBASE
from kif_lib.typing import cast

from .tests import kif_TestCase


class TestModelRankNormalRank(kif_TestCase):

    def test__init__(self):
        self.assert_normal_rank(NormalRank())
        self.assert_normal_rank(Normal)
        self.assertIs(Rank.normal, Normal)

    def test__from_rdflib(self):
        self.assertRaises(ValueError, Rank._from_rdflib, WIKIBASE.Url)
        self.assert_normal_rank(
            cast(NormalRank, Rank._from_rdflib(WIKIBASE.NormalRank)))

    def test__to_rdflib(self):
        self.assertEqual(NormalRank._to_rdflib(), WIKIBASE.NormalRank)


if __name__ == '__main__':
    TestModelRankNormalRank.main()
