# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Graph
from kif_lib import namespace as NS
from kif_lib import Normal, Preferred, Store
from kif_lib.vocabulary import wd

from ..tests import TestCase


class Test(TestCase):

    def assert_to_rdf(self, input: Graph) -> None:
        output = Graph(*Store('rdf', data=input.to_rdf()).filter_annotated())
        self.assertEqual(output, input)

    def test_to_rdf(self) -> None:
        # TODO: Check some-value and no-value in qualifiers & references.
        # TODO: Check lexeme and related pseudo-properties.
        self.assert_to_rdf(
            Graph(
                wd.mass(wd.benzene, 0, rank=Normal),
                wd.density(
                    wd.benzene, '0.88'@wd.gram_per_cubic_centimetre,
                    qualifiers=[
                        wd.phase_of_matter(wd.liquid),
                    ],
                    references=[
                        [wd.stated_in(wd.PubChem),
                         wd.reference_URL('http://...')],
                        [wd.stated_in(wd.Wikidata)],
                    ],
                    rank=Preferred,
                )
            ))

    def test_gen_wdref(self) -> None:
        stmt = wd.mass(
            wd.benzene, 76, references=[[wd.stated_in(wd.Wikidata)]])
        kb = Store('rdf', data=stmt.to_rdf(gen_wdref=lambda x: '0'))
        res = kb._sources[0].backend._select(  # type: ignore
            f'SELECT ?wdref {{_:b <{NS.PROV.wasDerivedFrom}> ?wdref}} LIMIT 1')
        self.assertEqual(
            res['results']['bindings'][0]['wdref']['value'],
            str(NS.WDREF['0']))

    def test_gen_wds(self) -> None:
        stmt = wd.mass(wd.benzene, 76)
        kb = Store('rdf', data=stmt.to_rdf(gen_wds=lambda x: '0'))
        res = kb._sources[0].backend._select(  # type: ignore
            f'SELECT ?wds {{?wds <{NS.WIKIBASE.rank}> _:b}} LIMIT 1')
        self.assertEqual(
            res['results']['bindings'][0]['wds']['value'], str(NS.WDS['0']))

    def test_gen_wdv(self) -> None:
        stmt = wd.mass(wd.benzene, 76)
        kb = Store('rdf', data=stmt.to_rdf(gen_wdv=lambda x: '0'))
        res = kb._sources[0].backend._select(  # type: ignore
            f'SELECT ?wdv {{?wdv a <{NS.WIKIBASE.QuantityValue}>}} LIMIT 1')
        self.assertEqual(
            res['results']['bindings'][0]['wdv']['value'], str(NS.WDV['0']))


if __name__ == '__main__':
    Test.main()
