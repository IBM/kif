# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

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
from ...typing import cast, Iterator, Mapping, override, Sequence
from .builder import Query
from .filter_compiler import SPARQL_FilterCompiler
from .mapping import SPARQL_Mapping
from .substitution import Substitution


class SPARQL_MappingFilterCompiler(SPARQL_FilterCompiler):
    """SPARQL Mapping - Filter Compiler """

    __slots__ = (
        '_mapping',
        '_entry_subst',
        '_entry_qvar',
    )

    # The SPARQL mapping.
    _mapping: SPARQL_Mapping

    #: The compiled substitutions for a given entry (identified by index).
    _entry_subst: dict[SPARQL_Mapping.EntryId, list[Substitution]]

    #: The query variable holding the index of the matched entry.
    _entry_qvar: Query.Variable

    def __init__(
            self,
            filter: Filter,
            mapping: SPARQL_Mapping,
            flags: SPARQL_FilterCompiler.Flags | None = None,
    ) -> None:
        super().__init__(filter, flags)
        self._mapping = mapping
        self._entry_subst = {}
        self._entry_qvar = self.q.fresh_var()

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

    @override
    def _push_filter(self, filter: Filter) -> None:
        assert isinstance(self.pattern, VariablePattern)
        assert isinstance(self.pattern.variable, StatementVariable)
        with self.q.union():
            for source in self._filter_to_patterns(filter):
                for target, bindings, entry in self.mapping.match(source):
                    saved_subst = self._theta
                    self._theta = Substitution()
                    self.q.stash_begin()
                    try:
                        with self.q.group():
                            self.q.bind(entry.id, self._entry_qvar)
                            entry.callback(
                                self.mapping, self,
                                *self._push_filter_get_entry_callback_args(
                                    entry, bindings))
                            self._push_filter_push_fps(entry, filter, target)
                    except self.mapping.Skip:
                        self.q.stash_drop()
                    else:
                        self._theta_add(self.pattern.variable, target)
                        self.q.stash_pop()
                        if id not in self._entry_subst:
                            self._entry_subst[entry.id] = []
                        self._entry_subst[entry.id].append(self._theta)
                    self._theta = saved_subst
        if not self._entry_subst:
            self._q = self.Query()  # empty query

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
        if not isinstance(target, (StatementTemplate, Statement)):
            return              # nothing to do
        # subject
        if isinstance(filter.subject, (CompoundFingerprint, SnakFingerprint)):
            self._push_fp(entry, filter.subject, target.subject)
        # snak
        if not isinstance(target.snak, (Snak, SnakTemplate)):
            return              # nothing to do
        if isinstance(filter.property, (CompoundFingerprint, SnakFingerprint)):
            self._push_fp(entry, filter.property, target.snak.property)
        if not isinstance(target.snak, (ValueSnak, ValueSnakTemplate)):
            return              # nothing to do
        if isinstance(filter.value, (CompoundFingerprint, SnakFingerprint)):
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
                self.q.comments()(f'{value} := {type(fp).__qualname__}')
                self._push_compound_fp(entry, fp, value)
        elif isinstance(fp, SnakFingerprint):
            with self.q.group():
                self.q.comments()(f'{value} := {fp}')
                assert isinstance(value, (
                    Entity, EntityTemplate, EntityVariable))
                self._push_snak_fp(entry, fp, value)
        elif isinstance(fp, ValueFingerprint):
            with self.q.group():
                self.q.comments()(f'{value} := {fp}')
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
        source = Statement(self._fresh_entity_variable(), fp.snak)
        with self.q.union():
            for _, bindings, target_entry in self.mapping.match(source):
                args = self._push_filter_get_entry_callback_args(
                    target_entry, bindings, False)
                if isinstance(fp, ConverseSnakFingerprint):
                    xargs = list(args)
                    assert len(xargs) == 2
                    args = reversed(xargs)
                with self.q.group():
                    target_entry.callback(self.mapping, self, *args)

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
            values = list(map(lambda v: (cast(
                Query.Literal | Query.URI, entry.preprocess(
                    self.mapping, self, var, self._as_simple_value(v))),),
                vs))
            if len(values) > 1 and use_values_clause:
                self.q.values(qvar)(*values)
            else:
                with self.q.union():
                    for (val,) in values:
                        with self.q.group():
                            self.q.bind(val, qvar)

    def _binding_to_thetas(
            self,
            binding: Mapping[str, dict[str, str]]
    ) -> Iterator[Theta]:
        if str(self._entry_qvar) in binding:
            id = binding[str(self._entry_qvar)]['value']
            for subst in self._entry_subst[id]:
                yield subst.instantiate(binding)

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
