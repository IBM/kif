# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Preferred, PreferredRank, Rank

from .tests import kif_TestCase, main


class TestModelPreferredRank(kif_TestCase):

    def test__init__(self):
        self.assert_preferred_rank(PreferredRank())
        self.assert_preferred_rank(Preferred)
        self.assertIs(Rank.preferred, Preferred)

    def test__from_rdflib(self):
        self.assertRaises(ValueError, Rank._from_rdflib, NS.WIKIBASE.Url)
        self.assert_preferred_rank(
            Rank._from_rdflib(NS.WIKIBASE.PreferredRank))

    def test__to_rdflib(self):
        self.assertEqual(
            PreferredRank._to_rdflib(), NS.WIKIBASE.PreferredRank)


if __name__ == '__main__':
    main()
