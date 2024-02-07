# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable

from .. import namespace as NS
from ..error import ShouldNotGetHere
from ..model import (
    DataValue,
    Entity,
    Property,
    Quantity,
    String,
    Text,
    Time,
    Value,
)
from ..typing import Any, Callable, cast, Optional
from .sparql_builder import SPARQL_Builder

TTrm = SPARQL_Builder.TTrm
Variable = SPARQL_Builder.Variable


class SPARQL_Mapping:

    class Builder(SPARQL_Builder):
        matched_property: TTrm
        matched_subject: TTrm
        matched_value: TTrm
        p: Variable
        pname: Variable
        property: Variable
        ps: Variable
        psv: Variable
        qt_amount: Variable
        qt_lower: Variable
        qt_unit: Variable
        qt_upper: Variable
        subject: Variable
        tm_calendar: Variable
        tm_precision: Variable
        tm_timezone: Variable
        tm_value: Variable
        value: Variable
        wds: Variable
        wdt: Variable

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.matched_property = self.var('matched_property')
            self.matched_subject = self.var('matched_subject')
            self.matched_value = self.var('matched_value')
            self.p = self.var('p')
            self.pname = self.var('pname')
            self.property = self.var('property')
            self.ps = self.var('ps')
            self.psv = self.var('psv')
            self.qt_amount = self.var('qt_amount')
            self.qt_lower = self.var('qt_lower')
            self.qt_unit = self.var('qt_unit')
            self.qt_upper = self.var('qt_upper')
            self.subject = self.var('subject')
            self.tm_calendar = self.var('tm_calendar')
            self.tm_precision = self.var('tm_precision')
            self.tm_timezone = self.var('tm_timezone')
            self.tm_value = self.var('tm_value')
            self.value = self.var('value')
            self.wds = self.var('wds')
            self.wdt = self.var('wdt')

        def bind_uri(
                self,
                term: TTrm,
                var: Variable,
                replace_prefix: Optional[tuple[str, str]] = None
        ) -> 'SPARQL_Mapping.Builder':
            if replace_prefix is not None:
                pfx, by = replace_prefix
                q = self.bind(self.uri(self.concat(
                    String(str(by)),
                    self.substr(self.str_(term), len(str(pfx)) + 1))), var)
            else:
                q = self.bind(self.uri(term), var)
            return cast(SPARQL_Mapping.Builder, q)

    class Entry:

        class Skip(Exception):
            pass

        entity: Entity
        datatype: type[Value]
        definition: Callable[
            ['SPARQL_Mapping.Entry', SPARQL_Builder,
             TTrm, TTrm, TTrm], Optional[bool]]
        kwargs: dict[str, Any]

        def __init__(
                self,
                entity: Entity,
                datatype: type[Value],
                definition: Callable[
                    ['SPARQL_Mapping.Entry', SPARQL_Builder,
                     TTrm, TTrm, TTrm], Optional[bool]],
                **kwargs: Any
        ):
            self.entity = entity
            self.datatype = datatype
            self.definition = definition
            self.kwargs = kwargs

        def define(
                self,
                q: 'SPARQL_Mapping.Builder',
                s: Optional[TTrm] = None,
                p: Optional[TTrm] = None,
                v: Optional[TTrm] = None,
                with_binds: bool = False
        ) -> bool:
            if s is None:
                s = q.matched_subject
            if p is None:
                p = q.matched_property
            if v is None:
                v = q.matched_value
            try:
                self.definition(self, q, s, p, v)
            except self.Skip:
                return False
            if with_binds:
                self._bind(q)
            return True

        def _bind(self, q: 'SPARQL_Mapping.Builder'):
            # subject
            q.bind_uri(
                q.matched_subject, q.subject,
                self.kwargs.get('subject_replace_prefix', None))
            # property
            pname = NS.Wikidata.get_wikidata_name(self.entity.iri.value)
            q.bind(String(pname), q.pname)
            q.bind_uri(q.concat(String(str(NS.P)), String(pname)), q.p)
            q.bind_uri(q.concat(String(str(NS.PS)), String(pname)), q.ps)
            q.bind_uri(
                q.concat(String(str(NS.WD)), String(pname)), q.property)
            q.bind_uri(q.concat(String(str(NS.WDT)), String(pname)), q.wdt)
            # wds
            q.bind_uri(q.concat(
                String(NS.WDS),
                q.md5(q.subject),
                String('_' + pname + '_'),
                q.md5(q.value)), q.wds)
            # value
            if issubclass(self.datatype, Entity):
                q.bind_uri(
                    q.matched_value, q.value,
                    self.kwargs.get('value_replace_prefix', None))
            elif issubclass(self.datatype, DataValue):
                value: Optional[TTrm] = None
                if self.datatype is Quantity:
                    dt = self.kwargs.get('value_set_datatype')
                    if (dt is not None
                            and isinstance(q.matched_value, Variable)):
                        value = q.strdt(q.matched_value, dt)
                    else:
                        value = q.matched_value
                    q.bind(value, q.qt_amount)
                    unit = self.kwargs.get('unit')
                    if unit is not None:
                        q.bind(unit, q.qt_unit)
                elif self.datatype is String:
                    value = q.str_(q.matched_value)
                elif self.datatype is Text:
                    lang = self.kwargs.get('value_set_language')
                    if (lang is not None
                            and isinstance(q.matched_value, Variable)):
                        value = q.strlang(q.matched_value, String(lang))
                    else:
                        value = q.matched_value
                elif self.datatype is Time:
                    value = q.matched_value
                    q.bind(value, q.tm_value)
                    prec = self.kwargs.get('precision')
                    if prec is not None:
                        q.bind(prec.value, q.tm_precision)
                    tz = self.kwargs.get('timezone')
                    if tz is not None:
                        q.bind(tz, q.tm_timezone)
                    cal = self.kwargs.get('calendar')
                    if cal is not None:
                        q.bind(cal, q.tm_calendar)
                else:
                    raise ShouldNotGetHere
                assert value is not None
                q.bind(value, q.value)
            else:
                raise ShouldNotGetHere

    entries: dict[Entity, 'SPARQL_Mapping.Entry']
    subject_replace_prefix: list[tuple[str, str]]
    value_replace_prefix: list[tuple[str, str]]

    def __init__(self):
        self.entries = dict()
        self.subject_replace_prefix = []

    def register(
            self,
            entity: Entity,
            datatype: type[Value],
            **kwargs: Any
    ) -> Callable[..., Any]:
        return lambda f: self._register(self.Entry(
            entity, datatype, f, **kwargs))

    def _register(self, entry: Entry):
        self.entries[entry.entity] = entry
        if 'subject_replace_prefix' in entry.kwargs:
            self.subject_replace_prefix.append(
                entry.kwargs['subject_replace_prefix'])

    def items(self) -> Iterable[tuple[Entity, Entry]]:
        return self.entries.items()

    def normalize_entity(self, entity: Entity) -> TTrm:
        for k, v in self.subject_replace_prefix:
            if entity.iri.value.startswith(v):
                return cast(Entity, entity.replace(
                    k + entity.iri.value.removeprefix(v)))
        return entity

    def normalize_value(
            self,
            value: Value,
            property: Optional[Property] = None
    ) -> TTrm:
        if value.is_entity():
            return self.normalize_entity(cast(Entity, value))
        else:
            return value
