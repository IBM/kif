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
    Value,
    ValueSnak,
    VariablePattern,
    VEntity,
    VProperty,
    VStatement,
    VValue,
)
from ...model.fingerprint import FullFingerprint, ValueFingerprint
from ...typing import cast, Iterator, override
from .filter_compiler import SPARQL_FilterCompiler
from .mapping import SPARQL_Mapping


class SPARQL_MappingFilterCompiler(SPARQL_FilterCompiler):
    """SPARQL Mapping - Filter Compiler """

    __slots__ = (
        '_mapping',
    )

    # The SPARQL mapping.
    _mapping: SPARQL_Mapping

    def __init__(
            self,
            filter: Filter,
            mapping: SPARQL_Mapping,
            flags: SPARQL_FilterCompiler.Flags | None = None,
    ) -> None:
        super().__init__(filter, flags)
        self._mapping = mapping

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
        assert isinstance(filter.subject, (FullFingerprint, ValueFingerprint))
        assert isinstance(filter.property, (FullFingerprint, ValueFingerprint))
        assert isinstance(filter.value, (FullFingerprint, ValueFingerprint))
        with self._q.union():
            for source in self._filter_to_patterns(filter):
                for entry in self.mapping:
                    theta = source.match(entry.pattern)
                    if theta is not None:
                        target = source.instantiate(theta)
                        self._q.stash_begin()
                        try:
                            with self._q.group():
                                entry.callback(entry, self, target)
                        except entry.Skip:
                            self._q.stash_drop()
                        else:
                            self._q.stash_pop()

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
                value: VValue = cast(Value, filter.value)
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
