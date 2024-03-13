# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import logging

from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    Descriptor,
    Entity,
    FilterPattern,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    SnakSet,
    Statement,
    String,
    T_IRI,
    Value,
    ValueSnak,
)
from ..typing import (
    Any,
    cast,
    Collection,
    Iterable,
    Iterator,
    Optional,
    override,
    Union,
)
from .sparql import (
    BNode,
    NS,
    SPARQL_Builder,
    SPARQL_Results,
    SPARQL_Store,
    URIRef,
)
from .sparql_mapping import SPARQL_Mapping

LOG = logging.getLogger(__name__)


class SPARQL_MapperStore(
        SPARQL_Store,
        store_name='sparql-mapper',
        store_description='SPARQL endpoint mapper'):
    """SPARQL mapper store.

    Parameters:
       store_name: Store plugin to instantiate.
       iri: SPARQL endpoint IRI.
       mapping: SPARQL mapping.
    """

    _mapping: SPARQL_Mapping

    def __init__(
            self,
            store_name: str,
            iri: T_IRI,
            mapping: SPARQL_Mapping,
            **kwargs: Any
    ):
        assert store_name == self.store_name
        super().__init__(store_name, iri, **kwargs)
        self._mapping = KIF_Object._check_arg_isinstance(
            mapping, SPARQL_Mapping, self.__class__, 'mapping', 3)

    @property
    def mapping(self) -> SPARQL_Mapping:
        """SPARQL mapping."""
        return self.get_mapping()

    def get_mapping(self) -> SPARQL_Mapping:
        """Gets SPARQL mapping.

        Returns:
           SPARQL mapping.
        """
        return self._mapping

# -- Statements ------------------------------------------------------------

    @override
    def _count(self, pattern: FilterPattern) -> int:
        q = self._make_filter_query(pattern)
        text = q.select('(count (*) as ?count)')
        res = self._eval_select_query_string(text)
        return self._parse_count_query_results(res)

    @override
    def _make_filter_query(
            self,
            pat: FilterPattern,
    ) -> SPARQL_Builder:
        q = self.mapping.Builder()
        with q.where():
            subject_prefix: Optional[IRI] = None
            if pat.subject is not None:
                if pat.subject.entity is not None:
                    q.matched_subject = self.mapping.encode_entity(
                        pat.subject.entity)
                elif pat.subject.snak_set is not None:
                    status, subject_prefix = self._try_push_snak_set(
                        q, q.matched_subject, pat.subject.snak_set)
                    if not status:
                        return q  # empty query
                    assert subject_prefix is not None
                else:
                    raise self._should_not_get_here()
            value: Optional[Value] = None
            value_prefix: Optional[IRI] = None
            if pat.value is not None:
                if pat.value.value is not None:
                    value = pat.value.value
                    q.matched_value = self.mapping.encode_value(value)
                elif pat.value.snak_set is not None:
                    status, value_prefix = self._try_push_snak_set(
                        q, q.matched_value, pat.value.snak_set)
                    if not status:
                        return q  # empty query
                    assert value_prefix is not None
                else:
                    raise self._should_not_get_here()
            with q.union() as cup:
                for property, specs in self.mapping.specs.items():
                    for spec in specs:
                        if subject_prefix is not None:
                            if not spec._match_kwargs(
                                    'subject_prefix', subject_prefix):
                                continue  # subject mismatch
                        if value_prefix is not None:
                            if not spec._match_kwargs(
                                    'value_prefix', value_prefix):
                                continue  # value mismatch
                            value = spec.kwargs.get('value')
                            if value is not None:
                                if not Entity.test(value):
                                    continue  # value mismatch
                                if not value.value.startswith(
                                        value_prefix.value):
                                    continue  # mismatch value
                        if not spec._match(pat):
                            continue  # spec does not match pattern
                        cup.branch()
                        spec._define(q, with_binds=True)
        return q

    def _parse_filter_results_check_wds(
            self,
            entry: SPARQL_Results.Bindings,
            stmt: Statement
    ) -> Union[BNode, URIRef]:
        return NS.WDS[stmt.digest]

    def _try_push_snak_set(
            self,
            q: SPARQL_Builder,
            target: SPARQL_Builder.TTrm,
            snaks: SnakSet
    ) -> tuple[bool, Optional[IRI]]:
        subject_prefixes = set()
        for snak in snaks:
            if not snak.is_value_snak():
                return False, None  # no such snak
            vsnak = cast(ValueSnak, snak)
            if vsnak.property not in self.mapping.specs:
                return False, None  # no such property
            for spec in self.mapping.specs[vsnak.property]:
                pat = FilterPattern.from_snak(None, vsnak)
                if not spec._match(pat):
                    continue    # spec does not match snak
                spec._define(
                    cast(SPARQL_Mapping.Builder, q), target, None,
                    self.mapping.encode_value(vsnak.value))
                if spec.kwargs.get('subject_prefix') is not None:
                    subject_prefixes.add(spec.kwargs.get('subject_prefix'))
        if len(subject_prefixes) != 1:
            return False, None  # no such subject
        return True, next(iter(subject_prefixes))

# -- Annotations -----------------------------------------------------------

    def _get_annotations(
            self,
            stmts: Iterable[Statement],
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        for stmt in stmts:
            if self._cache_get_wdss(stmt):
                yield stmt, AnnotationRecordSet(AnnotationRecord())
            else:
                yield stmt, None

# -- Descriptors -----------------------------------------------------------

    def _make_item_or_property_descriptor_query(
            self,
            entities: Collection[Union[Item, Property]],
            cls: type[Entity],
            lang: str,
            mask: Descriptor.AttributeMask
    ) -> SPARQL_Builder:
        q = self.mapping.Builder()
        if self.has_flags(self.EARLY_FILTER):
            get_label = bool(mask & Descriptor.LABEL)
            get_aliases = bool(mask & Descriptor.ALIASES)
            get_description = bool(mask & Descriptor.DESCRIPTION)
        else:
            get_label = True
            get_aliases = True
            get_description = True
        with q.where():
            with q.optional(cond=get_label or get_aliases or get_description):
                with q.union() as cup:
                    label_specs: list[SPARQL_Mapping.Spec] =\
                        self.mapping.descriptor_specs.get(
                            Property('label'), [])
                    for spec in label_specs:
                        matched_entities = [
                            e for e in entities
                            if spec._match(FilterPattern(e))]
                        if not matched_entities:
                            continue
                        cup.branch()
                        spec._define(cast(SPARQL_Mapping.Builder, q))
                        lang = spec.kwargs.get('value_language', None)
                        if get_label:
                            if lang is not None:
                                q.bind(
                                    q.strlang(q.matched_value, String(lang)),
                                    q.var('label'))
                            else:
                                q.bind(q.matched_value, q.var('label'))
                        values = q.values(q.matched_subject, q.subject)
                        with values:
                            for entity in matched_entities:
                                values.push(
                                    self.mapping.encode_entity(entity),
                                    entity)
        return q

    def _make_lexeme_descriptor_query(
            self,
            lexemes: Collection[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> SPARQL_Builder:
        q = self.mapping.Builder()
        with q.where():
            pass
        return q
