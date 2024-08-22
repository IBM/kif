# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Deprecated,
    DeprecatedRank,
    Item,
    Normal,
    NormalRank,
    Preferred,
    PreferredRank,
    Rank,
    SnakSet,
)
from kif_lib.namespace import WIKIBASE
from kif_lib.typing import assert_type, cast

from ....tests import KIF_ObjectTestCase


class Test(KIF_ObjectTestCase):

    def test_check(self) -> None:
        assert_type(Rank.check(NormalRank()), Rank)
        self._test_check(
            Rank,
            success=[
                (Deprecated, DeprecatedRank()),
                (DeprecatedRank(), Deprecated),
                (Normal, NormalRank()),
                (NormalRank(), Normal),
                (Preferred, PreferredRank()),
                (PreferredRank(), Preferred),
            ],
            failure=[0, {}, Item('x'), SnakSet()])

    def test__init__(self) -> None:
        self.assert_abstract_class(Rank)

    def test__from_rdflib(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'uri', 'cannot coerce URIRef into Rank',
            Rank._from_rdflib, WIKIBASE.Url)
        self.assert_raises_bad_argument(
            TypeError, 1, 'uri',
            'cannot coerce NormalRank into DeprecatedRank',
            DeprecatedRank._from_rdflib, WIKIBASE.NormalRank)
        self.assert_deprecated_rank(
            cast(DeprecatedRank, Rank._from_rdflib(WIKIBASE.DeprecatedRank)))
        self.assert_deprecated_rank(
            cast(DeprecatedRank, DeprecatedRank._from_rdflib(
                WIKIBASE.DeprecatedRank)))
        self.assert_normal_rank(
            cast(NormalRank, NormalRank._from_rdflib(WIKIBASE.NormalRank)))
        self.assert_preferred_rank(
            cast(PreferredRank, PreferredRank._from_rdflib(
                WIKIBASE.PreferredRank)))

    def test__to_rdflib(self) -> None:
        self.assertEqual(Deprecated._to_rdflib(), WIKIBASE.DeprecatedRank)
        self.assertEqual(Normal._to_rdflib(), WIKIBASE.NormalRank)
        self.assertEqual(Preferred._to_rdflib(), WIKIBASE.PreferredRank)


if __name__ == '__main__':
    Test.main()
