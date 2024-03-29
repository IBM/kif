# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Deprecated, DeprecatedRank, Rank
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelRankDeprecatedRank(kif_TestCase):

    def test__init__(self):
        self.assert_deprecated_rank(DeprecatedRank())
        self.assert_deprecated_rank(Deprecated)
        self.assertIs(Rank.deprecated, Deprecated)

    def test__from_rdflib(self):
        self.assertRaises(ValueError, Rank._from_rdflib, WIKIBASE.Url)
        self.assert_deprecated_rank(Rank._from_rdflib(WIKIBASE.DeprecatedRank))

    def test__to_rdflib(self):
        self.assertEqual(DeprecatedRank._to_rdflib(), WIKIBASE.DeprecatedRank)


if __name__ == '__main__':
    TestModelRankDeprecatedRank.main()
