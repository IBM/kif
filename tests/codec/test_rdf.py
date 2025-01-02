# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DeprecatedRank,
    ExternalIdDatatype,
    Filter,
    Graph,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    ItemDescriptor,
    KIF_Object,
    LexemeDatatype,
    Normal,
    NormalRank,
    NoValueSnak,
    Preferred,
    PreferredRank,
    Property,
    PropertyDatatype,
    Quantity,
    QuantityDatatype,
    ReferenceRecord,
    SnakSet,
    SomeValueSnak,
    Store,
    String,
    StringDatatype,
    Text,
    TextDatatype,
    Time,
    TimeDatatype,
    ValueSnak,
)
from kif_lib.typing import cast
from kif_lib.vocabulary import wd

from ..tests import TestCase


class Test(TestCase):

    def assert_to_rdf(self, input: Graph, output: Graph) -> None:
        it = Store('rdf', data=input.to_rdf()).filter_annotated()
        self.assertEqual(Graph(*it).args, output.args)

    def test_to_rdf(self):
        # TODO: Check some-value and no-value in qualifiers & references.
        # TODO: Check lexeme and related pseudo-properties.
        self.assert_to_rdf(
            Graph(
                wd.mass(wd.benzene, 0),
                wd.label(wd.benzene, Text('benzene', 'en')),
                wd.density(
                    wd.benzene, '0.88'@wd.gram_per_cubic_centimetre,
                    qualifiers=[
                        wd.phase_of_matter(wd.liquid),
                        wd.alias('xxx'),
                    ],
                    references=[
                        [wd.stated_in(wd.PubChem),
                         wd.reference_URL('http://...')],
                        [wd.stated_in(wd.Wikidata),
                         wd.description('xxx')],
                    ],
                    rank=Preferred,
                ),
            ),
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
                ),
            ))


if __name__ == '__main__':
    Test.main()
