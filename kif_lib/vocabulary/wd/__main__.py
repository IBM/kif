# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import pathlib

import httpx

from ... import namespace as NS
from ...compiler.sparql.builder import SelectQuery
from ...compiler.sparql.substitution import Substitution
from ...model import (
    Datatype,
    Entity,
    IRI,
    ItemTemplate,
    PropertyTemplate,
    Template,
    Variable,
)
from ...store.wikidata import WikidataStore
from ...typing import Callable, Iterator, Optional
from .registry import WikidataEntityRegistry as Registry


def download_properties_tsv(append: Optional[bool] = False):
    registry_dir = Registry._get_registry_dir()
    write(registry_dir / Registry.WIKIDATA_PROPERTIES_TSV,
          iterate_query_results(generate_properties_query), append)


def download_items_tsv(append: Optional[bool] = False):
    registry_dir = Registry._get_registry_dir()
    write(registry_dir / Registry.WIKIDATA_ITEMS_TSV,
          iterate_query_results(generate_items_query), append)


def write(
        path: pathlib.Path,
        input: Iterator[tuple[Entity, Optional[str]]],
        append: Optional[bool] = False
):
    count, seen = 0, set()
    with open(path, 'a' if append else 'w', encoding='utf-8') as fp:
        for entity, label in input:
            if label is None or entity in seen:
                continue
            seen.add(entity)
            i = int(NS.Wikidata.get_wikidata_name(entity.iri.content)[1:])
            fp.write(f'{i}\t{label.strip()}\t{entity}\n')
            fp.flush()
            count += 1
    print(f'Wrote {count} entries to {path}')


def iterate_query_results(
        gen_fn: Callable[[], tuple[SelectQuery, Template, Substitution]],
        page_size: int = 15000,
        limit: Optional[int] = None
) -> Iterator[tuple[Entity, Optional[str]]]:
    import json
    q, tpl, subst = gen_fn()
    kb = WikidataStore('wikidata')
    offset = 0
    while True:
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
            if 'label' in binding and 'value' in binding['label']:
                label: Optional[str] = binding['label']['value']
            else:
                label = None
            yield entity, label
        if len(bindings) < page_size:
            break
        offset += page_size


def generate_items_query() -> tuple[SelectQuery, ItemTemplate, Substitution]:
    q = SelectQuery()
    v_item, v_label = q.vars('item', 'label')
    q.triples()(
        (v_item, NS.WIKIBASE.sitelinks, q.bnode()),
        (v_item, NS.RDFS.label, v_label))
    with q.filter_not_exists():  # exclude scholarly articles
        q.triples()((v_item, NS.WDT['P31'], NS.WD['Q13442814']))
    q.filter(q.eq(q.lang(v_label), q.literal('en')))
    item_iri = Variable('item', IRI)
    item_tpl = ItemTemplate(item_iri)
    subst = Substitution()
    subst.add(item_iri, q.Variable(item_iri.name))
    return q, item_tpl, subst


def generate_properties_query() -> tuple[
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
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    noop = True
    if args.download_properties:
        download_properties_tsv(append=args.append)
        noop = False
    if args.download_items:
        download_items_tsv(append=args.append)
        noop = False
    if noop:
        print('Nothing to do.')
        print('Try --help for more information.')
    sys.exit(0)


if __name__ == '__main__':
    main()
