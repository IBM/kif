# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import enum

from ... import itertools
from ...model import (
    AndFingerprint,
    CompoundFingerprint,
    ConverseSnakFingerprint,
    Entity,
    EntityTemplate,
    EntityVariable,
    Filter,
    Fingerprint,
    FullFingerprint,
    NoValueSnak,
    OrFingerprint,
    Property,
    Snak,
    SnakFingerprint,
    SnakTemplate,
    SomeValueSnak,
    Statement,
    StatementTemplate,
    StatementVariable,
    Term,
    Theta,
    Value,
    ValueFingerprint,
    ValueSnak,
    ValueSnakTemplate,
    Variable,
    VariablePattern,
    VEntity,
    VProperty,
    VStatement,
    VValue,
)
from ...typing import (
    Callable,
    cast,
    Final,
    Iterator,
    Mapping,
    override,
    Sequence,
)
from .builder import Query
from .filter_compiler import SPARQL_FilterCompiler
from .mapping import SPARQL_Mapping
from .substitution import Substitution


class SPARQL_MappingFilterCompiler(SPARQL_FilterCompiler):
    """SPARQL Mapping - Filter Compiler """

    class State(enum.Enum):

        #: Ready to compile.
        READY = enum.auto()

        #: Compiling filter.
        COMPILING_FILTER = enum.auto()

        #: Compiling fingerprint.
        COMPILING_FINGERPRINT = enum.auto()

        #: Done.
        DONE = enum.auto()

    #: Alias of :attr:`State.READY`.
    READY: Final[State] = State.READY

    #: Alias of :attr:`State.COMPILING_FILTER`.
    COMPILING_FILTER: Final[State] = State.COMPILING_FILTER

    #: Alias of :attr:`State.COMPILING_FINGERPRINT`.
    COMPILING_FINGERPRINT: Final[State] = State.COMPILING_FINGERPRINT

    #: Alias of :attr:`State.DONE'.
    DONE: Final[State] = State.DONE

    __slots__ = (
        '_mapping',
        '_entry_subst',
        '_entry_id_qvar',
        '_state',
        '_target',
    )

    # The SPARQL mapping.
    _mapping: SPARQL_Mapping

    #: The compiled substitutions for a given entry (identified by index).
    _entry_subst: dict[SPARQL_Mapping.EntryId, list[Substitution]]

    #: The query variable holding the index of the matched entry.
    _entry_id_qvar: Query.Variable

    #: The current state (accessible by mapping entries).
    _state: State

    #: The current target pattern (accessible by mapping entries).
    _target: SPARQL_Mapping.EntryPattern | None

    def __init__(
            self,
            filter: Filter,
            mapping: SPARQL_Mapping,
            flags: SPARQL_FilterCompiler.Flags | None = None,
    ) -> None:
        super().__init__(filter, flags)
        self._mapping = mapping
        self._entry_subst = {}
        self._entry_id_qvar = self.q.fresh_var()
        self._state = self.State.READY
        self._target = None

    @property
    def mapping(self) -> SPARQL_Mapping:
        """The SPARQL mapping."""
        return self.get_mapping()

    def get_mapping(self) -> SPARQL_Mapping:
        """Gets the SPARQL mapping.

        Returns:
           SPARQL mapping.
        """
        return self._mapping

    @property
    def state(self) -> SPARQL_MappingFilterCompiler.State:
        """The current state."""
        return self.get_state()

    def get_state(self) -> SPARQL_MappingFilterCompiler.State:
        """Gets the current state.

        Returns:
           State.
        """
        return self._state

    @property
    def target(self) -> SPARQL_Mapping.EntryPattern:
        """The current target pattern."""
        return self.get_target()

    def get_target(self) -> SPARQL_Mapping.EntryPattern:
        """Gets the current target pattern.

        Returns:
           Entry pattern.
        """
        assert self._target is not None
        return self._target

    def _fresh_name_generator(self) -> Callable[[str], Iterator[str]]:
        return (lambda _: map(
            lambda _: self.fresh_qvar(), itertools.repeat(None)))

    @override
    def _push_filter(self, filter: Filter) -> None:
        assert self._state == self.READY
        self._state = self.COMPILING_FILTER
        assert isinstance(self.pattern, VariablePattern)
        assert isinstance(self.pattern.variable, StatementVariable)
        sources = list(self._filter_to_patterns(filter))
        self.mapping.preamble(self, sources)
        targets = []
        with self.q.union():
            for source in sources:
                assert self._state == self.COMPILING_FILTER
                source = source.generalize(rename=self._fresh_name_generator())
                for entry in self.mapping.values():
                    m = entry.match(source)
                    if m is None:
                        continue  # nothing to do
                    target, bindings = m
                    self._target = target
                    saved_subst = self._theta
                    self._theta = Substitution()
                    for var, val in entry.default_map.items():
                        self._theta_add_default(var, val)
                    self.q.stash_begin()
                    try:
                        with self.q.group():
                            self.q.bind(entry.id, self._entry_id_qvar)
                            args = self._push_filter_get_entry_callback_args(
                                entry, bindings)
                            entry.callback(self.mapping, self, *args)
                            self._state = self.COMPILING_FINGERPRINT
                            self._push_filter_push_fps(entry, filter, target)
                    except self.mapping.Skip:
                        self.q.stash_drop()
                    else:
                        self._theta_add(self.pattern.variable, target)
                        self.q.stash_pop()
                        if id not in self._entry_subst:
                            self._entry_subst[entry.id] = []
                        self._entry_subst[entry.id].append(self._theta)
                        targets.append(target)
                    self._state = self.COMPILING_FILTER
                    self._theta = saved_subst
                    self._target = None
        if not self._entry_subst:
            self._q = self.Query()  # empty query
        self.mapping.postamble(self, targets)
        self._state = self.DONE

    def _push_filter_get_entry_callback_args(
            self,
            entry: SPARQL_Mapping.Entry,
            bindings: Theta,
            add_to_subst: bool = True
    ) -> Iterator[Term | Query.VTerm | None]:
        for (var, val) in bindings.items():
            res: Term | Query.VTerm | None
            if isinstance(val, self._primitve_var_classes):
                qvar = self.as_qvar(cast(Variable, val))
                if add_to_subst:
                    self._theta_add(var, qvar)
                res = qvar
            elif isinstance(val, Value):
                if add_to_subst:
                    self._theta_add(var, val)
                res = self._as_simple_value(val)
            else:
                res = val       # keep it as is
            yield entry.preprocess(self.mapping, self, var, res)

    def _push_filter_push_fps(
            self,
            entry: SPARQL_Mapping.Entry,
            filter: Filter,
            target: VStatement
    ) -> None:
        assert isinstance(target, (StatementTemplate, Statement))
        # subject
        if isinstance(filter.subject, (CompoundFingerprint, SnakFingerprint)):
            self._push_fp(entry, filter.subject, target.subject)
        # snak
        assert isinstance(target.snak, (Snak, SnakTemplate))
        if isinstance(filter.property, (CompoundFingerprint, SnakFingerprint)):
            self._push_fp(entry, filter.property, target.snak.property)
        # value
        if (isinstance(target.snak, (ValueSnak, ValueSnakTemplate))
            and isinstance(filter.value, (
                CompoundFingerprint, SnakFingerprint))):
            self._push_fp(entry, filter.value, target.snak.value)

    def _push_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: Fingerprint,
            value: VValue
    ) -> None:
        if isinstance(value, Value) and not fp.match(value):
            raise SPARQL_Mapping.Skip  # fail
        if isinstance(fp, CompoundFingerprint):
            with self.q.group():
                if self.has_flags(self.DEBUG):
                    self.q.comments()(f'{value} =~ {type(fp).__qualname__}')
                self._push_compound_fp(entry, fp, value)
        elif isinstance(fp, SnakFingerprint):
            with self.q.group():
                if self.has_flags(self.DEBUG):
                    self.q.comments()(f'{value} =~ {fp}')
                assert isinstance(value, (
                    Entity, EntityTemplate, EntityVariable))
                self._push_snak_fp(entry, fp, value)
        elif isinstance(fp, ValueFingerprint):
            with self.q.group():
                if self.has_flags(self.DEBUG):
                    self.q.comments()(f'{value} =~ {fp}')
                raise NotImplementedError
        elif isinstance(fp, FullFingerprint):
            pass
        else:
            raise self._should_not_get_here()

    def _push_compound_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: CompoundFingerprint,
            value: VValue
    ) -> None:
        atoms, comps = map(list, itertools.partition(
            lambda x: isinstance(x, CompoundFingerprint), fp.args))
        snaks, values = map(list, itertools.partition(
            lambda x: isinstance(x, ValueFingerprint), atoms))
        if isinstance(fp, AndFingerprint):
            assert len(values) <= 1
            for child in itertools.chain(snaks, comps):
                self._push_fp(entry, child, value)
            if values:
                with self.q.group():
                    self._push_value_fps(entry, values, value, False)
        elif isinstance(fp, OrFingerprint):
            with self.q.union():
                for child in itertools.chain(snaks, comps):
                    with self.q.group():
                        self._push_fp(entry, child, value)
                if values:
                    with self.q.group():
                        self._push_value_fps(entry, values, value, False)
        else:
            raise self._should_not_get_here()

    def _push_snak_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: SnakFingerprint,
            entity: VEntity
    ) -> None:
        if isinstance(fp, ConverseSnakFingerprint):
            assert isinstance(fp.snak, ValueSnak)
            assert isinstance(fp.snak.value, Entity)
            source = fp.snak.property(fp.snak.value, entity)
        else:
            source = Statement(entity, fp.snak)
        with self.q.union():
            for target_entry in self.mapping.values():
                target_entry = target_entry.rename(
                    rename=self._fresh_name_generator())
                m = target_entry.match(source)
                if m is None:
                    continue
                target, bindings = m
                assert isinstance(target, (Statement, StatementTemplate))
                saved_target = self._target
                self._target = target
                try:
                    args = list(self._push_filter_get_entry_callback_args(
                        target_entry, bindings, False))
                    with self.q.group():
                        target_entry.callback(self.mapping, self, *args)
                        ###
                        # Determine the target entity (subject or value?).
                        ###
                        if isinstance(fp, ConverseSnakFingerprint):
                            assert isinstance(
                                target_entry.pattern.snak,
                                (ValueSnak, ValueSnakTemplate))
                            assert isinstance(
                                target_entry.pattern.snak.value,
                                (EntityTemplate, EntityVariable))
                            target_entity = target_entry.pattern.snak.value
                        else:
                            target_entity = target_entry.pattern.subject
                        assert isinstance(
                            target_entity, (EntityTemplate, EntityVariable))
                        ###
                        # Determine and replace ?src by ?tgt in this group.
                        ###
                        src = self.as_qvar(next(entity._iterate_variables()))
                        if isinstance(target_entity, Entity):
                            tgt: Query.VTerm = self._as_simple_value(
                                target_entity)
                            raise NotImplementedError
                        else:
                            tgt = self.as_qvar(next(
                                target_entity._iterate_variables()))
                        self.q.bind(tgt, src)
                except self.mapping.Skip as err:
                    raise err
                finally:
                    self._target = saved_target

    def _push_value_fps(
            self,
            entry: SPARQL_Mapping.Entry,
            fps: Sequence[ValueFingerprint],
            value: VValue,
            use_values_clause: bool = True
    ) -> None:
        assert bool(fps)
        if isinstance(value, Value):
            return              # nothing to do
        thetas: list[Theta] =\
            list(filter(lambda t: t is not None, map(  # type: ignore
                value.match, map(
                    ValueFingerprint.get_value, fps))))
        if not thetas:
            raise SPARQL_Mapping.Skip  # fail
        accum: dict[Variable, list[Value]] = {}
        for theta in thetas:
            for k, v in theta.items():
                assert isinstance(v, Value)
                if k in accum:
                    accum[k].append(v)
                else:
                    accum[k] = [v]
        for var, vs in accum.items():
            assert isinstance(var, self._primitve_var_classes)
            qvar = self.as_qvar(var)
            values = list(self._push_value_fps_preprocess(entry, var, vs))
            ###
            # FIXME: Handle the case where len(values) == 0.
            ###
            assert len(values) > 0
            if len(values) > 1 and use_values_clause:
                self.q.values(qvar)(*map(lambda x: (x,), values))
            else:
                with self.q.union():
                    for val in values:
                        with self.q.group():
                            self.q.bind(val, qvar)

    def _push_value_fps_preprocess(
            self,
            entry: SPARQL_Mapping.Entry,
            variable: Variable,
            values: list[Value]
    ) -> Iterator[Query.Literal | Query.URI]:
        for value in values:
            try:
                yield cast(Query.Literal | Query.URI,
                           entry.preprocess(
                               self.mapping, self, variable,
                               self._as_simple_value(value)))
            except SPARQL_Mapping.Skip:
                continue

    def _binding_to_thetas(
            self,
            binding: Mapping[str, dict[str, str]]
    ) -> Iterator[Theta]:
        if str(self._entry_id_qvar) in binding:
            id = binding[str(self._entry_id_qvar)]['value']
            entry = self._mapping[id]
            for var in entry.postprocess_map:
                if var.name in binding:
                    try:
                        term = entry.postprocess(
                            self.mapping, self, var,
                            self._dict2term(binding[var.name]))
                    except SPARQL_Mapping.Skip:
                        return
                    else:
                        assert isinstance(term, (Query.Literal, Query.URI))
                        assert isinstance(binding, dict)
                        binding[var.name] = self._term2dict(term)
            for subst in self._entry_subst[id]:
                theta = subst.instantiate(binding)
                yield theta

    def _dict2term(self, t: dict[str, str]) -> Query.Term:
        assert 'type' in t
        if t['type'] == 'uri':
            return Query.URI(t['value'])
        elif t['type'] == 'literal':
            ###
            # TODO: Handle language and datatype.
            ###
            return Query.Literal(t['value'])
        else:
            raise NotImplementedError

    def _term2dict(self, term: Query.Term) -> dict[str, str]:
        if isinstance(term, Query.URI):
            return {'type': 'uri', 'value': str(term)}
        elif isinstance(term, Query.Literal):
            ###
            # TODO: Handle language and datatype.
            ###
            assert term.language is None
            assert term.datatype is None
            return {'type': 'literal', 'value': str(term)}
        else:
            raise NotImplementedError

    def _filter_to_patterns(
            self,
            filter: Filter
    ) -> Iterator[SPARQL_Mapping.EntryPattern]:
        if isinstance(filter.subject, ValueFingerprint):
            subject: VEntity = cast(Entity, filter.subject.value)
        elif filter.subject_mask == filter.ITEM:
            subject = self._fresh_item_variable()
        elif filter.subject_mask == filter.PROPERTY:
            subject = self._fresh_property_variable()
        elif filter.subject_mask == filter.LEXEME:
            subject = self._fresh_lexeme_variable()
        elif filter.subject_mask == filter.ENTITY:
            subject = self._fresh_entity_variable()
        else:
            raise self._should_not_get_here()
        if isinstance(filter.property, ValueFingerprint):
            property: VProperty = cast(Property, filter.property.value)
        else:
            property = self._fresh_property_variable()
        if filter.snak_mask & filter.VALUE_SNAK:
            assert bool(filter.value_mask)
            if isinstance(filter.value, ValueFingerprint):
                value: VValue = cast(Value, filter.value.value)
            elif filter.value_mask == filter.ITEM:
                value = self._fresh_item_variable()
            elif filter.value_mask == filter.PROPERTY:
                value = self._fresh_property_variable()
            elif filter.value_mask == filter.LEXEME:
                value = self._fresh_lexeme_variable()
            elif filter.value_mask == filter.DATA_VALUE:
                value = self._fresh_data_value_variable()
            elif filter.value_mask == filter.SHALLOW_DATA_VALUE:
                value = self._fresh_shallow_data_value_variable()
            elif filter.value_mask == filter.IRI:
                value = self._fresh_iri_variable()
            elif filter.value_mask == filter.TEXT:
                value = self._fresh_text_variable()
            elif filter.value_mask == filter.STRING:
                value = self._fresh_string_variable()
            elif filter.value_mask == filter.EXTERNAL_ID:
                value = self._fresh_external_id_variable()
            elif filter.value_mask == filter.DEEP_DATA_VALUE:
                value = self._fresh_deep_data_value_variable()
            elif filter.value_mask == filter.QUANTITY:
                value = self._fresh_quantity_variable()
            elif filter.value_mask == filter.TIME:
                value = self._fresh_time_variable()
            else:
                value = self._fresh_value_variable()
            yield Statement(subject, ValueSnak(property, value))
        if filter.snak_mask & filter.SOME_VALUE_SNAK:
            yield Statement(subject, SomeValueSnak(property))
        if filter.snak_mask & filter.NO_VALUE_SNAK:
            yield Statement(subject, NoValueSnak(property))
