# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import decimal
import io
import json
import re

from .. import namespace as NS
from ..model import (
    Datatype,
    DeepDataValue,
    Entity,
    IRI,
    Item,
    Lexeme,
    NoValueSnak,
    Property,
    Quantity,
    Rank,
    Snak,
    SomeValueSnak,
    Statement,
    StringDatatype,
    Text,
    Time,
    Value,
    ValueSnak,
)
from ..rdflib import BNode, Literal, Result, URIRef
from ..typing import Any, cast, Iterator, Mapping, TypeAlias
from .abc import Store

TRes: TypeAlias = dict[str, Any]


class SPARQL_Results(Mapping):
    """SPARQL results.

       See <https://www.w3.org/TR/sparql11-results-json/>."""

# -- Bindings --------------------------------------------------------------

    class Bindings(Mapping):
        """Bindings of SPARQL results."""

        __slots__ = (
            '_bindings',
        )

        _bindings: TRes

        def __init__(self, bindings: TRes) -> None:
            self._bindings = bindings

        def __getitem__(self, key: str) -> Any:
            return self._bindings[key]

        def __iter__(self) -> Iterator[str]:
            return iter(self._bindings)

        def __len__(self) -> int:
            return len(self._bindings)

        def _error(self, msg: str) -> Store.Error:
            return Store._error(f'bad SPARQL results: {msg}')

        def _error_bad(
                self,
                var: str,
                expected: str | None = None,
                got: str | None = None
        ) -> Store.Error:
            msg = f"bad value for '{var}'"
            if expected and got:
                return self._error(f"{msg} (expected {expected}, got {got})")
            elif got:
                return self._error(f"{msg} ({got})")
            else:
                return self._error(msg)

        def _error_missing(self, var: str) -> Store.Error:
            return self._error(f"missing '{var}'")

        # -- RDFLib checks --

        def check(self, var: str) -> BNode | Literal | URIRef:
            bdn = self._check_binding(var)
            type = self._check_type(bdn)
            if type == 'bnode':
                return self._check_bnode_tail(bdn)
            elif type == 'literal':
                return self._check_literal_tail(bdn)
            else:
                return self._check_uriref_tail(bdn)

        def check_bnode_or_uriref(self, var: str) -> BNode | URIRef:
            bdn = self._check_binding(var)
            type = self._check_type(bdn)
            if type == 'bnode':
                return self._check_bnode_tail(bdn)
            elif type == 'uri':
                return self._check_uriref_tail(bdn)
            else:
                raise self._error_bad('type', 'bnode or uri', type)

        def check_bnode(self, var: str) -> BNode:
            bdn = self._check_binding(var)
            type = self._check_type(bdn)
            if type != 'bnode':
                raise self._error_bad('type', 'bnode', type)
            return self._check_bnode_tail(bdn)

        def _check_bnode_tail(self, bdn: TRes) -> BNode:
            return BNode(self._check_value(bdn))

        def check_uriref(self, var: str) -> URIRef:
            bdn = self._check_binding(var)
            type = self._check_type(bdn)
            if type != 'uri':
                raise self._error_bad('type', 'uri', type)
            return self._check_uriref_tail(bdn)

        def _check_uriref_tail(self, bdn: TRes) -> URIRef:
            return URIRef(self._check_value(bdn))

        def check_literal(self, var: str) -> Literal:
            bdn = self._check_binding(var)
            type = self._check_type(bdn)
            if type != 'literal':
                raise self._error_bad('type', 'literal', type)
            return self._check_literal_tail(bdn)

        def _check_literal_tail(self, bdn: TRes) -> Literal:
            value = self._check_value(bdn)
            datatype: URIRef | None = None
            if 'datatype' in bdn:
                datatype = URIRef(bdn['datatype'])
            lang: str | None = None
            if 'xml:lang' in bdn:
                lang = bdn['xml:lang']
            if datatype == NS.XSD.dateTime or datatype == NS.XSD.date:
                if value[0] == '+' or value[0] == '-':
                    ###
                    # FIXME: RDFLib does not support the +/- sign used by
                    # Wikidata at the start of date-time literals.
                    ###
                    value = value[1:]
                datatype = NS.XSD.dateTime
                if 'T' not in value:
                    ###
                    # FIXME: This is a hack! We should use an external lib
                    # to do this kind of thing.
                    ###
                    for fmt in ['%Y-%m-%d', '%Y-%m-%d%z']:
                        try:
                            value = datetime.datetime.strptime(
                                value, fmt).isoformat()
                            break
                        except ValueError:
                            pass
            return Literal(value, datatype=datatype, lang=lang)

        def _check_binding(self, var: str) -> TRes:
            if var not in self:
                raise self._error(f"no binding for '{var}'")
            return self[var]

        def _check_type(
                self,
                bdn: TRes,
                _types={
                    'uri': 'uri',
                    'literal': 'literal',
                    'typed-literal': 'literal',
                    'bnode': 'bnode'
                }
        ) -> str:
            if 'type' not in bdn:
                raise self._error_missing('type')
            type = bdn['type']
            if type not in _types:
                raise self._error_bad('type', got=type)
            return _types[type]

        def _check_value(self, bdn: TRes) -> str:
            if 'value' not in bdn:
                raise self._error_missing('value')
            return bdn['value']

        # -- KIF checks --

        def check_datatype(
                self,
                var: str,
                value: Datatype | None = None
        ) -> Datatype:
            if value:
                return value
            uri = self.check_uriref(var)
            try:
                return Datatype._from_rdflib(uri)
            except ValueError:
                return StringDatatype()  # unknown datatype, fallback to string

        def check_entity(
                self,
                var: str,
                value: Entity | None = None
        ) -> Entity:
            if value:
                return value
            uri = self.check_uriref(var)
            if NS.Wikidata.is_wd_item(uri):
                return Item(uri)
            elif NS.Wikidata.is_wd_property(uri):
                return Property(uri)
            elif NS.Wikidata.is_wd_lexeme(uri):
                return Lexeme(uri)
            else:
                raise self._error_bad(var, 'a Wikidata entity', str(uri))

        def check_item(
                self,
                var: str,
                value: Item | None = None
        ) -> Item:
            if value:
                return value
            uri = self.check_uriref(var)
            if not NS.Wikidata.is_wd_item(uri):
                raise self._error_bad(var, 'a Wikidata item', str(uri))
            return Item(uri)

        def check_property(
                self,
                var: str,
                value: Property | None = None,
                split=False
        ) -> Property:
            if value:
                return value
            uri = self.check_uriref(var)
            if split:
                name = NS.Wikidata.get_wikidata_name(uri)
                return Property(NS.Wikidata.WD[name])
            else:
                if not NS.Wikidata.is_wd_property(uri):
                    raise self._error_bad(var, 'a Wikidata property', str(uri))
                return Property(uri)

        def check_lexeme(
                self,
                var: str,
                value: Lexeme | None = None,
                split=False
        ) -> Lexeme:
            if value:
                return value
            uri = self.check_uriref(var)
            if split:
                name = NS.Wikidata.get_wikidata_name(uri)
                return Lexeme(NS.Wikidata.WD[name])
            else:
                if not NS.Wikidata.is_wd_lexeme(uri):
                    raise self._error_bad(var, 'a Wikidata lexeme', str(uri))
                return Lexeme(uri)

        def check_iri(self, var: str) -> IRI:
            return IRI(self.check_uriref(var))

        def check_text(self, var: str) -> Text:
            val = self.check_literal(var)
            return Text(str(val), val.language)

        def check_quantity(
                self,
                var_qt_amount: str,
                var_qt_unit: str,
                var_qt_lower: str,
                var_qt_upper: str,
                value: Quantity | None = None
        ) -> Quantity:
            assert value is None or isinstance(value, Quantity)
            qt_amount: decimal.Decimal
            qt_unit: Item | None
            qt_lb: decimal.Decimal | None
            qt_ub: decimal.Decimal | None
            if value:
                qt_amount = cast(Quantity, value).amount
            else:
                qt_amount = self.check_decimal(var_qt_amount)
            if var_qt_unit in self:
                qt_unit = self.check_item(var_qt_unit)
            elif value:
                qt_unit = value.unit
            else:
                qt_unit = None
            if var_qt_lower in self:
                qt_lb = self.check_decimal(var_qt_lower)
            elif value:
                qt_lb = cast(Quantity, value).lower_bound
            else:
                qt_lb = None
            if var_qt_upper in self:
                qt_ub = self.check_decimal(var_qt_upper)
            elif value:
                qt_ub = cast(Quantity, value).upper_bound
            else:
                qt_ub = None
            return Quantity(qt_amount, qt_unit, qt_lb, qt_ub)

        def check_time(
                self,
                var_tm_value: str,
                var_tm_precision: str,
                var_tm_timezone: str,
                var_tm_calendar: str,
                value: Time | None = None
        ) -> Time:
            assert value is None or isinstance(value, Time)
            tm_value: datetime.datetime
            tm_prec: int | None
            tm_tz: int | None
            tm_cal: Item | None
            if value:
                tm_value = cast(Time, value).time
            else:
                tm_value = self.check_datetime(var_tm_value)
            if var_tm_precision in self:
                tm_prec = self.check_integer(var_tm_precision)
            elif value and value.precision is not None:
                tm_prec = value.precision.value
            else:
                tm_prec = None
            if var_tm_timezone in self:
                tm_tz = self.check_integer(var_tm_timezone)
            elif value:
                tm_tz = cast(Time, value).timezone
            else:
                tm_tz = None
            if var_tm_calendar in self:
                tm_cal = self.check_item(var_tm_calendar)
            elif value:
                tm_cal = value.calendar
            else:
                tm_cal = None
            return Time(tm_value, tm_prec, tm_tz, tm_cal)

        def check_snak(
                self,
                property: Property,
                var_value: str,
                var_qt_amount: str,
                var_qt_unit: str,
                var_qt_lower: str,
                var_qt_upper: str,
                var_tm_value: str,
                var_tm_precision: str,
                var_tm_timezone: str,
                var_tm_calendar: str,
                value: Value | None = None,
        ) -> Snak:
            if value:
                if isinstance(value, DeepDataValue):
                    if isinstance(value, Quantity):
                        return ValueSnak(property, self.check_quantity(
                            var_qt_amount, var_qt_unit,
                            var_qt_lower, var_qt_upper,
                            cast(Quantity, value)))
                    elif isinstance(value, Time):
                        return ValueSnak(property, self.check_time(
                            var_tm_value, var_tm_precision,
                            var_tm_timezone, var_tm_calendar,
                            cast(Time, value)))
                    else:
                        raise Store._should_not_get_here()
                else:
                    return ValueSnak(property, value)
            else:
                if var_value not in self:
                    # Absence of value means no value.
                    return NoValueSnak(property)
                if var_qt_amount in self:
                    return ValueSnak(property, self.check_quantity(
                        var_qt_amount, var_qt_unit, var_qt_lower, var_qt_upper,
                        cast(Quantity, value)))
                if var_tm_value in self:
                    return ValueSnak(property, self.check_time(
                        var_tm_value, var_tm_precision,
                        var_tm_timezone, var_tm_calendar,
                        cast(Time, value)))
                val = self.check(var_value)
                if isinstance(val, URIRef):
                    if NS.Wikidata.is_wd_some_value(val):
                        ###
                        # IMPORTANT: Newer versions of Wikidata use Skolem
                        # IRIs to represent SomeValueSnak.
                        ###
                        return SomeValueSnak(property)
                    else:
                        return ValueSnak(property, Value._from_rdflib(val))
                elif isinstance(val, BNode):
                    ###
                    # IMPORTANT: Older versions of Wikidata use blank nodes
                    # to represent SomeValueSnak.
                    ###
                    return SomeValueSnak(property)
                elif isinstance(val, Literal):
                    return ValueSnak(property, Value._from_rdflib(val))
                else:
                    raise Store._should_not_get_here()

        def check_statement(
                self,
                var_subject: str,
                var_property: str,
                var_value: str,
                var_qt_amount: str,
                var_qt_unit: str,
                var_qt_lower: str,
                var_qt_upper: str,
                var_tm_value: str,
                var_tm_precision: str,
                var_tm_timezone: str,
                var_tm_calendar: str,
                value: Value | None = None
        ) -> Statement:
            return Statement(
                self.check_entity(var_subject),
                self.check_snak(
                    self.check_property(var_property), var_value,
                    var_qt_amount, var_qt_unit, var_qt_lower, var_qt_upper,
                    var_tm_value, var_tm_precision,
                    var_tm_timezone, var_tm_calendar, value))

        def check_rank(self, var: str) -> Rank:
            uri = self.check_uriref(var)
            try:
                return Rank._from_rdflib(uri)
            except ValueError as err:
                raise self._error_bad(var, 'a Wikibase rank', uri) from err

        def check_datetime(
                self,
                var: str,
                _re=re.compile(r'^[+-]?(\d+)-(\d+)-(\d+)')
        ) -> datetime.datetime:
            from datetime import date, time
            val = self.check_literal(var)
            if val.datatype != NS.XSD.dateTime:
                self._error_bad(var, 'a xsd:dateTime', val.n3())
            try:
                dt = val.toPython()
            except ValueError:
                dt = str(val)
            if isinstance(dt, datetime.datetime):
                return dt
            elif isinstance(dt, date):
                return datetime.datetime.combine(dt, time())
            elif isinstance(dt, str):
                m = _re.match(dt)
                if m is None:
                    return datetime.datetime.fromisoformat(str(val))
                else:
                    y, m, _ = map(int, m.groups())
                    y = max(min(y, 9999), 1)
                    m = max(min(m, 12), 1)
                    return datetime.datetime(y, m, 1)
            else:
                raise Store._should_not_get_here()

        def check_decimal(self, var: str) -> decimal.Decimal:
            val = self.check_literal(var)
            if val.datatype != NS.XSD.decimal:
                self._error_bad(var, 'a xsd:decimal', val.n3())
            return val.toPython()

        def check_integer(self, var: str) -> int:
            val = self.check_literal(var)
            if val.datatype != NS.XSD.integer:
                self._error_bad(var, 'a xsd:integer', val.n3())
            return val.toPython()

# -- Results ---------------------------------------------------------------

    __slots__ = (
        '_results',
        '_vars',
        '_bindings',
    )

    _results: TRes
    _vars: TRes
    _bindings: Iterator[Bindings]

    def __init__(self, results: TRes) -> None:
        self._results = results
        try:
            self._vars = results['head']['vars']
            self._bindings = map(self.Bindings, results['results']['bindings'])
        except KeyError as err:
            raise self._error(f'no {err}')

    def __getitem__(self, key: str) -> Any:
        return self._results[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._results)

    def __len__(self) -> int:
        return len(self._results)

    def __str__(self) -> str:
        res = Result.parse(io.StringIO(json.dumps(dict(self))), format='json')
        out = res.serialize(format='txt', namespace_manager=NS._DEFAULT_NSM)
        assert out is not None
        return out.decode('utf-8')

    def _error(self, msg: str) -> Store.Error:
        return Store._error(f'bad SPARQL results: {msg}')

    @property
    def vars(self) -> TRes:
        return self._vars

    @property
    def bindings(self) -> Iterator[Bindings]:
        return self._bindings
