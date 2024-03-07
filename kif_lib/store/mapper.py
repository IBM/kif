# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import logging

from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    Entity,
    FilterPattern,
    IRI,
    SnakSet,
    Statement,
    Value,
    ValueSnak,
)
from ..typing import Any, cast, Iterable, Iterator, Optional, override, Union
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
            iri: Union[IRI, str],
            mapping: SPARQL_Mapping,
            **kwargs: Any
    ):
        assert store_name == self.store_name
        super().__init__(store_name, iri, **kwargs)
        self._mapping = mapping

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
            if pat.subject is not None:
                if pat.subject.entity is not None:
                    q.matched_subject = self.mapping.normalize_entity(
                        pat.subject.entity)
                elif pat.subject.snak_set is not None:
                    if not self._try_push_snak_set(
                            q, q.matched_subject, pat.subject.snak_set):
                        return q  # impossible condition
                else:
                    raise self._should_not_get_here()
            value: Optional[Value] = None
            if pat.value is not None:
                if pat.value.value is not None:
                    value = pat.value.value
                    if pat.property is None:
                        q.matched_value = self.mapping.normalize_value(value)
                    else:
                        q.matched_value = self.mapping.normalize_value(
                            value, pat.property.property)
                elif pat.value.snak_set is not None:
                    if not self._try_push_snak_set(
                            q, q.matched_value, pat.value.snak_set):
                        return q  # impossible condition
                else:
                    raise self._should_not_get_here()
            with q.union() as cup:
                for property, spec in self.mapping.specs.items():
                    if pat.property is not None:
                        if pat.property.property != property:
                            continue
                    value_class = spec.datatype.to_value_class()
                    if pat.value is not None and pat.value.snak_set:
                        if not issubclass(value_class, Entity):
                            continue
                    if value is not None:
                        if not value_class.test(value):
                            continue
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
    ) -> bool:
        for snak in snaks:
            if not snak.is_value_snak():
                return False
            vsnak = cast(ValueSnak, snak)
            if vsnak.property not in self.mapping.specs:
                return False
            self.mapping.specs[vsnak.property]._define(
                cast(SPARQL_Mapping.Builder, q), target, None,
                self.mapping.normalize_value(vsnak.value, vsnak.property))
        return True

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
