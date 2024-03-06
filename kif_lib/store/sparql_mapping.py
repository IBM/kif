# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC

from .. import namespace as NS
from ..error import ShouldNotGetHere
from ..model import (
    Datatype,
    DataValue,
    Entity,
    ExternalId,
    IRI,
    Property,
    Quantity,
    String,
    T_IRI,
    Text,
    Time,
    Value,
)
from ..typing import Any, Callable, cast, NoReturn, Optional, TypeVar, Union
from .sparql_builder import SPARQL_Builder

T = TypeVar('T')
TTrm = SPARQL_Builder.TTrm
Variable = SPARQL_Builder.Variable


class SPARQL_Mapping(ABC):
    """Base class for SPARQL mappings."""

    class Builder(SPARQL_Builder):
        """SPARQL builder of SPARQL mapping."""

        #: The matched property.
        matched_property: TTrm

        #: The matched subject.
        matched_subject: TTrm

        #: The matched value.
        matched_value: TTrm

        #: The resulting property.
        property: Variable

        #: The resulting quantity amount (if any).
        qt_amount: Variable

        #: The resulting quantity lower bound (if any).
        qt_lower: Variable

        #: The resulting quantity unit (if any).
        qt_unit: Variable

        #: The resulting quantity upper bound (if any).
        qt_upper: Variable

        #: The resulting subject.
        subject: Variable

        #: The resulting time calendar model (if any).
        tm_calendar: Variable

        #: The resulting time precision (if any).
        tm_precision: Variable

        #: The resulting timezone (if any).
        tm_timezone: Variable

        #: The resulting time value (if any).
        tm_value: Variable

        #: The resulting simple value.
        value: Variable

        #: The resulting statement id.
        wds: Variable

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.matched_property = self.var('matched_property')
            self.matched_subject = self.var('matched_subject')
            self.matched_value = self.var('matched_value')
            self.property = self.var('property')
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

    class Spec:
        """A mapping specification in a SPARQL mapping."""

        #: Target property.
        property: Property

        #: Datatype of the target property.
        datatype: Datatype

        #: Function matching and mapping an (s,p,v) to the target property.
        definition: Callable[
            ['SPARQL_Mapping.Spec', SPARQL_Builder,
             TTrm, TTrm, TTrm], Optional[bool]]

        #: Extra keyword-arguments.
        kwargs: dict[str, Any]

        class Skip(Exception):
            """Skips the processing of the current specification."""

        @classmethod
        def skip(cls) -> NoReturn:
            """Skips the processing of the current specification."""
            raise cls.Skip

        @classmethod
        def _check(cls, v: T, test: Callable[[T], bool]) -> Union[T, NoReturn]:
            return v if test(v) else cls.skip()

        @classmethod
        def check_iri(cls, v: Value) -> IRI:
            """Checks whether `v` is an IRI value.

            Returns:
               `v`.

            Raises:
               Spec.Skip: `v` is not an IRI value.
            """
            return cast(IRI, cls._check(v, IRI.test))

        @classmethod
        def check_text(cls, v: Value) -> Text:
            """Checks whether `v` is a text value.

            Returns:
               `v`.

            Raises:
               Spec.Skip: `v` is not a text value.
            """
            return cast(Text, cls._check(v, Text.test))

        @classmethod
        def check_string(cls, v: Value) -> String:
            """Checks whether `v` is a string value.

            Returns:
               `v`.

            Raises:
               Spec.Skip: `v` is not a string value.
            """
            return cast(String, cls._check(v, String.test))

        @classmethod
        def check_external_id(cls, v: Value) -> ExternalId:
            """Checks whether `v` is an external id value.

            Returns:
               `v`.

            Raises:
               Spec.Skip: `v` is not an external id value.
            """
            return cast(ExternalId, cls._check(v, ExternalId.test))

        @classmethod
        def check_quantity(cls, v: Value) -> Quantity:
            """Checks whether `v` is a quantity value.

            Returns:
               `v`.

            Raises:
               Spec.Skip: `v` is not a quantity value.
            """
            return cast(Quantity, cls._check(v, Quantity.test))

        @classmethod
        def check_time(cls, v: Value) -> Time:
            """Checks whether `v` is a time value.

            Returns:
               `v`.

            Raises:
               Spec.Skip: `v` is not a time value.
            """
            return cast(Time, cls._check(v, Time.test))

        def __init__(
                self,
                property: Property,
                datatype: Datatype,
                definition: Callable[
                    ['SPARQL_Mapping.Spec', SPARQL_Builder,
                     TTrm, TTrm, TTrm], Optional[bool]],
                **kwargs: Any
        ):
            self.property = property
            self.datatype = datatype
            self.definition = definition
            self.kwargs = kwargs

        def _define(
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
            pname = NS.Wikidata.get_wikidata_name(self.property.iri.value)
            q.bind_uri(
                q.concat(String(str(NS.WD)), String(pname)), q.property)
            # wds
            q.bind_uri(q.concat(
                String(NS.WDS),
                q.md5(q.subject),
                String('_' + pname + '_'),
                q.md5(q.value)), q.wds)
            # value
            if issubclass(self.datatype.to_value_class(), Entity):
                q.bind_uri(
                    q.matched_value, q.value,
                    self.kwargs.get('value_replace_prefix', None))
            elif issubclass(self.datatype.to_value_class(), DataValue):
                value: Optional[TTrm] = None
                if self.datatype.is_quantity_datatype():
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
                elif self.datatype.is_string_datatype():
                    value = q.str_(q.matched_value)
                elif self.datatype.is_text_datatype():
                    lang = self.kwargs.get('value_set_language')
                    if (lang is not None
                            and isinstance(q.matched_value, Variable)):
                        value = q.strlang(q.matched_value, String(lang))
                    else:
                        value = q.matched_value
                elif self.datatype.is_time_datatype():
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

    @classmethod
    def register(
            cls,
            property: Property,
            datatype: Datatype,
            subject_prefix: Optional[T_IRI] = None,
            value_prefix: Optional[T_IRI] = None,
            **kwargs: Any
    ) -> Callable[..., Any]:
        """Decorator to register new specification into mapping.

        Parameters:
           property: Target property.
           datatype: Datatype of target property.
           subject_prefix: IRI prefix of target subject.
           value_prefix: IRI prefix of target value.
           kwargs: Extra keyword-arguments.

        Returns:
           A function that associates a definition a registers to a new
           mapping specification.
        """
        return lambda definition: cls._register(cls.Spec(
            Property._check_arg_property(
                property, cls.register, 'property', 1),
            Datatype._check_arg_datatype(
                datatype, cls.register, 'datatype', 2),
            definition,
            subject_prefix=IRI._check_optional_arg_iri(
                subject_prefix, None, cls.register, 'subject_prefix', 3),
            value_prefix=IRI._check_optional_arg_iri(
                value_prefix, None, cls.register, 'value_prefix', 4),
            **kwargs))

    @classmethod
    def _register(cls, spec: Spec):
        # Install prefix replacements, if any.
        for key in ['subject', 'value']:
            tgt = spec.kwargs[f'{key}_prefix']
            if tgt is None:
                continue
            src = cls.repls_inv[tgt]
            spec.kwargs[f'{key}_replace_prefix'] = (src.value, tgt.value)
        cls.specs[spec.property] = spec

    @classmethod
    def register_iri_prefix_replacement(cls, source: T_IRI, target: T_IRI):
        """Registers a prefix replacement into mapping.

        Parameters:
           source: Source IRI prefix as string.
           target: Target IRI prefix as string.
        """
        src = IRI._check_arg_iri(
            source, cls.register_iri_prefix_replacement, 'source', 1)
        tgt = IRI._check_arg_iri(
            target, cls.register_iri_prefix_replacement, 'target', 2)
        cls.repls[src] = tgt
        cls.repls_inv[tgt] = src

    @classmethod
    def normalize_entity(cls, entity: Entity) -> TTrm:
        for k, v in cls.repls.items():
            if entity.iri.value.startswith(v.value):
                return cast(Entity, entity.replace(
                    k.value + entity.iri.value.removeprefix(v.value)))
        return entity

    @classmethod
    def normalize_value(
            cls,
            value: Value,
            property: Optional[Property] = None
    ) -> TTrm:
        if value.is_entity():
            return cls.normalize_entity(cast(Entity, value))
        else:
            return value

    #: Specifications.
    specs: dict[Property, 'SPARQL_Mapping.Spec'] = dict()

    #: IRI prefix replacements.
    repls: dict[IRI, IRI] = dict()

    #: Inverse of IRI prefix replacements dict.
    repls_inv: dict[IRI, IRI] = dict()

    @classmethod
    def __init_subclass__(cls):
        from copy import deepcopy
        cls.specs = deepcopy(cls.__bases__[0].specs)
        cls.repls = deepcopy(cls.__bases__[0].repls)
        cls.repls_inv = deepcopy(cls.__bases__[0].repls)
