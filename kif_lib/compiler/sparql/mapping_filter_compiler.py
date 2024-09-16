# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...model import (
    Entity,
    Filter,
    NoValueSnak,
    Property,
    SomeValueSnak,
    Statement,
    StatementVariable,
    Term,
    Theta,
    Value,
    ValueSnak,
    Variable,
    VariablePattern,
    VEntity,
    VProperty,
    VValue,
)
from ...model.fingerprint import ValueFingerprint
from ...typing import cast, Iterator, Mapping, override, Union
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
                    updt_args: list[Union[Term, Query.VTerm]] = []
                    for (var, val) in bindings.items():
                        ###
                        # TODO: What if var is not of a basic type (String,
                        # Quantity, etc.)?  Maybe we should skip the
                        # conversion and pass it unchanged to the entry
                        # callback.
                        ###
                        if isinstance(val, Variable):
                            updt_args.append(self._theta_add_as_qvar(var))
                        else:
                            self._theta_add(var, val)
                            assert isinstance(val, Value)
                            updt_args.append(self._as_simple_value(val))
                    self.q.stash_begin()
                    try:
                        with self.q.group():
                            self.q.bind(entry.id, self._entry_qvar)
                            entry.callback(self.mapping, self, *updt_args)
                    except self.mapping.Skip:
                        self.q.stash_drop()
                    else:
                        self.q.stash_pop()
                        self._theta_add(self.pattern.variable, target)
                        if id not in self._entry_subst:
                            self._entry_subst[entry.id] = []
                        self._entry_subst[entry.id].append(self._theta)
                    self._theta = saved_subst

    def _binding_to_thetas(
            self,
            binding: Mapping[str, dict[str, str]]
    ) -> Iterator[Theta]:
        assert str(self._entry_qvar) in binding
        id = binding[str(self._entry_qvar)]['value']
        for subst in self._entry_subst[id]:
            yield subst.instantiate(binding)

    def _filter_to_patterns(
            self,
            filter: Filter
    ) -> Iterator[SPARQL_Mapping.EntryPattern]:
        if isinstance(filter.subject, ValueFingerprint):
            subject: VEntity = cast(Entity, filter.subject.value)
        elif filter.subject_mask & filter.ITEM:
            subject = self._fresh_item_variable()
        elif filter.subject_mask & filter.PROPERTY:
            subject = self._fresh_property_variable()
        elif filter.subject_mask & filter.LEXEME:
            subject = self._fresh_lexeme_variable()
        elif filter.subject_mask & filter.ENTITY:
            subject = self._fresh_entity_variable()
        else:
            subject = self._fresh_entity_variable()
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
