# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging

from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    Descriptor,
    Entity,
    ExternalIdDatatype,
    Filter,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    SnakSet,
    Statement,
    T_IRI,
    Value,
    ValueSnak,
)
from ..namespace import WD
from ..typing import (
    Any,
    cast,
    Collection,
    Final,
    Iterable,
    Iterator,
    override,
    Sequence,
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
    ) -> None:
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
    def _contains(self, filter: Filter) -> bool:
        it = self._filter_with_hooks(filter, 1, False)
        try:
            next(it)
            return True
        except StopIteration:
            return False

    @override
    def _count(self, filter: Filter) -> int:
        q = self._make_filter_query(filter)
        text = q.select('(count (distinct *) as ?count)')
        res = self._eval_select_query_string(text)
        return self._parse_count_query_results(res)

    def _parse_count_query_results(self, results: SPARQL_Results) -> int:
        return int(next(results.bindings).check_literal('count'))

    _filter_vars: Final[Sequence[str]] = (
        '?datatype',
        '?property',
        '?qt_amount',
        '?qt_lower',
        '?qt_unit',
        '?qt_upper',
        '?subject',
        '?tm_calendar',
        '?tm_precision',
        '?tm_timezone',
        '?tm_value',
        '?value',
        '?wds',
    )

    @override
    def _filter(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        assert limit > 0
        if filter.value.is_empty():
            return iter(())
        q = self._make_filter_query(filter)
        if (q.has_variable(q.var('subject'))
                and q.has_variable(q.var('property'))):
            order_by = '?wds' if self.has_flags(self.ORDER) else None
            return self._eval_select_query(
                q, lambda res: self._parse_filter_results(res, filter),
                vars=self._filter_vars,
                limit=limit, distinct=distinct, order_by=order_by, trim=True)
        else:
            LOG.debug(
                '%s(): nothing to select:\n%s', self._filter.__qualname__,
                q.select(*self._filter_vars, limit=limit, distinct=distinct))
            return iter(())     # query is empty

    @override
    def _filter_pre_hook(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> tuple[Filter, int, bool, Any]:
        return self.mapping.filter_pre_hook(self, filter, limit, distinct)

    @override
    def _filter_post_hook(
            self,
            filter: Filter,
            limit: int,
            distinct: bool,
            data: Any,
            it: Iterator[Statement]
    ) -> Iterator[Statement]:
        return self.mapping.filter_post_hook(
            self, filter, limit, distinct, data, it)

    def _make_filter_query(
            self,
            filter: Filter
    ) -> SPARQL_Builder:
        subject, property, value, snak_mask = filter._unpack_legacy()
        q = self.mapping.Builder()
        with q.where():
            subject_prefix: IRI | None = None
            if subject is not None:
                if isinstance(subject, Entity):
                    q.matched_subject = self.mapping.encode_entity(subject)
                elif isinstance(subject, SnakSet):
                    status, subject_prefix = self._try_push_snak_set(
                        q, q.matched_subject, subject)
                    if not status:
                        return q  # empty query
                    assert subject_prefix is not None
                else:
                    raise self._should_not_get_here()
            value_prefix: IRI | None = None
            if value is not None:
                if isinstance(value, Value):
                    q.matched_value = self.mapping.encode_value(value)
                elif isinstance(value, SnakSet):
                    status, value_prefix = self._try_push_snak_set(
                        q, q.matched_value, value)
                    if not status:
                        return q  # empty query
                    assert value_prefix is not None
                else:
                    raise self._should_not_get_here()
            with q.union() as cup:
                for _, specs in self.mapping.specs.items():
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
                                if not isinstance(value, Entity):
                                    continue  # value mismatch
                                assert isinstance(value, Entity)
                                if not value.iri.content.startswith(
                                        value_prefix.content):
                                    continue  # mismatch value
                        if not spec._match(
                                subject, property, value, snak_mask):
                            continue  # spec does not match filter
                        cup.branch()
                        spec._define(q, with_binds=True)
        return q

    def _parse_filter_results(
            self,
            results: SPARQL_Results,
            filter: Filter
    ) -> Iterator[Statement | None]:
        _, property, *_ = filter._unpack_legacy()
        for entry in results.bindings:
            stmt = entry.check_statement(
                'subject', 'property', 'value',
                'qt_amount', 'qt_unit', 'qt_lower', 'qt_upper',
                'tm_value', 'tm_precision', 'tm_timezone', 'tm_calendar')
            if (isinstance(property, Property)
                and isinstance(stmt.snak, ValueSnak)
                    and isinstance(property.range, ExternalIdDatatype)):
                stmt = stmt.replace(stmt.KEEP, property(stmt.snak.value))
            if self.has_flags(self.LATE_FILTER) and not filter.match(stmt):
                yield None
                continue
            wds = self._parse_filter_results_check_wds(entry, stmt)
            self._cache_add_wds(stmt, wds)
            yield stmt

    def _parse_filter_results_check_wds(
            self,
            entry: SPARQL_Results.Bindings,
            stmt: Statement
    ) -> BNode | URIRef:
        return NS.WDS[stmt.digest]

    def _try_push_snak_set(
            self,
            q: SPARQL_Builder,
            target: SPARQL_Builder.TTrm,
            snaks: SnakSet
    ) -> tuple[bool, IRI | None]:
        subject_prefixes = set()
        for snak in snaks:
            if not isinstance(snak, ValueSnak):
                return False, None  # no such snak
            vsnak = cast(ValueSnak, snak)
            if vsnak.property not in self.mapping.specs:
                return False, None  # no such property
            for spec in self.mapping.specs[vsnak.property]:
                t = Filter.from_snak(None, vsnak)._unpack_legacy()
                if not spec._match(*t):
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

    @override
    def _get_annotations_pre_hook(
            self,
            stmts: Iterable[Statement]
    ) -> tuple[Iterable[Statement], Any]:
        return self.mapping.get_annotations_pre_hook(self, stmts)

    @override
    def _get_annotations_post_hook(
            self,
            stmts: Iterable[Statement],
            data: Any,
            it: Iterator[tuple[Statement, AnnotationRecordSet | None]]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        return self.mapping.get_annotations_post_hook(self, stmts, data, it)

    @override
    def _get_annotations(
            self,
            stmts: Iterable[Statement],
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        for stmt in stmts:
            if self._cache_get_wdss(stmt) or stmt in self:
                assert self._cache_get_wdss(stmt)

                def it(property: Property) -> Iterable[AnnotationRecord]:
                    for spec in self.mapping.specs.get(property, ()):
                        yield from spec.kwargs.get('annotations', ())
                annots = AnnotationRecordSet(*it(stmt.snak.property))
                if not annots:
                    annots = AnnotationRecordSet(AnnotationRecord())
                yield stmt, annots
            else:
                yield stmt, None

# -- Descriptors -----------------------------------------------------------

    def _make_item_or_property_descriptor_query(
            self,
            entities: Collection[Item | Property],
            cls: type[Entity],
            lang: str,
            mask: Descriptor.AttributeMask
    ) -> SPARQL_Builder:
        q = cast(SPARQL_Mapping.Builder, self.mapping.Builder())
        if self.has_flags(self.EARLY_FILTER):
            get_label = bool(mask & Descriptor.LABEL)
            get_aliases = bool(mask & Descriptor.ALIASES)
            get_description = bool(mask & Descriptor.DESCRIPTION)
        else:
            get_label = True
            get_aliases = True
            get_description = True
        instance_of_specs = self.mapping.specs.get(
            Property(WD['P31'], Item), [])
        label_specs = self.mapping.descriptor_specs.get(
            Property('label'), [])
        alias_specs = self.mapping.descriptor_specs.get(
            Property('alias'), [])
        description_specs = self.mapping.descriptor_specs.get(
            Property('description'), [])
        with q.where():
            with q.union() as cup:
                for instance_of_spec in instance_of_specs:
                    matched_entities = [
                        e for e in entities
                        if instance_of_spec._match(
                            *Filter(e)._unpack_legacy())]
                    if not matched_entities:
                        continue  # nothing to do

                    def push_values(spec):
                        with q.values(q.matched_subject) as values:
                            for entity in matched_entities:
                                values.push(self.mapping.encode_entity(
                                    entity))
                        q.bind_uri(
                            q.matched_subject, q.subject,
                            spec.kwargs.get('subject_prefix_replacement'))
                    cup.branch()
                    filter = Filter(matched_entities[0])
                    matched_specs = {}
                    if get_label:
                        matched_specs['label'] = [
                            s for s in label_specs if s._match(
                                *filter._unpack_legacy())]
                    if get_aliases:
                        matched_specs['alias'] = [
                            s for s in alias_specs if s._match(
                                *filter._unpack_legacy())]
                    if get_description:
                        matched_specs['description'] = [
                            s for s in description_specs if s._match(
                                *filter._unpack_legacy())]
                    if not any(map(bool, matched_specs.values())):
                        instance_of_spec._define(q)
                        push_values(instance_of_spec)
                        continue  # test presence, nothing else to do
                    with q.union() as cup2:
                        for attr, specs in matched_specs.items():
                            for spec in specs:
                                cup2.branch()
                                instance_of_spec._define(q)
                                with q.optional():
                                    spec._define(q)
                                    ###
                                    # FIXME: This crashes Virtuoso!
                                    ###
                                    # value_language = spec.kwargs.get(
                                    #     'value_language')
                                    # if value_language is not None:
                                    #     q.bind(q.strlang(
                                    #         q.matched_value,
                                    #         String(value_language)),
                                    # else:
                                    #     q.bind(q.matched_value, q.var(attr))
                                    ###
                                    q.bind(q.matched_value, q.var(attr))
                                push_values(spec)
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
