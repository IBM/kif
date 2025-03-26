# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Graph, Normal, Preferred, Store
from kif_lib.vocabulary import wd

from ..tests import TestCase


class Test(TestCase):

    def assert_to_rdf(self, input: Graph) -> None:
        output = Graph(*Store('rdf', data=input.to_rdf()).filter_annotated())
        self.assertEqual(output, input)

    def test_to_rdf(self):
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


if __name__ == '__main__':
    Test.main()
