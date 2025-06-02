# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ... import itertools
from ...context import Context
from ...model import (
    AnnotatedStatement,
    DeepDataValue,
    Entity,
    Graph,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    NoValueSnak,
    Property,
    PseudoProperty,
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
from ...model.kif_object import Encoder, Object
from ...namespace import ONTOLEX, PROV, RDF, WIKIBASE, Wikidata
from ...rdflib import BNode, Literal, split_uri, URIRef
from ...typing import (
    Callable,
    cast,
    Iterator,
    override,
    TypeAlias,
    TypedDict,
    Union,
)
from .options import RDF_EncoderOptions

TSubject: TypeAlias = Union[URIRef, BNode]
TPredicate: TypeAlias = URIRef
TObject: TypeAlias = Union[URIRef, BNode, Literal]
TTriple: TypeAlias = tuple[TSubject, TPredicate, TObject]


class RDF_Encoder(
        Encoder,
        format='rdf',
        description='RDF encoder'
):
    """RDF encoder."""

    class AbsoluteSchema(TypedDict):
        """Property schema with absolute URIs."""

        p: URIRef
        pq: URIRef
        pqv: URIRef
        pr: URIRef
        prv: URIRef
        ps: URIRef
        psv: URIRef
        wdno: URIRef
        wdt: URIRef

    @classmethod
    def _get_context_options(
            cls,
            context: Context | None = None
    ) -> RDF_EncoderOptions:
        return Context.top(context).options.codec.rdf.encoder

    @classmethod
    def _default_gen_wdref(cls, reference: ReferenceRecord) -> str:
        return reference.digest

    @classmethod
    def _default_gen_wds(cls, statement: Statement) -> str:
        return statement.digest

    @classmethod
    def _default_gen_wdv(cls, value: Value) -> str:
        return value.digest

    __slots__ = (
        '_gen_wdref',
        '_gen_wds',
        '_gen_wdv',
        '_options',
        '_schema',
        '_seen_absolute_schemas',
        '_seen_deep_data_value',
        '_seen_entity',
        '_seen_reference_record',
    )

    #: Callback to use to generate WDREF IRIs.
    _gen_wdref: Callable[[ReferenceRecord], str]

    #: Callback to use to generate WDS IRIs.
    _gen_wds: Callable[[Statement], str]

    #: Callback to use to generate WDV IRIs.
    _gen_wdv: Callable[[Value], str]

    #: RDF encoder options.
    _options: RDF_EncoderOptions

    #: Default property schema.
    _schema: Property.Schema | None

    #: Cached absolute schemas.
    _seen_absolute_schemas: dict[Property, RDF_Encoder.AbsoluteSchema]

    #: Cached deep data values.
    _seen_deep_data_value: dict[DeepDataValue, URIRef]

    #: Cached entities.
    _seen_entity: dict[Entity, URIRef]

    #: Cached reference records.
    _seen_reference_record: dict[ReferenceRecord, URIRef]

    def __init__(
            self,
            schema: Property.TSchema | None = None,
            gen_wdref: Callable[[ReferenceRecord], str] | None = None,
            gen_wds: Callable[[Statement], str] | None = None,
            gen_wdv: Callable[[Value], str] | None = None,
            context: Context | None = None
    ) -> None:
        if gen_wdref:
            self._gen_wdref = lambda x: str(gen_wdref(x))
        else:
            self._gen_wdref = self._default_gen_wdref
        if gen_wds:
            self._gen_wds = lambda x: str(gen_wds(x))
        else:
            self._gen_wds = self._default_gen_wds
        if gen_wdv:
            self._gen_wdv = lambda x: str(gen_wdv(x))
        else:
            self._gen_wdv = self._default_gen_wdv
        self._options = self._get_context_options(context).copy()
        if schema is not None:
            self._options.set_schema(schema, type(self), 'schema', 1)
        self._seen_absolute_schemas = {}
        self._seen_deep_data_value = {}
        self._seen_entity = {}
        self._seen_reference_record = {}

    def _get_absolute_schema(
            self,
            property: Property
    ) -> RDF_Encoder.AbsoluteSchema:
        assert not isinstance(property, PseudoProperty)
        if property in self._seen_absolute_schemas:
            return self._seen_absolute_schemas[property]
        if property.range is None:
            raise self._error(f'no datatype for property: {property}')
        assert property.range is not None
        schema = property.schema or self._options.schema
        if schema is not None:
            _, name = split_uri(property.iri.content)
            absolute_schema = cast(RDF_Encoder.AbsoluteSchema, {
                k: URIRef(cast(IRI, v).content + name)
                for k, v in schema.items()})
            self._seen_absolute_schemas[property] = absolute_schema
            return absolute_schema
        else:
            raise self._error(f'no schema for property: {property}')

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
        if isinstance(stmt.snak.property, PseudoProperty):
            if not isinstance(stmt.snak, ValueSnak):
                return          # nothing to do
            yield from self._do_iterencode_entity(stmt.subject)
            subject = self._seen_entity[stmt.subject]
            value = stmt.snak.value
            if isinstance(value, Entity):
                self._do_iterencode_entity(value)
            yield from self._tr(
                (subject, cast(URIRef, stmt.snak.property._to_rdflib()),
                 stmt.snak.value._to_rdflib()))
        else:
            schema = self._get_absolute_schema(stmt.snak.property)
            wds = Wikidata.WDS[self._gen_wds(stmt)]
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
                if isinstance(qsnak.property, PseudoProperty):
                    continue    # skip
                qschema = self._get_absolute_schema(qsnak.property)
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
        yield from self._do_iterencode_property(snak.property)
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
            return              # nothing do do
        uri = cast(URIRef, item._to_rdflib())
        self._seen_entity[item] = uri
        yield from self._tr((uri, WIKIBASE.sitelinks, Literal(0)))

    def _do_iterencode_property(
            self,
            property: Property,
            define: bool = True
    ) -> Iterator[str]:
        if property in self._seen_entity:
            return              # nothing to do
        uri = cast(URIRef, property._to_rdflib())
        self._seen_entity[property] = uri
        yield from self._tr((uri, RDF.type, WIKIBASE.Property))
        if property.range is not None:
            dt_uri = property.range._to_rdflib()
            yield from self._tr((uri, WIKIBASE.propertyType, dt_uri))
        if define:
            schema = self._get_absolute_schema(property)
            assert property.range is not None
            yield from self._tr(
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
            return              # nothing to do
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
            return              # nothing to do
        wdv = Wikidata.WDV[self._gen_wdv(value)]
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
            return              # nothing to do
        wdref = Wikidata.WDREF[self._gen_wdref(ref)]
        self._seen_reference_record[ref] = wdref
        for snak in ref:
            if isinstance(snak.property, PseudoProperty):
                continue        # skip
            schema = self._get_absolute_schema(snak.property)
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
