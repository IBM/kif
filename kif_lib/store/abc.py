# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import sys
from enum import auto, Flag

from ..cache import Cache
from ..error import Error as KIF_Error
from ..error import MustBeImplementedInSubclass, ShouldNotGetHere
from ..itertools import batched, chain
from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    Descriptor,
    Entity,
    EntityFingerprint,
    FilterPattern,
    Fingerprint,
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
    TCallable,
    TEntityFingerprint,
    Text,
    TFingerprint,
    TPropertyFingerprint,
    TReferenceRecordSet,
)
from ..typing import (
    Any,
    Callable,
    cast,
    Final,
    Iterable,
    Iterator,
    NoReturn,
    Optional,
    Set,
    TypeVar,
    Union,
)

T = TypeVar('T')
S = TypeVar('S')


class Store(Set):
    """Store factory.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Arguments to store plugin.
       extra_references: Set of extra references to attach to statements.
       flags: Configuration flags.
       page_size: Page size of paginated responses.
       timeout: Timeout of responses (in seconds).
       kwargs: Keyword arguments to store plugin.
    """

    #: The global plugin registry.
    registry: Final[dict[str, type['Store']]] = dict()

    #: The name of this store plugin.
    store_name: str

    #: The description of this store plugin.
    store_description: str

    @classmethod
    def _register(
            cls,
            store: type['Store'],
            store_name: str,
            store_description: str
    ):
        store.store_name = store_name
        store.store_description = store_description
        cls.registry[store.store_name] = store

    @classmethod
    def __init_subclass__(cls, store_name: str, store_description: str):
        Store._register(cls, store_name, store_description)

    def __new__(cls, store_name: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            store_name, store_name in cls.registry,
            f"no such store plugin '{store_name}'",
            Store, 'store_name', 1, ValueError)
        return super(Store, cls).__new__(cls.registry[store_name])

    class Error(KIF_Error):
        """Base class for store errors."""
        pass

    @classmethod
    def _error(cls, details: str) -> Error:
        """Makes a store error.

        Parameters:
           details: Details.

        Returns:
           Store error.
        """
        return cls.Error(details)

    @classmethod
    def _must_be_implemented_in_subclass(
            cls,
            details: Optional[str] = None
    ) -> MustBeImplementedInSubclass:
        """Makes a "must be implemented in subclass" error.

        Parameters:
           details: Details.

        Returns:
           :class:`MustBeImplementedInSubclass` error.
        """
        return KIF_Object._must_be_implemented_in_subclass(details)

    @classmethod
    def _should_not_get_here(
            cls,
            details: Optional[str] = None
    ) -> ShouldNotGetHere:
        """Makes a "should not get here" error.

        Parameters:
           details: Details.

        Returns:
           :class:`ShouldNotGetHere` error.
        """
        return KIF_Object._should_not_get_here(details)

    __slots__ = (
        '_cache',
        '_extra_references',
        '_flags',
        '_page_size',
        '_timeout',
    )

    def __init__(
            self,
            *args: Any,
            extra_references: Optional[TReferenceRecordSet] = None,
            flags: Optional['Flags'] = None,
            page_size: Optional[int] = None,
            timeout: Optional[int] = None,
            **kwargs: Any
    ):
        self._init_flags(flags)
        self._init_cache(self.has_flags(self.CACHE))
        self.set_extra_references(extra_references)
        self.set_page_size(page_size)
        self.set_timeout(timeout)

# -- Caching ---------------------------------------------------------------

    #: The object cache of store.
    _cache: Cache

    def _init_cache(self, enabled: bool):
        self._cache = Cache(enabled)

    def _cache_get_presence(
            self,
            obj: Union[Entity, Statement]
    ) -> Optional[bool]:
        """Gets the status of `obj` presence in cache.

        Returns:
           ``True`` if `obj` is present;
           ``False`` if `obj` is not present;
           ``None`` otherwise (`obj` presence is unknown).

        """
        return self._cache.get(obj, 'presence')

    def _cache_set_presence(
            self,
            obj: Union[Entity, Statement],
            status: Optional[bool] = None
    ) -> Optional[bool]:
        """Sets the status of `obj` presence in cache.

        Parameter:
           status: Presence status.

        Returns:
           Status.
        """
        if status is None:
            self._cache.unset(obj, 'presence')
            return None
        else:
            return self._cache.set(obj, 'presence', status)

# -- Extra references ------------------------------------------------------

    #: The default set of extra references.
    default_extra_references: Final[ReferenceRecordSet] =\
        ReferenceRecordSet()

    _extra_references: Optional[ReferenceRecordSet]

    @property
    def extra_references(self) -> ReferenceRecordSet:
        """The set of extra references to attach to statements."""
        return self.get_extra_references()

    @extra_references.setter
    def extra_references(
            self,
            references: Optional[TReferenceRecordSet] = None
    ):
        self.set_extra_references(references)

    def get_extra_references(
            self,
            default=default_extra_references
    ) -> ReferenceRecordSet:
        """Gets the set of extra references to attach to statements.

        If the set of extra references is ``None``, returns `default`.

        Parameters:
           default: Default set of references.

        Returns:
           Set of references.
        """
        return (self._extra_references
                if self._extra_references is not None else default)

    def set_extra_references(
            self,
            references: Optional[TReferenceRecordSet] = None
    ):
        """Sets the set of extra references to attach to statements.

        Parameters:
           references: Set of references.
        """
        self._extra_references =\
            ReferenceRecordSet._check_optional_arg_reference_record_set(
                references, None, self.set_extra_references, 'references', 1)

# -- Flags -----------------------------------------------------------------

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

    #: All flags.
    ALL = Flags.ALL

    #: The default flags.
    default_flags: Final['Flags'] = Flags.ALL

    _flags: 'Flags'

    def _init_flags(self, flags: Optional['Flags'] = None):
        if flags is None:
            self._flags = self.default_flags
        else:
            self._flags = self.Flags(flags)

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
        """Unsets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        self.flags &= ~flags

# -- Page size -------------------------------------------------------------

    #: The default page size.
    default_page_size: Final[int] = 100

    #: The maximum page size (absolute upper limit).
    maximum_page_size: Final[int] = sys.maxsize

    _page_size: Optional[int]

    @property
    def page_size(self) -> int:
        """The page size of paginated responses."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: Optional[int] = None):
        self.set_page_size(page_size)

    def get_page_size(
            self,
            default: Optional[int] = None
    ) -> int:
        """Gets the page size of paginated responses.

        If the page size is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_page_size`.

        Parameters:
           default: Default page size.

        Returns:
           Page size.
        """
        if self._page_size is not None:
            return self._page_size
        elif default is not None:
            return min(default, self.maximum_page_size)
        else:
            return self.default_page_size

    def set_page_size(
            self,
            page_size: Optional[int] = None
    ):
        """Sets page size of paginated responses.

        If `page_size` is negative, assumes ``None``.

        Parameters:
           page_size: Page size.
        """
        page_size = KIF_Object._check_optional_arg_int(
            page_size, None, self.set_page_size, 'page_size', 1)
        if page_size is None or page_size < 0:
            self._page_size = None
        else:
            self._page_size = page_size

    def _batched(
            self,
            it: Iterable[T],
            page_size: Optional[int] = None
    ) -> Iterable[tuple[T, ...]]:
        """Batches `it` into tuples of at most page-size length.

        If `page_size` is ``None``, assumes :attr:`Store.page_size`.

        Parameters:
           it: Iterable.
           page_size: Page size.

        Returns:
           The resulting tuples.
        """
        return batched(
            it, page_size if page_size is not None else self.page_size)

    def _chain_map_batched(
            self,
            op: Callable[[Iterable[T]], Iterator[S]],
            it: Iterable[T],
            page_size: Optional[int] = None
    ) -> Iterator[S]:
        """Batches `it`, applies `op` to the batches, and chain them.

        If `page_size` is ``None``, assumes :attr:`Store.page_size`.

        Parameters:
           op: Callable.
           it: Iterable.
           page_size: Page size.

        Returns:
           The resulting iterator.
        """
        return chain.from_iterable(map(op, self._batched(it, page_size)))

# -- Timeout ---------------------------------------------------------------

    #: The default timeout (in seconds).
    default_timeout: Final[Optional[int]] = None

    #: The maximum timeout (absolute upper limit, in seconds).
    maximum_timeout: Final[int] = sys.maxsize

    _timeout: Optional[int]

    @property
    def timeout(self) -> Optional[int]:
        """The timeout of responses (in seconds)."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: Optional[int] = None):
        self.set_timeout(timeout)

    def get_timeout(
            self,
            default: Optional[int] = None
    ) -> Optional[int]:
        """Gets the timeout of responses (in seconds).

        If the timeout is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_timeout`.

        Parameters:
           default: Default timeout.

        Returns:
           Timeout.
        """
        if self._timeout is not None:
            return self._timeout
        elif default is not None:
            return min(default, self.maximum_timeout)
        else:
            return self.default_timeout

    def set_timeout(
            self,
            timeout: Optional[int] = None
    ):
        """Sets the timeout of responses (in seconds).

        If `timeout` is negative, assumes ``None``.

        Parameters:
           timeout: Timeout (in seconds).
        """
        timeout = self._timeout = KIF_Object._check_optional_arg_int(
            timeout, None, self.set_timeout, 'timeout', 1)
        if timeout is None or timeout < 0:
            self._timeout = None
        else:
            self._timeout = timeout

# -- Set interface ---------------------------------------------------------

    def __contains__(self, v):
        return self.contains(v) if Statement.test(v) else False

    def __iter__(self):
        return self.filter()

    def __len__(self):
        return self.count()

# -- Statements ------------------------------------------------------------

    def contains(self, stmt: Statement) -> bool:
        """Tests whether statement is in store.

        Parameters:
           stmt: Statement.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        Statement.check(stmt, self.contains, 'stmt', 1)
        status = self._cache_get_presence(stmt)
        if status is None:
            pat = self._normalize_filter_pattern(
                FilterPattern.from_statement(stmt))
            status = self._contains_tail(pat)
            status = self._cache_set_presence(stmt, status)
        assert status is not None
        return status

    def _contains_tail(self, pattern: FilterPattern) -> bool:
        if pattern.is_nonempty():
            return self._contains(pattern)
        else:
            return False

    def _contains(self, pattern: FilterPattern) -> bool:
        return False

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
        return 0

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
        if limit is None:
            limit = self.maximum_page_size
        else:
            limit = max(limit, 0)
        if limit > 0 and pattern.is_nonempty():
            return self._filter(pattern, limit=limit)
        else:
            return iter(())

    def _filter(
            self,
            pattern: FilterPattern,
            limit: int
    ) -> Iterator[Statement]:
        return iter(())

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
           An iterator of pairs "(statement, annotation record set)".
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
           An iterator of pairs "(statement, annotation record set)".
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
           An iterator of pairs "(statement, annotation record set)".
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
        return map(lambda stmt: (stmt, None), stmts)

# -- Entities --------------------------------------------------------------

    def has_item(
        self,
        items: Union[Item, Iterable[Item]],
    ) -> Iterator[tuple[Item, bool]]:
        """Tests whether items are in store.

        Parameters:
           items: Items.

        Returns:
           An iterator of pairs "(item, status)".
        """
        return iter(())

# -- Descriptors -----------------------------------------------------------

    def get_descriptor(
            self,
            entities: Union[Entity, Iterable[Entity]],
            language: Optional[str] = None,
            mask: Optional[Descriptor.TAttributeMask] = None
    ) -> Iterator[tuple[Entity, Optional[Descriptor]]]:
        """Gets the descriptor of `entities`.

        Parameters:
           entities: Entities.
           language: Language tag.
           mask: Descriptor mask.

        Returns:
           An iterator of pairs "(entity, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            entities, (Entity, Iterable), self.get_descriptor, 'entities', 1)
        language = KIF_Object._check_optional_arg_str(
            language, Text.default_language,
            self.get_descriptor, 'language', 2)
        assert language is not None
        mask = Descriptor._check_optional_arg_descriptor_attribute_mask(
            mask, Descriptor.ALL, self.get_descriptor, 'mask', 3)
        assert mask is not None
        if Entity.test(entities):
            return self._get_descriptor_tail(
                [cast(Entity, entities)], language, mask)
        else:
            return self._get_descriptor_tail(map(
                lambda e: cast(Entity, Entity.check(
                    e, self.get_descriptor)), entities), language, mask)

    def _get_descriptor_tail(
            self,
            entities: Iterable[Entity],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Entity, Optional[Descriptor]]]:
        return self._chain_map_batched(
            lambda batch: self._get_descriptor(batch, language, mask),
            entities, min(3 * self.page_size, self.maximum_page_size))

    def _get_descriptor(
            self,
            entities: Iterable[Entity],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Entity, Optional[Descriptor]]]:
        items: list[Item] = []
        properties: list[Property] = []
        lexemes: list[Lexeme] = []
        for entity in entities:
            if entity.is_item():
                items.append(cast(Item, entity))
            elif entity.is_property():
                properties.append(cast(Property, entity))
            elif entity.is_lexeme():
                lexemes.append(cast(Lexeme, entity))
            else:
                raise self._should_not_get_here()
        desc = dict(chain(
            self._get_item_descriptor(items, language, mask)
            if items else iter(()),
            self._get_property_descriptor(properties, language, mask)
            if properties else iter(()),
            self._get_lexeme_descriptor(lexemes, mask)
            if lexemes else iter(())))
        for entity in entities:
            assert entity in desc
            yield entity, desc[entity]

    def get_item_descriptor(
            self,
            items: Union[Item, Iterable[Item]],
            language: Optional[str] = None,
            mask: Optional[Descriptor.TAttributeMask] = None
    ) -> Iterator[tuple[Item, Optional[ItemDescriptor]]]:
        """Gets the descriptor of `items`.

        Parameters:
           items: Items.
           language: Language tag.
           mask: Descriptor mask.

        Returns:
           An iterator of pairs "(item, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            items, (Item, Iterable),
            self.get_item_descriptor, 'items', 1)
        language = KIF_Object._check_optional_arg_str(
            language, Text.default_language,
            self.get_item_descriptor, 'language', 2)
        assert language is not None
        mask = Descriptor._check_optional_arg_descriptor_attribute_mask(
            mask, Descriptor.ALL, self.get_item_descriptor, 'mask', 3)
        assert mask is not None
        if Item.test(items):
            return self._get_item_descriptor_tail(
                [cast(Item, items)], language, mask)
        else:
            return self._get_item_descriptor_tail(map(
                lambda e: cast(Item, Item.check(
                    e, self.get_item_descriptor)), items), language, mask)

    def _get_item_descriptor_tail(
            self,
            items: Iterable[Item],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Item, Optional[ItemDescriptor]]]:
        return self._chain_map_batched(
            lambda batch: self._get_item_descriptor(batch, language, mask),
            items)

    def _get_item_descriptor(
            self,
            items: Iterable[Item],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Item, Optional[ItemDescriptor]]]:
        return map(lambda item: (item, None), items)

    def get_property_descriptor(
            self,
            properties: Union[Property, Iterable[Property]],
            language: Optional[str] = None,
            mask: Optional[Descriptor.TAttributeMask] = None
    ) -> Iterator[tuple[Property, Optional[PropertyDescriptor]]]:
        """Gets the descriptor of `properties`.

        Parameters:
           properties: Properties.
           language: Language tag.
           mask: Descriptor mask.

        Returns:
           An iterator of pairs "(property, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            properties, (Property, Iterable),
            self.get_property_descriptor, 'properties', 1)
        language = KIF_Object._check_optional_arg_str(
            language, Text.default_language,
            self.get_property_descriptor, 'language', 2)
        assert language is not None
        mask = Descriptor._check_optional_arg_descriptor_attribute_mask(
            mask, Descriptor.ALL, self.get_property_descriptor, 'mask', 3)
        assert mask is not None
        if Property.test(properties):
            return self._get_property_descriptor_tail(
                [cast(Property, properties)], language, mask)
        else:
            return self._get_property_descriptor_tail(map(
                lambda e: cast(Property, Property.check(
                    e, self.get_property_descriptor)),
                properties), language, mask)

    def _get_property_descriptor_tail(
            self,
            properties: Iterable[Property],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Property, Optional[PropertyDescriptor]]]:
        return self._chain_map_batched(
            lambda batch: self._get_property_descriptor(batch, language, mask),
            properties)

    def _get_property_descriptor(
            self,
            properties: Iterable[Property],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Property, Optional[PropertyDescriptor]]]:
        return map(lambda property: (property, None), properties)

    def get_lexeme_descriptor(
            self,
            lexemes: Union[Lexeme, Iterable[Lexeme]],
            mask: Optional[Descriptor.TAttributeMask] = None
    ) -> Iterator[tuple[Lexeme, Optional[LexemeDescriptor]]]:
        """Gets the descriptor of `lexemes`.

        Parameters:
           lexemes: Lexemes.

        Returns:
           An iterator of pairs "(lexeme, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            lexemes, (Lexeme, Iterable),
            self.get_lexeme_descriptor, 'lexemes', 1)
        mask = Descriptor._check_optional_arg_descriptor_attribute_mask(
            mask, Descriptor.ALL, self.get_lexeme_descriptor, 'mask', 3)
        assert mask is not None
        if Lexeme.test(lexemes):
            return self._get_lexeme_descriptor_tail(
                [cast(Lexeme, lexemes)], mask)
        else:
            return self._get_lexeme_descriptor_tail(map(
                lambda e: cast(Lexeme, Lexeme.check(
                    e, self.get_lexeme_descriptor)), lexemes), mask)

    def _get_lexeme_descriptor_tail(
            self,
            lexemes: Iterable[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Lexeme, Optional[LexemeDescriptor]]]:
        return self._chain_map_batched(
            lambda batch: self._get_lexeme_descriptor(batch, mask), lexemes)

    def _get_lexeme_descriptor(
            self,
            lexemes: Iterable[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Lexeme, Optional[LexemeDescriptor]]]:
        return map(lambda lexeme: (lexeme, None), lexemes)
