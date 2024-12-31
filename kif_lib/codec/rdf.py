# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .. import itertools
from ..model import (
    AnnotatedStatement,
    DeepDataValue,
    Entity,
    Graph,
    Item,
    KIF_Object,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    ReferenceRecord,
    ShallowDataValue,
    Snak,
    SomeValueSnak,
    Statement,
    Time,
    Value,
    ValueSnak,
)
from ..model.kif_object import Encoder, Object
from ..namespace import ONTOLEX, PROV, RDF, WIKIBASE, Wikidata
from ..rdflib import BNode, Literal, URIRef
from ..typing import cast, Iterator, override, TypeAlias, TypedDict

TSubject: TypeAlias = URIRef | BNode
TPredicate: TypeAlias = URIRef
TObject: TypeAlias = URIRef | BNode | Literal
TTriple: TypeAlias = tuple[TSubject, TPredicate, TObject]


class RDF_Encoder(
        Encoder,
        format='rdf',
        description='RDF encoder'
):
    """RDF encoder."""

    class PropertySchema(TypedDict):
        p: URIRef
        pq: URIRef
        pqv: URIRef
        pr: URIRef
        prv: URIRef
        ps: URIRef
        psv: URIRef
        wdno: URIRef
        wdt: URIRef

    __slots__ = (
        '_property_schema_table',
        '_seen_deep_data_value',
        '_seen_entity',
        '_seen_reference_record',
    )

    _property_schema_table: dict[Property, RDF_Encoder.PropertySchema]
    _seen_deep_data_value: dict[DeepDataValue, URIRef]
    _seen_entity: dict[Entity, URIRef]
    _seen_reference_record: dict[ReferenceRecord, URIRef]

    def __init__(
            self,
            schema: dict[Property, RDF_Encoder.PropertySchema] | None = None
    ) -> None:
        self._property_schema_table = {}
        for prop, t in (schema or {}).items():
            self._property_schema_table[prop] = cast(
                RDF_Encoder.PropertySchema,
                {k: URIRef(v) for k, v in t.items()})
        self._seen_deep_data_value = {}
        self._seen_entity = {}
        self._seen_reference_record = {}

    def _get_property_schema(
            self,
            property: Property
    ) -> RDF_Encoder.PropertySchema:
        if property in self._property_schema_table:
            return self._property_schema_table[property]
        if property.range is None:
            raise self._error(f'no datatype for property: {property}')
        assert property.range is not None
        try:
            name = Wikidata.get_wikidata_name(property.iri.content)
            schema: RDF_Encoder.PropertySchema = {
                'p': Wikidata.P[name],
                'pq': Wikidata.PQ[name],
                'pqv': Wikidata.PQV[name],
                'pr': Wikidata.PR[name],
                'prv': Wikidata.PRV[name],
                'ps': Wikidata.PS[name],
                'psv': Wikidata.PSV[name],
                'wdno': Wikidata.WDNO[name],
                'wdt': Wikidata.WDT[name],
            }
            self._property_schema_table[property] = schema
            return schema
        except ValueError as err:
            raise self._error(
                f'no schema for property: {property}') from err

    @override
    def iterencode(self, input: Object) -> Iterator[str]:
        if isinstance(input, Graph):
            for s in input:
                yield from self.iterencode(s)
        elif isinstance(input, Statement):
            if isinstance(input, AnnotatedStatement):
                stmt: AnnotatedStatement = input
            else:
                stmt = input.annotate()
            yield from self._iterencode_annotated_statement(stmt)
        else:
            raise self._error(f'cannot encode to RDF: {input}')

    def _iterencode_annotated_statement(
            self,
            stmt: AnnotatedStatement
    ) -> Iterator[str]:
        schema = self._get_property_schema(stmt.snak.property)
        wds = Wikidata.WDS[stmt.digest]
        # property definition
        yield from self._do_iterencode_property(stmt.snak.property, True)
        # subject
        yield from self._do_iterencode_entity(stmt.subject)
        subject = self._seen_entity[stmt.subject]
        assert subject
        yield from self._tr((subject, schema['p'], wds))
        # main snak
        if not isinstance(stmt.snak, NoValueSnak):
            if isinstance(stmt.snak, ValueSnak):
                truthy_value = stmt.snak.value._to_rdflib()
            else:
                truthy_value = Wikidata.WDGENID[stmt.snak.property.digest]
            yield from self._tr((subject, schema['wdt'], truthy_value))
        yield from self._do_iterencode_snak(
            stmt.snak, wds, schema['ps'], schema['psv'], schema['wdno'])
        # qualifiers
        for qsnak in stmt.qualifiers:
            qschema = self._get_property_schema(qsnak.property)
            yield from self._do_iterencode_snak(
                qsnak, wds, qschema['pq'], qschema['pqv'], qschema['wdno'])
        # references
        for ref in stmt.references:
            yield from self._do_iterencode_reference_record(ref)
            wdref = self._seen_reference_record[ref]
            yield from self._tr((wds, PROV.wasDerivedFrom, wdref))
        # rank
        yield from self._tr(
            (wds, RDF.type, WIKIBASE.BestRank),
            (wds, WIKIBASE.rank, stmt.rank._to_rdflib()))

    def _do_iterencode_snak(
            self,
            snak: Snak,
            wds: URIRef,
            ps: URIRef,
            psv: URIRef,
            wdno: URIRef
    ) -> Iterator[str]:
        yield from self._do_iterencode_property(snak.property, True)
        if isinstance(snak, ValueSnak):
            yield from self._do_iterencode_value(snak.value, wds, ps, psv)
        elif isinstance(snak, SomeValueSnak):
            yield from self._tr(
                (wds, ps, Wikidata.WDGENID[snak.property.digest]))
        elif isinstance(snak, NoValueSnak):
            yield from self._tr((wds, RDF.type, wdno))
        else:
            raise KIF_Object._should_not_get_here()

    def _do_iterencode_entity(self, entity: Entity) -> Iterator[str]:
        if isinstance(entity, Item):
            yield from self._do_iterencode_item(entity)
        elif isinstance(entity, Property):
            yield from self._do_iterencode_property(entity)
        elif isinstance(entity, Lexeme):
            yield from self._do_iterencode_lexeme(entity)
        else:
            raise KIF_Object._should_not_get_here()

    def _do_iterencode_item(self, item: Item) -> Iterator[str]:
        if item in self._seen_entity:
            yield ''
        else:
            uri = cast(URIRef, item._to_rdflib())
            self._seen_entity[item] = uri
            yield from self._tr((uri, WIKIBASE.sitelinks, Literal(0)))

    def _do_iterencode_property(
            self,
            property: Property,
            define: bool = False
    ) -> Iterator[str]:
        if property in self._seen_entity:
            yield ''
        else:
            uri = cast(URIRef, property._to_rdflib())
            self._seen_entity[property] = uri
            yield from self._tr((uri, RDF.type, WIKIBASE.Property))
            if define:
                schema = self._get_property_schema(property)
                assert property.range is not None
                dt_uri = property.range._to_rdflib()
                yield from self._tr(
                    (uri, WIKIBASE.propertyType, dt_uri),
                    (uri, WIKIBASE.claim, schema['p']),
                    (uri, WIKIBASE.qualifier, schema['pq']),
                    (uri, WIKIBASE.qualifierValue, schema['pqv']),
                    (uri, WIKIBASE.reference, schema['pr']),
                    (uri, WIKIBASE.referenceValue, schema['prv']),
                    (uri, WIKIBASE.statementProperty, schema['ps']),
                    (uri, WIKIBASE.statementValue, schema['psv']),
                    (uri, WIKIBASE.novalue, schema['wdno']),
                    (uri, WIKIBASE.directClaim, schema['wdt']))

    def _do_iterencode_lexeme(self, lexeme: Lexeme) -> Iterator[str]:
        if lexeme in self._seen_entity:
            yield ''
        else:
            uri = cast(URIRef, lexeme._to_rdflib())
            self._seen_entity[lexeme] = uri
            yield from self._tr((uri, RDF.type, ONTOLEX.LexicalEntry))

    def _do_iterencode_value(
            self,
            value: Value,
            wds: URIRef,
            ps: URIRef,
            psv: URIRef
    ) -> Iterator[str]:
        if isinstance(value, Entity):
            yield from self._do_iterencode_entity(value)
            yield from self._tr((wds, ps, self._seen_entity[value]))
        elif isinstance(value, ShallowDataValue):
            yield from self._tr((wds, ps, value._to_rdflib()))
        elif isinstance(value, DeepDataValue):
            yield from self._do_iterencode_deep_data_value(value)
            yield from self._tr(
                (wds, ps, value._to_rdflib()),
                (wds, psv, self._seen_deep_data_value[value]))
        else:
            raise KIF_Object._should_not_get_here()

    def _do_iterencode_deep_data_value(
            self,
            value: DeepDataValue
    ) -> Iterator[str]:
        if value in self._seen_deep_data_value:
            yield ''
        else:
            wdv = Wikidata.WDV[value.digest]
            self._seen_deep_data_value[value] = wdv
            if isinstance(value, Quantity):
                yield from self._tr(
                    (wdv, RDF.type, WIKIBASE.QuantityValue),
                    (wdv, WIKIBASE.quantityAmount, value._to_rdflib()))
                if value.unit is not None:
                    yield from self._do_iterencode_item(value.unit)
                    yield from self._tr(
                        (wdv, WIKIBASE.quantityUnit,
                         self._seen_entity[value.unit]))
                if value.lower_bound is not None:
                    yield from self._tr(
                        (wdv, WIKIBASE.quantityLowerBound,
                         Literal(value.lower_bound)))
                if value.upper_bound is not None:
                    yield from self._tr(
                        (wdv, WIKIBASE.quantityUpperBound,
                         Literal(value.upper_bound)))
            elif isinstance(value, Time):
                yield from self._tr(
                    (wdv, RDF.type, WIKIBASE.TimeValue),
                    (wdv, WIKIBASE.timeValue, value._to_rdflib()))
                if value.precision is not None:
                    yield from self._tr(
                        (wdv, WIKIBASE.timePrecision,
                         Literal(value.precision.value)))
                if value.timezone is not None:
                    yield from self._tr(
                        (wdv, WIKIBASE.timeTimezone,
                         Literal(value.timezone)))
                if value.calendar is not None:
                    yield from self._do_iterencode_item(value.calendar)
                    yield from self._tr(
                        (wdv, WIKIBASE.timeCalendarModel,
                         self._seen_entity[value.calendar]))
            else:
                raise KIF_Object._should_not_get_here()

    def _do_iterencode_reference_record(
            self,
            ref: ReferenceRecord
    ) -> Iterator[str]:
        if ref in self._seen_reference_record:
            yield ''
        else:
            wdref = Wikidata.WDREF[ref.digest]
            self._seen_reference_record[ref] = wdref
            for snak in ref:
                schema = self._get_property_schema(snak.property)
                yield from self._do_iterencode_snak(
                    snak, wdref, schema['pr'], schema['prv'], schema['wdno'])

    def _tr(self, tr: TTriple, *trs: TTriple) -> Iterator[str]:
        for (s, p, o) in itertools.chain((tr,), trs):
            yield s.n3()
            yield ' '
            yield p.n3()
            yield ' '
            yield o.n3()
            yield ' .\n'
