# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import io
import json
from collections.abc import Mapping
from typing import Any, cast, Optional, Union

from rdflib import BNode, Literal, URIRef

from .. import namespace as NS
from ..error import ShouldNotGetHere
from ..model import (
    Datetime,
    Decimal,
    Entity,
    IRI,
    Item,
    NoValueSnak,
    Property,
    Quantity,
    Rank,
    Snak,
    SomeValueSnak,
    Statement,
    Text,
    Time,
    UTC,
    Value,
    ValueSnak,
)
from .abc import StoreError

# See <https://www.w3.org/TR/sparql11-results-json/>.

TRes = dict[str, Any]


class Bindings(Mapping):
    __slots__ = (
        '_bindings',
    )

    _bindings: TRes

    def __init__(self, bindings: TRes):
        self._bindings = bindings

    def __getitem__(self, key):
        return self._bindings[key]

    def __iter__(self):
        return iter(self._bindings)

    def __len__(self):
        return len(self._bindings)

    def _error(self, msg: str) -> StoreError:
        return StoreError(f'bad SPARQL results: {msg}')

    def _error_bad(
            self,
            var: str,
            expected: Optional[str] = None,
            got: Optional[str] = None
    ) -> StoreError:
        msg = f"bad value for '{var}'"
        if expected and got:
            return self._error(f"{msg} (expected {expected}, got {got})")
        elif got:
            return self._error(f"{msg} ({got})")
        else:
            return self._error(msg)

    def _error_missing(self, var: str) -> StoreError:
        return self._error(f"missing '{var}'")

    # -- RDFLib checks -----------------------------------------------------

    def check(self, var: str) -> Union[BNode, Literal, URIRef]:
        bdn = self._check_binding(var)
        type = self._check_type(bdn)
        if type == 'bnode':
            return self._check_bnode_tail(bdn)
        elif type == 'literal':
            return self._check_literal_tail(bdn)
        else:
            return self._check_uriref_tail(bdn)

    def check_bnode_or_uriref(self, var: str) -> Union[BNode, URIRef]:
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
        datatype: Optional[URIRef] = None
        if 'datatype' in bdn:
            datatype = URIRef(bdn['datatype'])
        lang: Optional[str] = None
        if 'xml:lang' in bdn:
            lang = bdn['xml:lang']
        if (datatype == NS.XSD.dateTime
                and (value[0] == '+' or value[0] == '-')):
            ###
            # FIXME: RDFLib does not support the +/- sign used by Wikidata
            # at the start of date-time literals.
            ###
            value = value[1:]
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

    # -- KIF checks --------------------------------------------------------

    def check_entity(
            self,
            var: str,
            value: Optional[Entity] = None
    ) -> Entity:
        if value:
            return value
        uri = self.check_uriref(var)
        if NS.Wikidata.is_wd_item(uri):
            return Item(uri)
        elif NS.Wikidata.is_wd_property(uri):
            return Property(uri)
        else:
            raise self._error_bad(var, 'a Wikidata entity', str(uri))

    def check_item(
            self,
            var: str,
            value: Optional[Item] = None
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
            value: Optional[Property] = None,
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
            value: Optional[Quantity] = None
    ) -> Quantity:
        assert value is None or value.is_quantity()
        qt_amount: Decimal
        qt_unit: Optional[Item]
        qt_lb: Optional[Decimal]
        qt_ub: Optional[Decimal]
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
            value: Optional[Time] = None
    ) -> Time:
        assert value is None or value.is_time()
        tm_value: Datetime
        tm_prec: Optional[int]
        tm_tz: Optional[int]
        tm_cal: Optional[Item]
        if value:
            tm_value = cast(Time, value).time
        else:
            ###
            # IMPORTANT: Do not forget to reset tzinfo to UTC.
            # In KIF, the actual timezone is stored in the Time object.
            ###
            tm_value = self.check_datetime(var_tm_value).replace(tzinfo=UTC)
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
            tm_cal = value.calendar_model
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
            value: Optional[Value] = None,
    ) -> Snak:
        if value:
            if value.is_deep_data_value():
                if value.is_quantity():
                    return ValueSnak(property, self.check_quantity(
                        var_qt_amount, var_qt_unit,
                        var_qt_lower, var_qt_upper,
                        cast(Quantity, value)))
                elif value.is_time():
                    return ValueSnak(property, self.check_time(
                        var_tm_value, var_tm_precision,
                        var_tm_timezone, var_tm_calendar,
                        cast(Time, value)))
                else:
                    raise ShouldNotGetHere
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
                    # Newer versions of Wikidata use Skolem IRIs to
                    # represent SomeValueSnak.
                    return SomeValueSnak(property)
                else:
                    return ValueSnak(property, Value._from_rdflib(val))
            elif isinstance(val, BNode):
                # Older versions of Wikidata use blank nodes to
                # represent SomeValueSnak.
                return SomeValueSnak(property)
            elif isinstance(val, Literal):
                return ValueSnak(property, Value._from_rdflib(val))
            else:
                raise ShouldNotGetHere

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
            value: Optional[Value] = None) -> Statement:
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
        except ValueError:
            raise self._error_bad(var, 'a Wikibase rank', uri)

    def check_datetime(self, var: str) -> Datetime:
        from datetime import date, time
        val = self.check_literal(var)
        if val.datatype != NS.XSD.dateTime:
            self._error_bad(var, 'a xsd:dateTime', val.n3())
        dt = val.toPython()
        if isinstance(dt, Datetime):
            return dt
        elif isinstance(dt, date):
            return Datetime.combine(dt, time())
        else:
            raise ShouldNotGetHere

    def check_decimal(self, var: str) -> Decimal:
        val = self.check_literal(var)
        if val.datatype != NS.XSD.decimal:
            self._error_bad(var, 'a xsd:decimal', val.n3())
        return val.toPython()

    def check_integer(self, var: str) -> int:
        val = self.check_literal(var)
        if val.datatype != NS.XSD.integer:
            self._error_bad(var, 'a xsd:integer', val.n3())
        return val.toPython()


class SPARQL_Results(Mapping):
    __slots__ = (
        '_results',
        '_vars',
        '_bindings',
    )

    _results: TRes
    _vars: TRes
    _bindings: map

    def __init__(self, results: TRes):
        self._results = results
        try:
            self._vars = results['head']['vars']
            self._bindings = map(Bindings, results['results']['bindings'])
        except KeyError as err:
            raise self._error(f'no {err}')

    def __getitem__(self, key):
        return self._results[key]

    def __iter__(self):
        return iter(self._results)

    def __len__(self):
        return len(self._results)

    def __str__(self):
        from rdflib.query import Result
        res = Result.parse(
            io.StringIO(json.dumps(dict(self))), format='json')
        return res.serialize(
            format='txt', namespace_manager=NS._DEFAULT_NSM).decode('utf-8')

    def _error(self, msg):
        return StoreError(f'bad SPARQL results: {msg}')

    @property
    def vars(self):
        return self._vars

    @property
    def bindings(self):
        return self._bindings
