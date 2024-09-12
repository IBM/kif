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
    StatementTemplate,
    StatementVariable,
    Theta,
    Value,
    ValueSnak,
    VariablePattern,
    VEntity,
    VProperty,
    VStatement,
    VValue,
)
from ...model.fingerprint import FullFingerprint, ValueFingerprint
from ...typing import cast, Iterator, Mapping, override
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
    _entry_subst: dict[int, list[Substitution]]

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
        self._entry_qvar = self._q.fresh_var()

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
        # assert isinstance(filter.subject, (FullFingerprint, ValueFingerprint))
        # assert isinstance(filter.property, (FullFingerprint, ValueFingerprint))
        # assert isinstance(filter.value, (FullFingerprint, ValueFingerprint))
        with self._q.union():
            for source in self._filter_to_patterns(filter):
                for i, entry in enumerate(self.mapping):
                    theta = source.match(entry.pattern)
                    if theta is None:
                        continue  # nothing to do
                    saved_subst = self._theta
                    self._theta = Substitution()
                    target = source.instantiate(theta)
                    assert isinstance(
                        target, (Statement, StatementTemplate))
                    # ---
                    args: list[Query.VTerm] = []
                    for var in entry.pattern._iterate_variables():
                        val = var.instantiate(theta)
                        if var == val:
                            args.append(self._theta_add_as_qvar(var))
                        else:
                            self._theta_add(var, val)
                            args.append(self._as_simple_value(val))
                    # ----
                    self._q.stash_begin()
                    try:
                        with self._q.group():
                            self._q.bind(i, self._entry_qvar)
                            entry.callback(self, *args)
                    except entry.Skip:
                        self._q.stash_drop()
                    else:
                        self._q.stash_pop()
                        self._theta_add(self.pattern.variable, target)
                        if i not in self._entry_subst:
                            self._entry_subst[i] = []
                        self._entry_subst[i].append(self._theta)
                    self._theta = saved_subst

    def _binding_to_thetas(
            self,
            binding: Mapping[str, dict[str, str]]
    ) -> Iterator[Theta]:
        assert str(self._entry_qvar) in binding
        i = int(binding[str(self._entry_qvar)]['value'])
        for subst in self._entry_subst[i]:
            yield subst.instantiate(binding)

    def _filter_to_patterns(self, filter: Filter) -> Iterator[VStatement]:
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
