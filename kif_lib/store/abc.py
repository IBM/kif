# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import sys
from collections.abc import Iterable, Set
from enum import auto, Flag
from itertools import chain
from typing import Any, cast, Iterator, NoReturn, Optional, TypeVar, Union

import more_itertools
from rdflib.graph import Graph
from rdflib.namespace import NamespaceManager

from .. import namespace as NS
from ..cache import Cache
from ..error import Error, MustBeImplementedInSubclass
from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    Descriptor,
    Entity,
    EntityFingerprint,
    FilterPattern,
    Fingerprint,
    IRI,
    KIF_Object,
    PropertyFingerprint,
    ReferenceRecordSet,
    Snak,
    SnakMask,
    Statement,
    T_IRI,
    TCallable,
    TEntityFingerprint,
    Text,
    TFingerprint,
    TPropertyFingerprint,
    TReferenceRecordSet,
    TSnakMask,
)

T = TypeVar('T')
T_NS = NS.T_NS


class StoreError(Error):
    """Base class for store errors."""


class StoreFlags(Flag):
    """Store configuration flags."""

    #: Whether to enable cache.
    CACHE = auto()

    #: Whether to fetch only best ranked statements.
    BEST_RANK = auto()

    #: Whether to fetch ValueSnak's.
    VALUE_SNAK = auto()

    #: Whether to fetch SomeValueSnak's.
    SOME_VALUE_SNAK = auto()

    #: Whether to fetch NoValueSnak's.
    NO_VALUE_SNAK = auto()

    #: Whether to do early filtering.
    EARLY_FILTER = auto()

    #: Whether to do late filtering.
    LATE_FILTER = auto()

    #: Alias for "default flags".
    DEFAULT = (CACHE
               | BEST_RANK
               | VALUE_SNAK
               | SOME_VALUE_SNAK
               | NO_VALUE_SNAK
               | EARLY_FILTER
               | LATE_FILTER)

    #: Alias for "all flags".
    ALL = (CACHE
           | BEST_RANK
           | VALUE_SNAK
           | SOME_VALUE_SNAK
           | NO_VALUE_SNAK
           | EARLY_FILTER
           | LATE_FILTER)


class Store(Set):
    """Store factory.

    Parameters:
       store_type: Type of concrete store to instantiate.
       args: Arguments to concrete store.
       flags: Configuration flags.
       namespaces: Namespaces.
       page_size: Maximum size of result pages.
       timeout: Timeout in seconds.
       kwargs: Keyword arguments to concrete store.
    """

    registry: dict[str, type['Store']] = dict()
    store_type: str
    store_description: str

    @classmethod
    def _register(cls, store: type['Store'], type: str, description: str):
        store.store_type = type
        store.store_description = description
        cls.registry[store.store_type] = store

    @classmethod
    def __init_subclass__(cls, type: str, description: str):
        Store._register(cls, type, description)

    @classmethod
    def _error(cls, msg: str) -> StoreError:
        return StoreError(msg)

    # @classmethod
    # def _generate_serial_number(cls) -> str:
    #     from uuid import uuid4
    #     return uuid4().hex

    def __new__(cls, store_type: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            store_type, store_type in cls.registry,
            f"no such store type '{store_type}'",
            Store, 'store_type', 1, ValueError)
        return super(Store, cls).__new__(cls.registry[store_type])

    __slots__ = (
        '_cache',
        '_extra_references',
        '_flags',
        '_nsm',
        '_page_size',
        '_timeout',
    )

    _cache: Cache
    _extra_references: Optional[ReferenceRecordSet]
    _flags: StoreFlags
    _nsm: NamespaceManager
    _page_size: Optional[int]
    _timeout: Optional[int]

    def __init__(
            self,
            *args: Any,
            extra_references: Optional[TReferenceRecordSet] = None,
            flags: Optional[StoreFlags] = None,
            namespaces: Optional[dict[str, T_IRI]] = None,
            page_size: Optional[int] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ):
        self._init_flags(flags)
        self._cache = Cache(self.has_flags(StoreFlags.CACHE))
        self._init_nsm(namespaces or dict())
        self.set_extra_references(extra_references)
        self.set_page_size(page_size)
        self.set_timeout(timeout)

    def _init_flags(self, flags: Optional[StoreFlags] = None):
        if flags is None:
            self._flags = StoreFlags.DEFAULT
        else:
            self._flags = StoreFlags(flags)

    def _init_nsm(self, namespaces: dict[str, T_IRI]):
        self._nsm = NamespaceManager(Graph())
        ns_dict = dict()
        for k, v in chain(NS._DEFAULT_NSM.namespaces(), namespaces.items()):
            self._nsm.bind(k, v)
            ns_dict[k] = v

    # -- Extra references --------------------------------------------------

    @property
    def extra_references(self) -> ReferenceRecordSet:
        """Extra references."""
        return self.get_extra_references()

    @extra_references.setter
    def extra_references(
            self,
            references: Optional[TReferenceRecordSet] = None
    ):
        self.set_extra_references(references)

    def get_extra_references(
            self,
            default=ReferenceRecordSet()
    ) -> ReferenceRecordSet:
        """Gets extra references.

        If no extra references are set, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Extra references.
        """
        return self._extra_references or default

    def set_extra_references(
            self,
            references: Optional[TReferenceRecordSet] = None
    ):
        """Sets extra references.

        Parameters:
           references: References.
        """
        self._extra_references =\
            ReferenceRecordSet._check_optional_arg_reference_record_set(
                references, None, self.set_extra_references, 'references', 1)

    # -- Page size ---------------------------------------------------------

    @property
    def page_size(self) -> int:
        """Response page size."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: Optional[int] = None):
        self.set_page_size(page_size)

    def get_page_size(
            self,
            default: int = 100
    ) -> int:
        """Gets response page size.

        If no page size is set, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Response page size.
        """
        return self._page_size or default

    def set_page_size(
            self,
            page_size: Optional[int] = None
    ):
        """Sets response page size.

        Parameters:
           page_size: Page size.
        """
        self._page_size = KIF_Object._check_optional_arg_int(
            page_size, None, self.set_page_size, 'page_size', 1)

    def _batched(self, it: Iterable[T]) -> Iterable[tuple[T, ...]]:
        return more_itertools.batched(it, self.page_size)

    # -- Timeout -----------------------------------------------------------

    @property
    def timeout(self) -> Optional[int]:
        """Timeout in seconds."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: Optional[int] = None):
        self.set_timeout(timeout)

    def get_timeout(
            self,
            default: Optional[int] = None
    ) -> Optional[int]:
        """Gets timeout in seconds.

        If no timeout is set, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Timeout in seconds or ``None`` (no timeout).
        """
        return self._timeout or default

    def set_timeout(
            self,
            timeout: Optional[int] = None
    ):
        """Sets timeout in seconds.

        Parameters:
           timeout: Timeout in seconds.
        """
        self._timeout = KIF_Object._check_optional_arg_int(
            timeout, None, self.set_timeout, 'timeout', 1)

    # -- Set interface -----------------------------------------------------

    def __contains__(self, v):
        return self.contains(v) if Statement.test(v) else False

    def __iter__(self):
        return self.filter()

    def __len__(self):
        return self.count()

    # -- Flags -------------------------------------------------------------

    #: Alias for :attr:`StoreFlags.CACHE`.
    CACHE = StoreFlags.CACHE

    #: Alias for :attr:`StoreFlags.BEST_RANK`.
    BEST_RANK = StoreFlags.BEST_RANK

    #: Alias for :attr:`StoreFlags.VALUE_SNAK`.
    VALUE_SNAK = StoreFlags.VALUE_SNAK

    #: Alias for :attr:`StoreFlags.SOME_VALUE_SNAK`.
    SOME_VALUE_SNAK = StoreFlags.SOME_VALUE_SNAK

    #: Alias for :attr:`StoreFlags.NO_VALUE_SNAK`.
    NO_VALUE_SNAK = StoreFlags.NO_VALUE_SNAK

    #: Alias for :attr:`StoreFlags.EARLY_FILTER`.
    EARLY_FILTER = StoreFlags.EARLY_FILTER

    #: Alias for :attr:`StoreFlags.LATE_FILTER`.
    LATE_FILTER = StoreFlags.LATE_FILTER

    #: Alias for :attr:`StoreFlags.DEFAULT`.
    DEFAULT = StoreFlags.DEFAULT

    #: Alias for :attr:`StoreFlags.ALL`.
    ALL = StoreFlags.ALL

    @property
    def flags(self) -> StoreFlags:
        """Store flags."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: StoreFlags):
        if flags != self._flags and self._do_set_flags(self._flags, flags):
            self._flags = StoreFlags(flags)

    def _do_set_flags(self, old: StoreFlags, new: StoreFlags) -> bool:
        self._cache.clear()
        return True

    def get_flags(self) -> StoreFlags:
        """Gets store flags.

        Returns:
           Store flags.
        """
        return self._flags

    def has_flags(self, flags: StoreFlags) -> bool:
        """Tests whether store flags are set.

        Parameters:
           flags: Flags to test.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return bool(self.flags & flags)

    def set_flags(self, flags: StoreFlags):
        """Set store flags.

        Parameters:
           flags: Flags to set.
        """
        self.flags |= flags

    def unset_flags(self, flags: StoreFlags):
        """Unset store flags.

        Parameters:
           flags: Flags to unset.
        """
        self.flags &= ~flags

    # -- Caching -----------------------------------------------------------

    def _cache_get_occurrence(
            self,
            obj: Union[Entity, Statement]
    ) -> Optional[bool]:
        return self._cache.get(obj, 'occurrence')

    def _cache_set_occurrence(
            self,
            obj: Union[Entity, Statement],
            status: bool
    ) -> bool:
        return self._cache.set(obj, 'occurrence', status)

    # -- Namespaces --------------------------------------------------------

    @property
    def namespaces(self) -> dict[str, IRI]:
        """The namespace dictionary of store."""
        return self.get_namespaces()

    def get_namespaces(self) -> dict[str, IRI]:
        """Gets the namespace dictionary of store.

        Returns:
           The namespace dictionary of store.
        """
        return dict(map(
            lambda t: (t[0], IRI(t[1])), self._nsm.namespaces()))

    @property
    def owl(self) -> T_NS:
        return NS.OWL

    @property
    def p(self) -> T_NS:
        return NS.P

    @property
    def pq(self) -> T_NS:
        return NS.PQ

    @property
    def pqn(self) -> T_NS:
        return NS.PQN

    @property
    def pqv(self) -> T_NS:
        return NS.PQV

    @property
    def pr(self) -> T_NS:
        return NS.PR

    @property
    def prn(self) -> T_NS:
        return NS.PRN

    @property
    def prov(self) -> T_NS:
        return NS.PROV

    @property
    def prv(self) -> T_NS:
        return NS.PRV

    @property
    def ps(self) -> T_NS:
        return NS.PS

    @property
    def psn(self) -> T_NS:
        return NS.PSN

    @property
    def psv(self) -> T_NS:
        return NS.PSV

    @property
    def rdf(self) -> T_NS:
        return NS.RDF

    @property
    def rdfs(self) -> T_NS:
        return NS.RDFS

    @property
    def schema(self) -> T_NS:
        return NS.SCHEMA

    @property
    def skos(self) -> T_NS:
        return NS.SKOS

    @property
    def wd(self) -> T_NS:
        return NS.WD

    @property
    def wdata(self) -> T_NS:
        return NS.WDATA

    @property
    def wdgenid(self) -> T_NS:
        return NS.WDGENID

    @property
    def wdno(self) -> T_NS:
        return NS.WDNO

    @property
    def wdref(self) -> T_NS:
        return NS.WDREF

    @property
    def wds(self) -> T_NS:
        return NS.WDS

    @property
    def wdt(self) -> T_NS:
        return NS.WDT

    @property
    def wdv(self) -> T_NS:
        return NS.WDV

    @property
    def wikibase(self) -> T_NS:
        return NS.WIKIBASE

    @property
    def xsd(self) -> T_NS:
        return NS.XSD

    # -- Queries -----------------------------------------------------------

    def contains(self, stmt: Statement) -> bool:
        """Tests whether statement is in store.

        Parameters:
           stmt: Statement.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        Statement.check(stmt, self.contains, 'stmt', 1)
        status = self._cache_get_occurrence(stmt)
        if status is None:
            pat = self._normalize_filter_pattern(
                FilterPattern.from_statement(stmt))
            status = self._contains_tail(pat)
            status = self._cache_set_occurrence(stmt, status)
        return status

    def _contains_tail(self, pattern: FilterPattern) -> bool:
        if pattern.is_nonempty():
            return self._contains(pattern)
        else:
            return False

    def _contains(self, pattern: FilterPattern) -> bool:
        raise MustBeImplementedInSubclass

    def count(
            self,
            subject: Optional[TEntityFingerprint] = None,
            property: Optional[TPropertyFingerprint] = None,
            value: Optional[TFingerprint] = None,
            snak_mask: Optional[TSnakMask] = None,
            pattern: Optional[FilterPattern] = None
    ) -> int:
        """Counts statements matching pattern.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           pattern: Filter pattern.

        Returns:
           The number of statements matching pattern.
        """
        return self._count_tail(self._check_filter_pattern(
            subject, property, value, snak_mask, pattern, self.count))

    def count_snak(
            self,
            subject: Optional[TEntityFingerprint] = None,
            snak: Optional[Snak] = None
    ) -> int:
        """Counts statements matching pattern.

        Parameters:
           subject: Entity.
           snak: Snak.

        Returns:
           The number of statements matching pattern.
        """
        return self._count_tail(self._check_filter_snak_pattern(
            subject, snak, self.count_snak))

    def _count_tail(self, pattern: FilterPattern) -> int:
        if pattern.is_nonempty():
            return self._count(pattern)
        else:
            return 0

    def _count(self, pattern: FilterPattern) -> int:
        raise MustBeImplementedInSubclass

    def _check_filter_pattern(
            self,
            subject: Optional[TEntityFingerprint] = None,
            property: Optional[TPropertyFingerprint] = None,
            value: Optional[TFingerprint] = None,
            snak_mask: Optional[TSnakMask] = None,
            pattern: Optional[FilterPattern] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[FilterPattern, NoReturn]:
        subj = EntityFingerprint._check_optional_arg_entity_fingerprint(
            subject, None, function, 'subject', 1)
        prop = PropertyFingerprint._check_optional_arg_property_fingerprint(
            property, None, function, 'property', 2)
        val = Fingerprint._check_optional_arg_fingerprint(
            value, None, function, 'value', 3)
        mask = Snak._check_optional_arg_snak_mask(
            snak_mask, SnakMask.ALL, function, 'snak_mask', 4)
        pat = FilterPattern(subj, prop, val, mask)
        if pattern is not None:
            pat = FilterPattern._combine(
                pat, cast(FilterPattern, FilterPattern.check(
                    pattern, function, 'pattern', 5)))
        return self._normalize_filter_pattern(pat)

    def _check_filter_snak_pattern(
            self,
            subject: Optional[TEntityFingerprint] = None,
            snak: Optional[Snak] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[FilterPattern, NoReturn]:
        return self._normalize_filter_pattern(FilterPattern.from_snak(
            EntityFingerprint._check_optional_arg_entity_fingerprint(
                subject, None, function, 'subject', 1),
            cast(Optional[Snak], Snak.check_optional(
                snak, None, function, 'snak', 2))))

    def _normalize_filter_pattern(
            self,
            pat: FilterPattern
    ) -> FilterPattern:
        store_snak_mask = SnakMask(0)
        if self.has_flags(StoreFlags.VALUE_SNAK):
            store_snak_mask |= SnakMask.VALUE_SNAK
        if self.has_flags(StoreFlags.SOME_VALUE_SNAK):
            store_snak_mask |= SnakMask.SOME_VALUE_SNAK
        if self.has_flags(StoreFlags.NO_VALUE_SNAK):
            store_snak_mask |= SnakMask.NO_VALUE_SNAK
        return cast(FilterPattern, pat.replace(
            None, None, None, pat.snak_mask & store_snak_mask))

    def _check_filter_limit(self, limit: Optional[int]) -> int:
        if limit is None:
            return sys.maxsize
        else:
            return max(limit, 0)

    def filter(
            self,
            subject: Optional[TEntityFingerprint] = None,
            property: Optional[TPropertyFingerprint] = None,
            value: Optional[TFingerprint] = None,
            snak_mask: Optional[TSnakMask] = None,
            pattern: Optional[FilterPattern] = None,
            limit: Optional[int] = None
    ) -> Iterator[Statement]:
        """Filters statements matching pattern.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           pattern: Filter pattern.
           limit: Maximum number of statements to return.

        Returns:
           An iterator of statements matching pattern.
        """
        pat = self._check_filter_pattern(
            subject, property, value, snak_mask, pattern, self.filter)
        KIF_Object._check_optional_arg_int(
            limit, None, self.filter, 'limit', 6)
        return self._filter_tail(pat, limit)

    def filter_snak(
            self,
            subject: Optional[TEntityFingerprint] = None,
            snak: Optional[Snak] = None,
            limit: Optional[int] = None
    ) -> Iterator[Statement]:
        """Filters statements matching pattern.

        Parameters:
           subject: Entity.
           snak: Snak.
           limit: Maximum number of statements to return.

        Returns:
           An iterator of statements matching pattern.
        """
        pat = self._check_filter_snak_pattern(
            subject, snak, self.filter_snak)
        KIF_Object._check_optional_arg_int(
            limit, None, self.filter_snak, 'limit', 3)
        return self._filter_tail(pat, limit)

    def _filter_tail(
            self,
            pattern: FilterPattern,
            limit: Optional[int]
    ) -> Iterator[Statement]:
        limit = self._check_filter_limit(limit)
        if limit > 0 and pattern.is_nonempty():
            return self._filter(pattern, limit=limit)
        else:
            return iter([])

    def _filter(
            self,
            pattern: FilterPattern,
            limit: int
    ) -> Iterator[Statement]:
        raise MustBeImplementedInSubclass

    # -- Annotations -------------------------------------------------------

    def filter_annotated(
            self,
            subject: Optional[TEntityFingerprint] = None,
            property: Optional[TPropertyFingerprint] = None,
            value: Optional[TFingerprint] = None,
            snak_mask: Optional[TSnakMask] = None,
            pattern: Optional[FilterPattern] = None,
            limit: Optional[int] = None
    ) -> Iterator[tuple[Statement, AnnotationRecordSet]]:
        """:meth:`Store.filter` with annotations.

        Same as :meth:`Store.filter` followed by
        :meth:`Store.get_annotations`.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           pattern: Filter pattern.
           limit: Maximum number of statements to return.

        Returns:
           An iterator of pairs (statement, annotation record set)
           where statement matches pattern.
        """
        return self._filter_annotated_tail(self.filter(
            subject, property, value, snak_mask, pattern, limit))

    def _filter_annotated_tail(
            self,
            it: Iterator[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet]]:
        for stmt, annots in self.get_annotations(it):
            assert annots is not None
            yield stmt, annots

    def filter_snak_annotated(
            self,
            subject: Optional[TEntityFingerprint] = None,
            snak: Optional[Snak] = None,
            limit: Optional[int] = None
    ) -> Iterator[tuple[Statement, AnnotationRecordSet]]:
        """:meth:`Store.filter_snak` with annotations.

        Same as :meth:`Store.filter_snak` followed by
        :meth:`Store.get_annotations`.

        Parameters:
           subject: Entity.
           snak: Snak.
           limit: Maximum number of statements to return.

        Returns:
           An iterator of pairs (statement, annotation record set)
           where statement matches pattern.
        """
        return self._filter_annotated_tail(self.filter_snak(
            subject, snak, limit))

    def get_annotations(
            self,
            stmts: Union[Statement, Iterable[Statement]]
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        """Gets statements' annotations.

        Parameters:
           stmts: Statements.

        Returns:
           An iterator of pairs (statement, annotation record set).
        """
        KIF_Object._check_arg_isinstance(
            stmts, (Statement, Iterable), self.get_annotations, 'stmts', 1)
        return self._get_annotations_tail(stmts)

    def _get_annotations_tail(
            self,
            stmts: Union[Statement, Iterable[Statement]]
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        if Statement.test(stmts):
            it = self._get_annotations([cast(Statement, stmts)])
        else:
            it = self._get_annotations(map(
                lambda s: cast(Statement, Statement.check(
                    s, self.get_annotations)), stmts))
        if self.extra_references:
            return self._get_annotations_with_default_references(it)
        else:
            return it

    def _get_annotations_with_default_references(
            self,
            it: Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        for stmt, annots in it:
            if annots is None:
                yield stmt, annots
            else:
                def patch(a: AnnotationRecord):
                    return AnnotationRecord(
                        a.qualifiers,
                        a.references.union(self.extra_references),
                        a.rank)
                yield stmt, AnnotationRecordSet(*map(patch, annots))

    def _get_annotations(
            self,
            stmts: Iterable[Statement],
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        raise MustBeImplementedInSubclass

    # -- Descriptors -------------------------------------------------------

    def get_descriptor(
            self,
            entities: Union[Entity, Iterable[Entity]],
            language: str = Text.default_language
    ) -> Iterator[tuple[Entity, Optional[Descriptor]]]:
        """Gets entities' descriptor.

        Parameters:
           entities: Entities.

        Returns:
           An iterator of pairs (entity, descriptor).
        """
        KIF_Object._check_arg_isinstance(
            entities, (Entity, Iterable),
            self.get_descriptor, 'entities', 1)
        KIF_Object._check_arg_str(
            language, self.get_descriptor, 'language', 2)
        if Entity.test(entities):
            return self._get_descriptor([cast(Entity, entities)], language)
        else:
            return self._get_descriptor(map(
                lambda e: cast(Entity, Entity.check(
                    e, self.get_descriptor)), entities), language)

    def _get_descriptor(
            self,
            entities: Iterable[Entity],
            language: str
    ) -> Iterator[tuple[Entity, Optional[Descriptor]]]:
        raise MustBeImplementedInSubclass
