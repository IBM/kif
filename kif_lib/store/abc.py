# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import sys
from collections.abc import Iterable, Set
from enum import auto, Flag

from rdflib.graph import Graph
from rdflib.namespace import NamespaceManager

from .. import namespace as NS
from ..cache import Cache
from ..error import Error, MustBeImplementedInSubclass
from ..itertools import batched, chain
from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    Entity,
    EntityFingerprint,
    FilterPattern,
    Fingerprint,
    IRI,
    Item,
    ItemDescriptor,
    KIF_Object,
    Lexeme,
    LexemeDescriptor,
    Property,
    PropertyDescriptor,
    PropertyFingerprint,
    ReferenceRecordSet,
    Snak,
    Statement,
    T_IRI,
    TCallable,
    TEntityFingerprint,
    Text,
    TFingerprint,
    TPropertyFingerprint,
    TReferenceRecordSet,
)
from ..typing import Any, cast, Iterator, NoReturn, Optional, TypeVar, Union

T = TypeVar('T')
T_NS = NS.T_NS


class StoreError(Error):
    """Base class for store errors."""


class Store(Set):
    """Store factory.

    Parameters:
       store_name: Store plugin to instantiate.
       args: Arguments to concrete store.
       flags: Configuration flags.
       namespaces: Namespaces.
       page_size: Maximum size of result pages.
       timeout: Timeout in seconds.
       kwargs: Keyword arguments to concrete store.
    """

    #: Store plugin registry.
    registry: dict[str, type['Store']] = dict()

    #: The name of store plugin.
    store_name: str

    #: The description of store plugin.
    store_description: str

    @classmethod
    def _register(cls, store: type['Store'], name: str, description: str):
        store.store_name = name
        store.store_description = description
        cls.registry[store.store_name] = store

    @classmethod
    def __init_subclass__(cls, name: str, description: str):
        Store._register(cls, name, description)

    @classmethod
    def _error(cls, msg: str) -> StoreError:
        return StoreError(msg)

    def __new__(cls, store_name: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            store_name, store_name in cls.registry,
            f"no such store plugin '{store_name}'",
            Store, 'store_name', 1, ValueError)
        return super(Store, cls).__new__(cls.registry[store_name])

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
    _flags: 'Flags'
    _nsm: NamespaceManager
    _page_size: Optional[int]
    _timeout: Optional[int]

    def __init__(
            self,
            *args: Any,
            extra_references: Optional[TReferenceRecordSet] = None,
            flags: Optional['Flags'] = None,
            namespaces: Optional[dict[str, T_IRI]] = None,
            page_size: Optional[int] = None,
            timeout: Optional[int] = None,
            **kwargs: Any
    ):
        self._init_flags(flags)
        self._cache = Cache(self.has_flags(self.CACHE))
        self._init_nsm(namespaces or dict())
        self.set_extra_references(extra_references)
        self.set_page_size(page_size)
        self.set_timeout(timeout)

    def _init_flags(self, flags: Optional['Flags'] = None):
        if flags is None:
            self._flags = self.DEFAULT
        else:
            self._flags = self.Flags(flags)

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
        return batched(it, self.page_size)

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

    class Flags(Flag):
        """Store flags."""

        #: Whether to enable cache.
        CACHE = auto()

        #: Whether to fetch only the best ranked statements.
        BEST_RANK = auto()

        #: Whether to fetch value snaks.
        VALUE_SNAK = auto()

        #: Whether to fetch some-value snaks.
        SOME_VALUE_SNAK = auto()

        #: Whether to fetch no-value snaks.
        NO_VALUE_SNAK = auto()

        #: Whether to enable early filtering.
        EARLY_FILTER = auto()

        #: Whether to enable late filtering.
        LATE_FILTER = auto()

        #: Default flags.
        DEFAULT = (
            CACHE
            | BEST_RANK
            | VALUE_SNAK
            | SOME_VALUE_SNAK
            | NO_VALUE_SNAK
            | EARLY_FILTER
            | LATE_FILTER)

        #: All flags.
        ALL = (
            CACHE
            | BEST_RANK
            | VALUE_SNAK
            | SOME_VALUE_SNAK
            | NO_VALUE_SNAK
            | EARLY_FILTER
            | LATE_FILTER)

    #: Whether to enable cache.
    CACHE = Flags.CACHE

    #: Whether to fetch only the best ranked statements.
    BEST_RANK = Flags.BEST_RANK

    #: Whether to fetch value snaks.
    VALUE_SNAK = Flags.VALUE_SNAK

    #: Whether to fetch some-value snaks.
    SOME_VALUE_SNAK = Flags.SOME_VALUE_SNAK

    #: Whether to fetch no-value snaks.
    NO_VALUE_SNAK = Flags.NO_VALUE_SNAK

    #: Whether to enable early filtering.
    EARLY_FILTER = Flags.EARLY_FILTER

    #: Whether to enable late filtering.
    LATE_FILTER = Flags.LATE_FILTER

    #: Default flags.
    DEFAULT = Flags.DEFAULT

    #: All flags.
    ALL = Flags.ALL

    @property
    def flags(self) -> Flags:
        """The flags set in store."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: Flags):
        if flags != self._flags and self._do_set_flags(self._flags, flags):
            self._flags = self.Flags(flags)

    def _do_set_flags(self, old: Flags, new: Flags) -> bool:
        self._cache.clear()
        return True

    def get_flags(self) -> Flags:
        """Gets the flags set in store.

        Returns:
           Store flags.
        """
        return self._flags

    def has_flags(self, flags: Flags) -> bool:
        """Tests whether `flags` are set in store.

        Parameters:
           flags: Store flags.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return bool(self.flags & flags)

    def set_flags(self, flags: Flags):
        """Sets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        self.flags |= flags

    def unset_flags(self, flags: Flags):
        """Unset `flags` in store.

        Parameters:
           flags: Store flags.
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
    def dct(self) -> T_NS:
        return NS.DCT

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
            snak_mask: Optional[Snak.TMask] = None,
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
            snak_mask: Optional[Snak.TMask] = None,
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
            snak_mask, Snak.ALL, function, 'snak_mask', 4)
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
        store_snak_mask = Snak.Mask(0)
        if self.has_flags(self.VALUE_SNAK):
            store_snak_mask |= Snak.VALUE_SNAK
        if self.has_flags(self.SOME_VALUE_SNAK):
            store_snak_mask |= Snak.SOME_VALUE_SNAK
        if self.has_flags(self.NO_VALUE_SNAK):
            store_snak_mask |= Snak.NO_VALUE_SNAK
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
            snak_mask: Optional[Snak.TMask] = None,
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
            snak_mask: Optional[Snak.TMask] = None,
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
           An iterator of pairs: statement, annotation record set.
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
           An iterator of pairs: statement, annotation record set.
        """
        return self._filter_annotated_tail(self.filter_snak(
            subject, snak, limit))

    def get_annotations(
            self,
            stmts: Union[Statement, Iterable[Statement]]
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        """Gets annotation records of statements.

        Parameters:
           stmts: Statements.

        Returns:
           An iterator of pairs: statement, annotation record set.
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

    def get_item_descriptor(
            self,
            items: Union[Item, Iterable[Item]],
            language: str = Text.default_language,
            descriptor_mask: Optional[ItemDescriptor.TAttributeMask] = None
    ) -> Iterable[tuple[Item, Optional[ItemDescriptor]]]:
        """Gets descriptor of items.

        Parameters:
           items: Items.
           language: Language tag.
           descriptor_mask: Descriptor mask.

        Returns:
           An iterator of pairs: item, descriptor.
        """
        KIF_Object._check_arg_isinstance(
            items, (Item, Iterable),
            self.get_item_descriptor, 'items', 1)
        KIF_Object._check_arg_str(
            language, self.get_item_descriptor, 'language', 2)
        mask =\
            ItemDescriptor.\
            _check_optional_arg_plain_descriptor_attribute_mask(
                descriptor_mask, ItemDescriptor.ALL,
                self.get_item_descriptor, 'mask', 3)
        assert mask is not None
        if Item.test(items):
            return self._get_item_descriptor(
                [cast(Item, items)], language, mask)
        else:
            return self._get_item_descriptor(map(
                lambda e: cast(Item, Item.check(
                    e, self.get_item_descriptor)), items), language, mask)

    def _get_item_descriptor(
            self,
            items: Iterable[Item],
            lang: str,
            mask: ItemDescriptor.AttributeMask
    ) -> Iterator[tuple[Item, Optional[ItemDescriptor]]]:
        raise MustBeImplementedInSubclass

    def get_property_descriptor(
            self,
            properties: Union[Property, Iterable[Property]],
            language: str = Text.default_language,
            descriptor_mask: Optional[PropertyDescriptor.TAttributeMask] = None
    ) -> Iterable[tuple[Property, Optional[PropertyDescriptor]]]:
        """Gets descriptor of properties.

        Parameters:
           properties: Properties.
           language: Language tag.
           descriptor_mask: Descriptor mask.

        Returns:
           An iterator of pairs: property, descriptor.
        """
        KIF_Object._check_arg_isinstance(
            properties, (Property, Iterable),
            self.get_property_descriptor, 'properties', 1)
        KIF_Object._check_arg_str(
            language, self.get_property_descriptor, 'language', 2)
        mask =\
            PropertyDescriptor.\
            _check_optional_arg_plain_descriptor_attribute_mask(
                descriptor_mask, PropertyDescriptor.ALL,
                self.get_property_descriptor, 'mask', 3)
        assert mask is not None
        if Property.test(properties):
            return self._get_property_descriptor(
                [cast(Property, properties)], language, mask)
        else:
            return self._get_property_descriptor(map(
                lambda e: cast(Property, Property.check(
                    e, self.get_property_descriptor)),
                properties), language, mask)

    def _get_property_descriptor(
            self,
            properties: Iterable[Property],
            lang: str,
            mask: PropertyDescriptor.AttributeMask
    ) -> Iterator[tuple[Property, Optional[PropertyDescriptor]]]:
        raise MustBeImplementedInSubclass

    def get_lexeme_descriptor(
            self,
            lexemes: Union[Lexeme, Iterable[Lexeme]]
    ) -> Iterable[tuple[Lexeme, Optional[LexemeDescriptor]]]:
        """Gets descriptor of lexemes.

        Parameters:
           lexemes: Lexemes.

        Returns:
           An iterator of pairs: lexeme, descriptor.
        """
        KIF_Object._check_arg_isinstance(
            lexemes, (Lexeme, Iterable),
            self.get_lexeme_descriptor, 'lexemes', 1)
        if Lexeme.test(lexemes):
            return self._get_lexeme_descriptor([cast(Lexeme, lexemes)])
        else:
            return self._get_lexeme_descriptor(map(
                lambda e: cast(Lexeme, Lexeme.check(
                    e, self.get_lexeme_descriptor)), lexemes))

    def _get_lexeme_descriptor(
            self,
            lexemes: Iterable[Lexeme]
    ) -> Iterator[tuple[Lexeme, Optional[LexemeDescriptor]]]:
        raise MustBeImplementedInSubclass
