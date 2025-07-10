# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy

from kif_lib import Context, Filter, Graph, Item
from kif_lib import namespace as NS
from kif_lib import Normal, Preferred, Property, Store
from kif_lib.model import EncoderError
from kif_lib.rdflib import split_uri
from kif_lib.typing import Any
from kif_lib.vocabulary import pc, wd

from ..tests import TestCase


class Test(TestCase):

    def assert_to_rdf(self, input: Graph, **kwargs: Any) -> None:
        output = Graph(*Store('rdf', data=input.to_rdf(
            **kwargs)).filter_annotated())
        self.assertEqual(output, Graph(*map(lambda s: s.annotate(), input)))

    def assert_to_rdf_schema(
            self,
            input: Graph,
            input_schema: Property.TSchema,
            *args: Property,
            **kwargs: Any,
    ) -> None:
        schema = Property._check_schema(input_schema)
        kb = Store('rdf', data=input.to_rdf(**kwargs))
        for prop in args:
            p = schema['p'].content + split_uri(prop.iri.content)[1]
            status = kb._sources[0].backend._ask(  # type: ignore
                f'ASK {{_:b <{p}> ?wds. ?wds <{NS.WIKIBASE.rank}> _:b2}}')
            self.assertTrue(status['boolean'])

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

    def test_define(self) -> None:
        lines = list(wd.mass(wd.benzene, 0).to_rdf().splitlines())
        with Context() as ctx:
            ctx.options.codec.rdf.encoder.set_define(
                Filter.ENTITY & ~Filter.PROPERTY)
            self.assertEqual(
                list(wd.mass(wd.benzene, 0).to_rdf().splitlines()),
                [s for s in lines if not s.startswith(wd.mass.n3())])

    def test_schema(self) -> None:
        stmt = pc.isotope_atom_count(pc.CID(241), 0)
        self.assertRaises(TypeError, stmt.to_rdf, schema=0)
        self.assertRaises(ValueError, stmt.to_rdf, schema={})
        with Context() as ctx:
            ctx.options.codec.rdf.encoder.schema = None
            self.assertRaises(EncoderError, stmt.to_rdf)
        with Context() as ctx:
            if ctx.options.codec.rdf.encoder.DEFAULT_SCHEMA is not None:
                self.assert_to_rdf_schema(
                    Graph(stmt),
                    ctx.options.codec.rdf.encoder.DEFAULT_SCHEMA,
                    pc.isotope_atom_count)
            schema: Property._TSchema = {
                'p': 'http://p/',
                'pq': 'http://pq/',
                'pqv': 'http://pqv/',
                'pr': 'http://pr/',
                'prv': 'http://prv/',
                'ps': 'http://ps/',
                'psv': 'http://psv/',
                'wdno': 'http://wdno/',
                'wdt': 'http://wdno/',
            }
            ctx.options.codec.rdf.encoder.set_schema(schema)
            self.assert_to_rdf_schema(
                Graph(stmt), schema, pc.isotope_atom_count)
            schema1 = copy.copy(schema)
            schema1['p'] = 'http://p1'
            self.assert_to_rdf_schema(
                Graph(stmt), schema1, pc.isotope_atom_count, schema=schema1)
        self.assert_to_rdf(Graph(
            Property('http://x')(Item('http://y'), Item('http://z'))))

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
