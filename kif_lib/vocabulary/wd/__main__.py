# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import httpx

from ... import namespace as NS
from ...compiler.sparql.builder import SelectQuery
from ...compiler.sparql.substitution import Substitution
from ...model import (
    Datatype,
    Entity,
    IRI,
    Item,
    ItemTemplate,
    Property,
    PropertyTemplate,
    Template,
    Variable,
)
from ...store.wikidata import WikidataStore
from ...typing import Callable, Iterator, Optional, TextIO
from .registry import WikidataEntityRegistry as Registry

#: Wikidata SPARQL endpoint to use (`None` means the official endpoint).
WIKIDATA: Optional[str] = None

#: Page-size to use.
PAGE_SIZE: int = 30000


def download_properties_tsv(append: Optional[bool] = None):
    def write(fp: TextIO, data: tuple[Entity, str]):
        prop, label = data
        assert isinstance(prop, Property)
        uri = prop.iri.content
        assert prop.range is not None
        datatype_uri = str(prop.range._to_rdflib())
        fp.write(f'{uri}\t{datatype_uri}\t{label}\n')
    _download_helper(
        Registry.WIKIDATA_PROPERTIES_TSV,
        _generate_properties_query, write, append)


def download_items_tsv(*types: str, append: Optional[bool] = None):
    def write(fp: TextIO, data: tuple[Entity, str]):
        item, label = data
        assert isinstance(item, Item)
        fp.write(f'{item.iri.content}\t{label}\n')
    _download_helper(
        Registry.WIKIDATA_ITEMS_TSV,
        lambda: _generate_items_query(*types), write, append)


def _download_helper(
        tsv: str,
        gen_fn: Callable[[], tuple[SelectQuery, Template, Substitution]],
        write_fn: Callable[[TextIO, tuple[Entity, str]], None],
        append: Optional[bool] = None
):
    registry_dir = Registry._get_registry_dir()
    path = registry_dir / tsv
    with open(path, 'a' if append else 'w', encoding='utf-8') as fp:
        for t in _iterate_query_results(gen_fn):
            write_fn(fp, t)
            fp.flush()


def _iterate_query_results(
        gen_fn: Callable[[], tuple[SelectQuery, Template, Substitution]],
        page_size: int = 30000,
        limit: Optional[int] = None
) -> Iterator[tuple[Entity, str]]:
    import json
    import logging
    import time
    q, tpl, subst = gen_fn()
    kb = WikidataStore('wikidata', iri=WIKIDATA)
    offset, page_count = 0, 0
    while True:
        page_count += 1
        dt = time.time()
        try:
            res = kb._eval_query_string(str(q.select(
                distinct=True, limit=page_size, offset=offset))).json()
        except httpx.HTTPStatusError:
            continue            # retry
        except json.decoder.JSONDecodeError:
            continue            # retry
        if not res['results']['bindings']:
            break
        bindings = res['results']['bindings']
        for binding in bindings:
            entity = tpl.instantiate(subst.instantiate(binding))
            assert isinstance(entity, Entity)
            if 'label' not in binding or 'value' not in binding['label']:
                continue        # skip
            label = binding['label']['value']
            assert isinstance(label, str)
            yield entity, label.strip()
        logging.info(
            'page %d\t[%.0fs since last page]',
            page_count, time.time() - dt)
        if len(bindings) < page_size:
            break
        offset += page_size


def _generate_items_query(
        *types: str
) -> tuple[SelectQuery, ItemTemplate, Substitution]:
    q = SelectQuery()
    v_item, v_label, v_type = q.vars('item', 'label', 'type')
    q.triples()(
        (v_item, NS.WIKIBASE.sitelinks, q.bnode()),
        (v_item, NS.RDFS.label, v_label))
    if types:
        q.triples()((v_item, NS.WDT['P31'], v_type))
        q.values(v_type)(*map(lambda t: (q.uri(NS.WD[t]),), types))
    q.filter(q.eq(q.lang(v_label), q.literal('en')))
    item_iri = Variable('item', IRI)
    item_tpl = ItemTemplate(item_iri)
    subst = Substitution()
    subst.add(item_iri, q.Variable(item_iri.name))
    return q, item_tpl, subst


def _generate_properties_query() -> tuple[
        SelectQuery, PropertyTemplate, Substitution]:
    q = SelectQuery()
    v_property, v_datatype, v_label = q.vars('property', 'datatype', 'label')
    q.triples()(
        (v_property, NS.RDF.type, NS.WIKIBASE.Property),
        (v_property, NS.WIKIBASE.propertyType, v_datatype),
        (v_property, NS.RDFS.label, v_label))
    q.filter(q.eq(q.lang(v_label), q.literal('en')))
    prop_iri = Variable('property', IRI)
    prop_range = Variable('range', Datatype)
    prop_tpl = PropertyTemplate(prop_iri, prop_range)
    subst = Substitution()
    subst.add(prop_iri, q.Variable(prop_iri.name))
    subst.add(Variable('datatype', IRI), q.Variable('datatype'))
    subst.add(prop_range, Variable('datatype', IRI))
    return q, prop_tpl, subst


def _get_default_item_types() -> list[str]:
    return [
        'Q125824188',           # ecosystem type
        'Q223662',              # SI base unit
        'Q28640',               # profession
        'Q34770',               # language
        'Q39367',               # dog breed
        'Q4022',                # river
        'Q4830453',             # business
        'Q5',                   # human
        'Q515',                 # city
        'Q6256',                # country
        'Q8502',                # mountain
    ]


def main():
    import argparse
    import logging
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--append', action='store_true',
        help='open output files in append mode')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='enable debugging')
    parser.add_argument(
        '-P', '--download-properties', action='store_true',
        help=f'download {Registry.WIKIDATA_PROPERTIES_TSV}')
    parser.add_argument(
        '-Q', '--download-items', action='store_true',
        help=f'download {Registry.WIKIDATA_ITEMS_TSV}')
    parser.add_argument(
        '-s', '--page-size', metavar='N', type=int,
        help='page-size to use')
    parser.add_argument(
        '-t', '--type', metavar='TYPE', action='append', default=[],
        help='item type to consider')
    parser.add_argument(
        '-T', '--default-types', action='store_true',
        help='consider the default item types')
    parser.add_argument(
        '-w', '--wikidata', metavar='URL', type=str,
        help='Wikidata SPARQL endpoint to use')
    args = parser.parse_args()
    if args.page_size:
        global PAGE_SIZE
        PAGE_SIZE = args.page_size
    if args.wikidata:
        global WIKIDATA
        WIKIDATA = args.wikidata
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    noop = True
    if args.download_properties:
        download_properties_tsv(append=args.append)
        noop = False
    if args.download_items:
        types = list(args.type)
        if args.default_types:
            types += _get_default_item_types()
        download_items_tsv(*types, append=args.append)
        noop = False
    if noop:
        print('Nothing to do.')
        print('Try --help for more information.')
    sys.exit(0)


if __name__ == '__main__':
    main()
