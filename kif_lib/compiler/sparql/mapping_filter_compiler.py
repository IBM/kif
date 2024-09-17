# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ... import itertools
from ...model import (
    Entity,
    Filter,
    Fingerprint,
    IRI_Variable,
    NoValueSnak,
    Property,
    QuantityVariable,
    Snak,
    SnakTemplate,
    SomeValueSnak,
    Statement,
    StatementTemplate,
    StatementVariable,
    StringVariable,
    Term,
    Theta,
    TimeVariable,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    Variable,
    VariablePattern,
    VEntity,
    VProperty,
    VStatement,
    VValue,
)
from ...model.fingerprint import (
    AndFingerprint,
    CompoundFingerprint,
    FullFingerprint,
    OrFingerprint,
    SnakFingerprint,
    ValueFingerprint,
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
                                    bindings))
                            self._push_filter_push_fps(filter, target)
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
            bindings: Theta,
            add_to_subst: bool = True,
            _var_qvar: tuple[type[Variable], ...] = (
                IRI_Variable, QuantityVariable, StringVariable, TimeVariable)
    ) -> Iterator[Term | Query.VTerm | None]:
        for (var, val) in bindings.items():
            if isinstance(val, _var_qvar):
                qvar = self.as_qvar(cast(Variable, val))
                if add_to_subst:
                    self._theta_add(var, qvar)
                yield qvar
            elif isinstance(val, Value):
                if add_to_subst:
                    self._theta_add(var, val)
                yield self._as_simple_value(val)
            else:
                yield val       # keep it as is

    def _push_filter_push_fps(
            self,
            filter: Filter,
            target: VStatement
    ) -> None:
        if not isinstance(target, (StatementTemplate, Statement)):
            return              # nothing to do
        # subject
        if isinstance(filter.subject, (CompoundFingerprint, SnakFingerprint)):
            self._push_fp(filter.subject, target.subject)
        # snak
        if not isinstance(target.snak, (Snak, SnakTemplate)):
            return              # nothing to do
        if isinstance(filter.property, (CompoundFingerprint, SnakFingerprint)):
            self._push_fp(filter.property, target.snak.property)
        if not isinstance(target.snak, (ValueSnak, ValueSnakTemplate)):
            return              # nothing to do
        if isinstance(filter.value, (CompoundFingerprint, SnakFingerprint)):
            self._push_fp(filter.value, target.snak.value)

    def _push_fp(self, fp: Fingerprint, v: VValue) -> None:
        if isinstance(v, Value) and not fp.match(v):
            raise SPARQL_Mapping.Skip  # fail
        if isinstance(fp, CompoundFingerprint):
            self._push_compound_fp(fp, v)
        elif isinstance(fp, SnakFingerprint):
            raise NotImplementedError
        elif isinstance(fp, ValueFingerprint):
            raise NotImplementedError
        elif isinstance(fp, FullFingerprint):
            pass
        else:
            raise self._should_not_get_here()

    def _push_compound_fp(self, fp: CompoundFingerprint, v: VValue) -> None:
        atoms, comps = map(list, itertools.partition(
            lambda x: isinstance(x, CompoundFingerprint), fp.args))
        snaks, values = map(list, itertools.partition(
            lambda x: isinstance(x, ValueFingerprint), atoms))
        if isinstance(fp, AndFingerprint):
            raise NotImplementedError
        elif isinstance(fp, OrFingerprint):
            if values:
                self._push_values_fps(values, v)
        else:
            raise self._should_not_get_here()

    def _push_values_fps(
            self,
            fps: Sequence[ValueFingerprint],
            v: VValue
    ) -> None:
        assert bool(fps)
        if isinstance(v, Value):
            return              # nothing to do
        # thetas = list(filter(lambda t: t is not None, map(v.match, map(
        #     ValueFingerprint.get_value, fps))))
        # print(thetas)
        # for theta in map(v.match, map(ValueFingerprint.get_value, fps)):
        #     for k, v in theta.items():
        #         print(k, v)
        raise NotImplementedError

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
            elif filter.value_mask == filter.VALUE:
                value = self._fresh_value_variable()
            else:
                raise self._should_not_get_here()
            yield Statement(subject, ValueSnak(property, value))
        if filter.snak_mask & filter.SOME_VALUE_SNAK:
            yield Statement(subject, SomeValueSnak(property))
        if filter.snak_mask & filter.NO_VALUE_SNAK:
            yield Statement(subject, NoValueSnak(property))
