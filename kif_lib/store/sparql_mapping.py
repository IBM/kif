# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC

from .. import namespace as NS
from ..error import ShouldNotGetHere
from ..model import (
    AnnotationRecordSet,
    Datatype,
    DataValue,
    Entity,
    ExternalId,
    FilterPattern,
    IRI,
    Property,
    Quantity,
    Snak,
    Statement,
    String,
    T_IRI,
    Text,
    TextDatatype,
    Time,
    Value,
)
from ..store.abc import Store
from ..typing import (
    Any,
    Callable,
    cast,
    Iterable,
    Iterator,
    NoReturn,
    Optional,
    TypeVar,
    Union,
)
from .sparql_builder import SPARQL_Builder

T = TypeVar('T')
TTrm = SPARQL_Builder.TTrm
Variable = SPARQL_Builder.Variable


class SPARQL_Mapping(ABC):
    """Base class for SPARQL mappings."""

# -- Builder ---------------------------------------------------------------

    class Builder(SPARQL_Builder):
        """SPARQL builder of SPARQL mapping."""

        #: The matched (encoded) subject.
        matched_subject: TTrm

        #: The matched (encoded) property.
        matched_property: TTrm

        #: The matched (encoded) value.
        matched_value: TTrm

        #: The resulting (decoded) subject.
        subject: Variable

        #: The resulting (decoded) property.
        property: Variable

        #: The resulting (decoded) simple value.
        value: Variable

        #: The resulting (decoded) quantity amount.
        qt_amount: Variable

        #: The resulting (decoded) quantity unit.
        qt_unit: Variable

        #: The resulting (decoded) quantity lower bound.
        qt_lower: Variable

        #: The resulting (decoded) quantity upper bound.
        qt_upper: Variable

        #: The resulting (decoded) time value.
        tm_value: Variable

        #: The resulting (decoded) time precision.
        tm_precision: Variable

        #: The resulting (decoded) timezone.
        tm_timezone: Variable

        #: The resulting (decoded) time calendar model.
        tm_calendar: Variable

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.matched_subject = self.var('matched_subject')
            self.matched_property = self.var('matched_property')
            self.matched_value = self.var('matched_value')
            self.subject = self.var('subject')
            self.property = self.var('property')
            self.value = self.var('value')
            self.qt_amount = self.var('qt_amount')
            self.qt_unit = self.var('qt_unit')
            self.qt_lower = self.var('qt_lower')
            self.qt_upper = self.var('qt_upper')
            self.tm_value = self.var('tm_value')
            self.tm_precision = self.var('tm_precision')
            self.tm_timezone = self.var('tm_timezone')
            self.tm_calendar = self.var('tm_calendar')

        def bind_uri(
                self,
                term: TTrm,
                var: Variable,
                replace_prefix: Optional[tuple[str, str]] = None
        ) -> 'SPARQL_Mapping.Builder':
            """Binds URI term to variable.

            If `replace_prefix` is not ``None``, applies replacement before
            binding the term.

            Parameters:
               term: URI term.
               var: Variable.

            Returns:
               `self`.
            """
            if replace_prefix is not None:
                pfx, by = replace_prefix
                q = self.bind(self.uri(self.concat(
                    String(str(by)),
                    self.substr(self.str_(term), len(str(pfx)) + 1))), var)
            else:
                q = self.bind(self.uri(term), var)
            return cast(SPARQL_Mapping.Builder, q)

# -- Mapping spec. ---------------------------------------------------------

    class Spec:
        """A mapping specification (spec.) in a SPARQL mapping."""

        class Skip(Exception):
            """Skips the processing of the current spec."""

        @classmethod
        def skip(cls) -> NoReturn:
            """Skips the processing of the current spec."""
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

        #: The (decoded) property being mapped.
        property: Property

        #: The datatype of the property being mapped.
        datatype: Datatype

        #: The function that expands to the definition of the mapping.
        definition: Callable[
            ['SPARQL_Mapping.Spec', SPARQL_Builder,
             TTrm, TTrm, TTrm], Optional[bool]]

        #: The other keyword-arguments of spec.
        kwargs: dict[str, Any]

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
                self.kwargs.get('subject_prefix_replacement', None))
            # property
            pname = NS.Wikidata.get_wikidata_name(self.property.iri.value)
            q.bind_uri(
                q.concat(String(str(NS.WD)), String(pname)), q.property)
            # value
            if self.kwargs.get('value') is not None:
                fixed_value = self.kwargs.get('value')
                assert fixed_value is not None
                if isinstance(q.matched_value, Variable):
                    q.bind(fixed_value, q.matched_value)
            if issubclass(self.datatype.to_value_class(), Entity):
                q.bind_uri(
                    q.matched_value, q.value,
                    self.kwargs.get('value_prefix_replacement', None))
            elif issubclass(self.datatype.to_value_class(), DataValue):
                value: Optional[TTrm] = None
                dt = self.kwargs.get('value_datatype')
                if dt is not None and isinstance(q.matched_value, Variable):
                    value = q.strdt(q.matched_value, dt)
                else:
                    value = q.matched_value
                if self.datatype.is_iri_datatype():
                    pass        # nothing to do
                elif self.datatype.is_string_datatype():
                    value = q.str_(q.matched_value)
                elif self.datatype.is_text_datatype():
                    lang = self.kwargs.get('value_language')
                    if (lang is not None
                            and isinstance(q.matched_value, Variable)):
                        value = q.strlang(q.matched_value, String(lang))
                    else:
                        value = q.matched_value
                elif self.datatype.is_quantity_datatype():
                    q.bind(value, q.qt_amount)
                    unit = self.kwargs.get('value_unit')
                    if unit is not None:
                        q.bind(unit, q.qt_unit)
                elif self.datatype.is_time_datatype():
                    q.bind(value, q.tm_value)
                    prec = self.kwargs.get('value_precision')
                    if prec is not None:
                        q.bind(prec.value, q.tm_precision)
                    tz = self.kwargs.get('value_timezone')
                    if tz is not None:
                        q.bind(tz, q.tm_timezone)
                    cal = self.kwargs.get('value_calendar')
                    if cal is not None:
                        q.bind(cal, q.tm_calendar)
                else:
                    raise ShouldNotGetHere
                assert value is not None
                q.bind(value, q.value)
            else:
                raise ShouldNotGetHere

        def _match(self, pat: FilterPattern) -> bool:
            # Property mismatch.
            if (pat.property is not None
                    and pat.property.property != self.property):
                return False
            # Subject mismatch.
            if pat.subject is not None and pat.subject.entity is not None:
                subject = pat.subject.entity
                assert subject is not None
                if not self._match_kwargs(
                        'subject_prefix', subject.value,
                        lambda x, y: x.startswith(y.value)):
                    return False
            # Snak mask mismatch.
            if not (pat.snak_mask & Snak.VALUE_SNAK):
                return False
            # Value mismatch.
            if pat.value is not None:
                value_class = self.datatype.to_value_class()
                if pat.value.value is not None:
                    value = pat.value.value
                    assert value is not None
                    if not value_class.test(value):
                        return False
                    if self.kwargs.get('value') is not None:
                        if self.kwargs.get('value') != value:
                            return False
                    if issubclass(value_class, Entity):
                        if not self._match_kwargs(
                                'value_prefix', value.value,
                                lambda x, y: x.startswith(y.value)):
                            return False
                    elif value_class is Text:
                        text = cast(Text, value)
                        if not self._match_kwargs(
                                'value_language', text.language):
                            return False
                    elif value_class is Quantity:
                        qt = cast(Quantity, value)
                        if (qt.unit is not None and not self._match_kwargs(
                                'value_unit', qt.unit)):
                            return False
                        if qt.lower_bound is not None:
                            return False
                        if qt.upper_bound is not None:
                            return False
                    elif value_class is Time:
                        tm = cast(Time, value)
                        if (tm.precision is not None
                            and not self._match_kwargs(
                                'value_precision', tm.precision)):
                            return False
                        if (tm.timezone is not None
                            and not self._match_kwargs(
                                'value_timezone', tm.timezone)):
                            return False
                        if (tm.calendar is not None
                            and not self._match_kwargs(
                                'value_calendar', tm.calendar)):
                            return False
                elif pat.value.snak_set is not None:
                    if not issubclass(value_class, Entity):
                        return False
            # Success.
            return True

        def _match_kwargs(
                self,
                k: str,
                v: Any,
                cmp: Callable[[Any, Any], bool] = (lambda x, y: x == y)
        ) -> bool:
            if k not in self.kwargs:
                return True
            elif self.kwargs[k] is None:
                return True
            else:
                return cmp(v, self.kwargs[k])


# -- Mapping ---------------------------------------------------------------

    #: The registered specs.
    specs: dict[Property, list['SPARQL_Mapping.Spec']]

    #: The registered descriptor specs.
    descriptor_specs: dict[Property, list['SPARQL_Mapping.Spec']]

    #: The registered IRI prefix replacements "(encoded, decoded)".
    iri_prefix_replacements: dict[IRI, IRI]

    #: Inverse of IRI prefix replacements dict.
    iri_prefix_replacements_inv: dict[IRI, IRI]

    @classmethod
    def __init_subclass__(cls):
        cls._init()

    @classmethod
    def _init(cls):
        cls.specs = dict()
        cls.descriptor_specs = dict()
        cls.iri_prefix_replacements = dict()
        cls.iri_prefix_replacements_inv = dict()

    @classmethod
    def register(
            cls,
            property: Property,
            datatype: Datatype,
            **kwargs: Any
    ) -> Callable[..., Any]:
        """Decorator used to register a new specification into mapping.

        Parameters:
           property: Property.
           datatype: Datatype of property.
           kwargs: Keyword-arguments to be passed to :class:`Spec`.

        Returns:
           A function that takes a definition and associates it with
           new spec in mapping.
        """
        property = Property._check_arg_property(
            property, cls.register, 'property', 1)
        datatype = Datatype._check_arg_datatype(
            datatype, cls.register, 'datatype', 2)
        return lambda definition: cls._register(cls.specs, cls.Spec(
            property, datatype, definition, **kwargs))

    @classmethod
    def register_label(cls, **kwargs: Any) -> Callable[..., Any]:
        return lambda definition: cls._register(
            cls.descriptor_specs, cls.Spec(
                Property('label'), TextDatatype(), definition, **kwargs))

    @classmethod
    def register_alias(cls, **kwargs: Any) -> Callable[..., Any]:
        return lambda definition: cls._register(
            cls.descriptor_specs, cls.Spec(
                Property('alias'), TextDatatype(), definition, **kwargs))

    @classmethod
    def register_description(cls, **kwargs: Any) -> Callable[..., Any]:
        return lambda definition: cls._register(
            cls.descriptor_specs, cls.Spec(
                Property('description'), TextDatatype(),
                definition, **kwargs))

    @classmethod
    def _register(
            cls,
            specs: dict[Property, list['SPARQL_Mapping.Spec']],
            spec: Spec):
        # IRI prefix replacements.
        for key in ['subject', 'value']:
            tgt = spec.kwargs.get(f'{key}_prefix', None)
            if tgt is None:
                continue
            src = cls.iri_prefix_replacements_inv[tgt]
            spec.kwargs[f'{key}_prefix_replacement'] = (src.value, tgt.value)
        if spec.property not in specs:
            specs[spec.property] = list()
        specs[spec.property].append(spec)

    @classmethod
    def register_iri_prefix_replacement(cls, encoded: T_IRI, decoded: T_IRI):
        """Registers prefix replacement into mapping.

        Parameters:
           encoded: IRI.
           decoded: IRI.
        """
        encoded = IRI._check_arg_iri(
            encoded, cls.register_iri_prefix_replacement, 'encoded', 1)
        decoded = IRI._check_arg_iri(
            decoded, cls.register_iri_prefix_replacement, 'decoded', 2)
        cls.iri_prefix_replacements[encoded] = decoded
        cls.iri_prefix_replacements_inv[decoded] = encoded

    @classmethod
    def encode_entity(cls, entity: Entity) -> TTrm:
        """Encodes entity using mapping.

        Parameters:
           entity: Entity.

        Returns:
           The resulting term.
        """
        for k, v in cls.iri_prefix_replacements.items():
            if entity.iri.value.startswith(v.value):
                return cast(Entity, entity.replace(
                    k.value + entity.iri.value.removeprefix(v.value)))
        return entity

    @classmethod
    def encode_value(cls, value: Value) -> TTrm:
        """Encodes value using mapping.

        Parameters:
           value: Value.

        Returns:
           The resulting term.
        """
        if value.is_entity():
            return cls.encode_entity(cast(Entity, value))
        else:
            return value

# -- Hooks -----------------------------------------------------------------

    @classmethod
    def filter_pre_hook(
            cls,
            store: Store,
            pattern: FilterPattern,
            limit: int,
            distinct: bool
    ) -> tuple[FilterPattern, int, bool, Any]:
        return pattern, limit, distinct, None

    @classmethod
    def filter_post_hook(
            cls,
            store: Store,
            pattern: FilterPattern,
            limit: int,
            distinct: bool,
            data: Any,
            it: Iterator[Statement]
    ) -> Iterator[Statement]:
        return it

    @classmethod
    def get_annotations_pre_hook(
            cls,
            store: Store,
            stmts: Iterable[Statement]
    ) -> tuple[Iterable[Statement], Any]:
        return stmts, None

    @classmethod
    def get_annotations_post_hook(
            self,
            store: Store,
            stmts: Iterable[Statement],
            data: Any,
            it: Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        return it
