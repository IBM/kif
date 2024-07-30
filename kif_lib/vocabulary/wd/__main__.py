# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...compiler.sparql.builder import SelectQuery
from ...compiler.sparql.substitution import Substitution
from ...model import Datatype, IRI, Property, PropertyTemplate, Variable
from ...store.wikidata import WikidataStore
from ...typing import Iterator, Optional
from .registry import WikidataEntityRegistry


def iterate_properties() -> Iterator[
        tuple[Property, Optional[str], Optional[str]]]:
    kb = WikidataStore('wikidata')
    q = SelectQuery()
    v_property, v_datatype, v_label, v_description = q.vars(
        'property', 'datatype', 'label', 'description')
    q.triples()(
        (v_property, NS.RDF.type, NS.WIKIBASE.Property),
        (v_property, NS.WIKIBASE.propertyType, v_datatype),
        (v_property, NS.RDFS.label, v_label),
        (v_property, NS.SCHEMA.description, v_description))
    q.filter(q.eq(q.lang(v_label), q.literal('en')))
    q.filter(q.eq(q.lang(v_description), q.literal('en')))
    res = kb._eval_query_string(str(
        q.select(distinct=True))).json()
    prop_iri = Variable('property', IRI)
    prop_range = Variable('range', Datatype)
    prop = PropertyTemplate(prop_iri, prop_range)
    subst = Substitution()
    subst.add(prop_iri, q.Variable(prop_iri.name))
    subst.add(Variable('datatype', IRI), q.Variable('datatype'))
    subst.add(prop_range, Variable('datatype', IRI))
    for binding in res['results']['bindings']:
        property = prop.instantiate(subst.instantiate(binding))
        assert isinstance(property, Property)
        if 'label' in binding and 'value' in binding['label']:
            label: Optional[str] = binding['label']['value']
        else:
            label = None
        if 'description' in binding and 'value' in binding['description']:
            description: Optional[str] = binding['description']['value']
        else:
            description = None
        yield property, label, description


def main():
    import json
    import logging
    logging.basicConfig(level=logging.INFO)

    def it():
        for prop, label, desc in iterate_properties():
            assert prop.range is not None
            yield prop.iri.content, {
                'object': prop.to_ast(),
                'datatype': prop.range._to_rdflib(),
                'label': label,
                'description': desc,
            }
    path = WikidataEntityRegistry._get_wikidata_json_path(
        WikidataEntityRegistry._wikidata_properties_json)
    props = dict(it())
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(props, fp, indent=2)
    print(f'Wrote {len(props)} properties to {path}.')


if __name__ == '__main__':
    main()
