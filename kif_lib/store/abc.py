# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..context import Context
from ..error import Error as KIF_Error
from ..error import ShouldNotGetHere
from ..model import (
    AnnotatedStatement,
    Filter,
    Fingerprint,
    KIF_Object,
    Quantity,
    ReferenceRecordSet,
    Snak,
    Statement,
    String,
    TFingerprint,
    TReferenceRecordSet,
    TTextLanguage,
)
from ..model.flags import Flags as KIF_Flags
from ..typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterator,
    Location,
    Set,
    TypeAlias,
    TypeVar,
)

at_property = property
T = TypeVar('T')
S = TypeVar('S')


class Store(Set):
    """Abstract base class for stores."""

    #: The store plugin registry.
    registry: Final[dict[str, type[Store]]] = {}

    #: The name of this store plugin.
    store_name: ClassVar[str]

    #: The description of this store plugin.
    store_description: ClassVar[str]

    @classmethod
    def _register(
            cls,
            store: type[Store],
            store_name: str,
            store_description: str
    ) -> None:
        store.store_name = store_name
        store.store_description = store_description
        cls.registry[store.store_name] = store

    @classmethod
    def __init_subclass__(
            cls,
            store_name: str,
            store_description: str
    ) -> None:
        Store._register(cls, store_name, store_description)

    def __new__(cls, store_name: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            store_name, store_name in cls.registry,
            f"no such store plugin '{store_name}'",
            Store, 'store_name', 1, ValueError)
        return super().__new__(cls.registry[store_name])  # pyright: ignore

    class Error(KIF_Error):
        """Base class for store errors."""

    @classmethod
    def _error(cls, details: str) -> Error:
        """Makes a store error.

        Parameters:
           details: Details.

        Returns:
           :class:`Error`.
        """
        return cls.Error(details)

    @classmethod
    def _should_not_get_here(
            cls,
            details: str | None = None
    ) -> ShouldNotGetHere:
        """Makes a "should not get here" error.

        Parameters:
           details: Details.

        Returns:
           :class:`ShouldNotGetHere`.
        """
        return KIF_Object._should_not_get_here(details)

    __slots__ = (
        '_context',
        '_base_filter',
        '_extra_references',
        '_flags',
        '_limit',
        '_page_size',
        '_timeout',
    )

    def __init__(
            self,
            *args: Any,
            base_filter: Filter | None = None,
            extra_references: TReferenceRecordSet | None = None,
            flags: TFlags | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> None:
        """
        Initializes :class:`Store`.

        Parameters:
           store_name: Name of the store plugin to instantiate.
           args: Arguments.
           base_filter: Base filter.
           extra_references: Extra references to attach to statements.
           flags: Store flags.
           limit: Limit (maximum number) of responses.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           kwargs: Extra keyword arguments.
        """
        self._flags = None
        self.flags = flags      # type: ignore
        self._base_filter = None
        self.set_base_filter(base_filter)
        self._extra_references = None
        self.set_extra_references(extra_references)
        self._limit = None
        self.set_limit(limit)
        self._page_size = None
        self.set_page_size(page_size)
        self._timeout = None
        self.set_timeout(timeout)

    @at_property
    def context(self) -> Context:
        """The current KIF context."""
        return self.get_context()

    def get_context(self, context: Context | None = None) -> Context:
        """Gets the current KIF context.

        If `context` is not ``None``, returns `context`.

        Returns:
           Context.
        """
        return Context.top(context)

# -- Base filter -----------------------------------------------------------

    @at_property
    def default_base_filter(self) -> Filter:
        """The default value for :attr:`Store.base_filter`."""
        return self.get_default_base_filter()

    def get_default_base_filter(self) -> Filter:
        """Gets the default value for :attr:`Store.base_filter`.

        Returns:
           Filter.
        """
        return self.context.options.store.base_filter

    #: Base filter.
    _base_filter: Filter | None

    @at_property
    def base_filter(self) -> Filter:
        """The base filter of store."""
        return self.get_base_filter()

    @base_filter.setter
    def base_filter(self, base_filter: Filter | None = None) -> None:
        self.set_base_filter(base_filter)

    def get_base_filter(
            self,
            default: Filter | None = None
    ) -> Filter:
        """Gets the base filter of store.

        If the base filter is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_base_filter`.

        Parameters:
           default: Default base filter.

        Returns:
           Filter.
        """
        if self._base_filter is not None:
            base_filter: Filter = self._base_filter
        elif default is not None:
            base_filter = default
        else:
            base_filter = self.default_base_filter
        return base_filter

    def set_base_filter(self, base_filter: Filter | None = None) -> None:
        """Sets the base filter of store.

        If `filter` is ``None``, resets base filter to
        :attr:`Store.default_base_filter`.

        Parameters:
           base_filter: Filter.
        """
        base_filter = Filter.check_optional(
            base_filter, None, self.set_base_filter, 'base_filter', 1)
        if (base_filter != self._base_filter and self._set_base_filter(
                self._base_filter, base_filter)):
            self._base_filter = base_filter

    def _set_base_filter(
            self,
            old: Filter | None,
            new: Filter | None
    ) -> bool:
        return True

    @at_property
    def subject(self) -> Fingerprint:
        """The subject fingerprint of the base filter of store."""
        return self.get_subject()

    @subject.setter
    def subject(self, subject: TFingerprint) -> None:
        self.set_subject(subject)

    def get_subject(self) -> Fingerprint:
        """Gets the subject fingerprint of the base filter of store.

        Returns:
           Fingerprint.
        """
        return self.base_filter.subject

    def set_subject(self, subject: TFingerprint | None = None) -> None:
        """Sets the subject fingerprint of the base filter of store.

        If `subject` is ``None``, assumes the full fingerprint.

        Parameters:
           subject: Fingerprint.
        """
        self.base_filter = self.base_filter.replace(subject=subject)

    @at_property
    def property(self) -> Fingerprint:
        """The property fingerprint of the base filter of store."""
        return self.get_property()

    @property.setter
    def property(self, property: TFingerprint) -> None:
        self.set_property(property)

    def get_property(self) -> Fingerprint:
        """Gets the property fingerprint of the base filter of store.

        Returns:
           Fingerprint.
        """
        return self.base_filter.property

    def set_property(self, property: TFingerprint) -> None:
        """Sets the property fingerprint of the base filter of store.

        If `property` is ``None``, assumes the full fingerprint.

        Parameters:
           property: Fingerprint.
        """
        self.base_filter = self.base_filter.replace(property=property)

    @at_property
    def value(self) -> Fingerprint:
        """The value fingerprint of the base filter of store."""
        return self.get_value()

    @value.setter
    def value(self, value: TFingerprint) -> None:
        self.set_value(value)

    def get_value(self) -> Fingerprint:
        """Gets the value fingerprint of the base filter of store.

        Returns:
           Fingerprint.
        """
        return self.base_filter.value

    def set_value(self, value: TFingerprint) -> None:
        """Sets the value fingerprint of the base filter of store.

        If `value` is ``None``, assumes the full fingerprint.

        Parameters:
           value: Fingerprint.
        """
        self.base_filter = self.base_filter.replace(value=value)

    @at_property
    def snak_mask(self) -> Filter.SnakMask:
        """The snak mask of the base filter of store."""
        return self.get_snak_mask()

    @snak_mask.setter
    def snak_mask(self, snak_mask: Filter.SnakMask) -> None:
        self.set_snak_mask(snak_mask)

    def get_snak_mask(self) -> Filter.SnakMask:
        """Gets the snak mask of the base filter of store.

        Returns:
           Snak mask.
        """
        return self.base_filter.snak_mask

    def set_snak_mask(self, snak_mask: Filter.TSnakMask) -> None:
        """Sets the snak mask of the base filter of store.

        Parameters:
           snak_mask: Snak mask.
        """
        self.base_filter = self.base_filter.replace(snak_mask=snak_mask)

    @at_property
    def subject_mask(self) -> Filter.DatatypeMask:
        """The subject mask of the base filter of store."""
        return self.get_subject_mask()

    @subject_mask.setter
    def subject_mask(self, subject_mask: Filter.DatatypeMask) -> None:
        self.set_subject_mask(subject_mask)

    def get_subject_mask(self) -> Filter.DatatypeMask:
        """Gets the subject mask of the base filter of store.

        Returns:
           Datatype mask.
        """
        return self.base_filter.subject_mask

    def set_subject_mask(self, subject_mask: Filter.TDatatypeMask) -> None:
        """Sets the subject mask of the base filter of store.

        Parameters:
           subject_mask: Datatype mask.
        """
        self.base_filter = self.base_filter.replace(subject_mask=subject_mask)

    @at_property
    def property_mask(self) -> Filter.DatatypeMask:
        """The property mask of the base filter of store."""
        return self.get_property_mask()

    @property_mask.setter
    def property_mask(self, property_mask: Filter.DatatypeMask) -> None:
        self.set_property_mask(property_mask)

    def get_property_mask(self) -> Filter.DatatypeMask:
        """Gets the property mask of the base filter of store.

        Returns:
           Datatype mask.
        """
        return self.base_filter.property_mask

    def set_property_mask(self, property_mask: Filter.TDatatypeMask) -> None:
        """Sets the property mask of the base filter of store.

        Parameters:
           property_mask: Datatype mask.
        """
        self.base_filter = self.base_filter.replace(
            property_mask=property_mask)

    @at_property
    def value_mask(self) -> Filter.DatatypeMask:
        """The value mask of the base filter of store."""
        return self.get_value_mask()

    @value_mask.setter
    def value_mask(self, value_mask: Filter.DatatypeMask) -> None:
        self.set_value_mask(value_mask)

    def get_value_mask(self) -> Filter.DatatypeMask:
        """Gets the value mask of the base filter of store.

        Returns:
           Datatype mask.
        """
        return self.base_filter.value_mask

    def set_value_mask(self, value_mask: Filter.TDatatypeMask) -> None:
        """Sets the value mask of the base filter of store.

        Parameters:
           value_mask: Datatype mask.
        """
        self.base_filter = self.base_filter.replace(value_mask=value_mask)

    @at_property
    def rank_mask(self) -> Filter.RankMask:
        """The rank mask of the base filter of store."""
        return self.get_rank_mask()

    @rank_mask.setter
    def rank_mask(self, rank_mask: Filter.RankMask) -> None:
        self.set_rank_mask(rank_mask)

    def get_rank_mask(self) -> Filter.RankMask:
        """Gets the rank mask of the base filter of store.

        Returns:
           Datatype mask.
        """
        return self.base_filter.rank_mask

    def set_rank_mask(self, rank_mask: Filter.TRankMask) -> None:
        """Sets the rank mask of the base filter of store.

        Parameters:
           rank_mask: Datatype mask.
        """
        self.base_filter = self.base_filter.replace(rank_mask=rank_mask)

    @at_property
    def language(self) -> str | None:
        """The language of the base filter of store."""
        return self.get_language()

    @language.setter
    def language(self, language: TTextLanguage | None) -> None:
        self.set_language(language)

    def get_language(self) -> str | None:
        """Gets the language of the base filter of store.

        Returns:
           Language.
        """
        return self.base_filter.language

    def set_language(self, language: TTextLanguage | None) -> None:
        """Sets the language of the base filter of store.

        Parameters:
           language: Language.
        """
        self.base_filter = self.base_filter.replace(language=language)

    @at_property
    def annotated(self) -> bool:
        """The annotated flag of the base filter of store."""
        return self.get_annotated()

    @annotated.setter
    def annotated(self, annotated: bool) -> None:
        self.set_annotated(annotated)

    def get_annotated(self) -> bool:
        """Gets the annotated flag of the base filter of store.

        Returns:
           Annotated flag.
        """
        return self.base_filter.annotated

    def set_annotated(self, annotated: bool) -> None:
        """Sets the annotated flag of the base filter of store.

        Parameters:
           annotated: Annotated flag.
        """
        self.base_filter = self.base_filter.replace(annotated=annotated)

# -- Extra references ------------------------------------------------------

    @at_property
    def default_extra_references(self) -> ReferenceRecordSet:
        """The default value for :attr:`Store.extra_references`."""
        return self.get_default_extra_references()

    def get_default_extra_references(self) -> ReferenceRecordSet:
        """Gets the default value for :attr:`Store.extra_references`.

        Returns:
           Reference record set.
        """
        return self.context.options.store.extra_references

    #: Extra references.
    _extra_references: ReferenceRecordSet | None

    @at_property
    def extra_references(self) -> ReferenceRecordSet:
        """The extra references of store."""
        return self.get_extra_references()

    @extra_references.setter
    def extra_references(
            self,
            references: TReferenceRecordSet | None = None
    ) -> None:
        self.set_extra_references(references)

    def get_extra_references(
            self,
            default: ReferenceRecordSet | None = None
    ) -> ReferenceRecordSet:
        """Gets the extra references of store.

        If the extra references is ``None``, returns `default`.

        If `default` is ``None``,
        assumes :attr:`Store.default_extra_references`.

        Parameters:
           default: Default reference record set.

        Returns:
           Reference record set.
        """
        if self._extra_references is not None:
            extra_references: ReferenceRecordSet = self._extra_references
        elif default is not None:
            extra_references = default
        else:
            extra_references = self.default_extra_references
        return extra_references

    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet | None = None
    ) -> None:
        """Sets the extra references of store.

        If `extra_references` is ``None``, resets extra references to
        :attr:`Store.default_extra_references`.

        Parameters:
           references: Reference record set.
        """
        extra_references = ReferenceRecordSet.check_optional(
            extra_references, None, self.set_extra_references,
            'extra_references', 1)
        if (extra_references != self._extra_references
            and self._set_extra_references(
                self._extra_references, extra_references)):
            self._extra_references = extra_references

    def _set_extra_references(
            self,
            old: ReferenceRecordSet | None,
            new: ReferenceRecordSet | None
    ) -> bool:
        return True

# -- Flags -----------------------------------------------------------------

    class Flags(KIF_Flags):
        """Store flags."""

        #: Whether to enable debugging.
        DEBUG = KIF_Flags.auto()

        #: Whether to fetch only the best ranked statements.
        BEST_RANK = KIF_Flags.auto()

        #: Whether to fetch value snaks.
        VALUE_SNAK = KIF_Flags.auto()

        #: Whether to fetch some-value snaks.
        SOME_VALUE_SNAK = KIF_Flags.auto()

        #: Whether to fetch no-value snaks.
        NO_VALUE_SNAK = KIF_Flags.auto()

        #: All flags.
        ALL = (
            DEBUG
            | BEST_RANK
            | VALUE_SNAK
            | SOME_VALUE_SNAK
            | NO_VALUE_SNAK)

    #: Whether to enable debugging.
    DEBUG: Final[Flags] = Flags.DEBUG

    #: Whether to fetch only the best ranked statements.
    BEST_RANK: Final[Flags] = Flags.BEST_RANK

    #: Whether to fetch value snaks.
    VALUE_SNAK: Final[Flags] = Flags.VALUE_SNAK

    #: Whether to fetch some-value snaks.
    SOME_VALUE_SNAK: Final[Flags] = Flags.SOME_VALUE_SNAK

    #: Whether to fetch no-value snaks.
    NO_VALUE_SNAK: Final[Flags] = Flags.NO_VALUE_SNAK

    #: Type alias for store flags.
    TFlags: TypeAlias = Flags | int

    @at_property
    def default_flags(self) -> Flags:
        """The default value for :attr:`Store.flags`."""
        return self.get_default_flags()

    def get_default_flags(self) -> Flags:
        """Gets the default value for :attr:`Store.flags`.

        Returns:
           Default store flags.
        """
        return self.context.options.store.flags

    #: Store flags.
    _flags: Flags | None

    @at_property
    def flags(self) -> Flags:
        """The store flags."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: TFlags | None) -> None:
        flags = self.Flags.check_optional(
            flags, None, self.set_flags, 'flags', 1)
        if flags != self._flags and self._set_flags(self._flags, flags):
            self._flags = flags

    def _set_flags(self, old: Flags | None, new: Flags | None) -> bool:
        return True

    def get_flags(self, default: Flags | None = None) -> Flags:
        """Gets the store flags.

        If `default` is ``None``, assumes :attr:`Store.default_flags`.

        Parameters:
           default: Default flags.

        Returns:
           Store flags.
        """
        if self._flags is not None:
            flags: Store.Flags = self._flags
        elif default is not None:
            flags = default
        else:
            flags = self.default_flags
        return flags

    def has_flags(self, flags: TFlags) -> bool:
        """Tests whether `flags` are set in store.

        Parameters:
           flags: Store flags.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        flags = self.Flags.check(flags, self.has_flags, 'flags', 1)
        return bool(self.flags & flags)

    def set_flags(self, flags: TFlags | None = None) -> None:
        """Sets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        if flags is None:
            self.flags = None   # type: ignore
        else:
            self.flags |= self.Flags.check(
                flags, self.set_flags, 'flags', 1)

    def unset_flags(self, flags: TFlags) -> None:
        """Unsets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        flags = self.Flags.check(flags, self.unset_flags, 'flags', 1)
        self.flags &= ~flags

# -- Limit -----------------------------------------------------------------

    @classmethod
    def _check_limit(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        return max(int(Quantity.check(
            arg, function, name, position).amount), 0)

    @classmethod
    def _do_check_optional(
            cls,
            check: Callable[
                [Any, Location | None, str | None, int | None], T],
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> T | None:
        if arg is None:
            arg = default
        if arg is None:
            return default
        else:
            return check(arg, function, name, position)

    @classmethod
    def _check_optional_limit(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        return cls._do_check_optional(
            cls._check_limit, arg, default, function, name, position)

    @at_property
    def max_limit(self) -> int:
        """The maximum value for :attr:`Store.limit`."""
        return self.get_max_limit()

    def get_max_limit(self) -> int:
        """Gets the maximum value for :attr:`Store.limit`.

        Returns:
           Maximum limit.
        """
        return self.context.options.store.max_limit

    @at_property
    def default_limit(self) -> int | None:
        """The default value for :attr:`Store.limit`."""
        return self.get_default_limit()

    def get_default_limit(self) -> int | None:
        """Gets the default value for :attr:`Store.limit`.

        Returns:
           Default limit or ``None``.
        """
        return self.context.options.store.limit

    #: Limit.
    _limit: int | None

    @at_property
    def limit(self) -> int | None:
        """The limit of store (maximum number of responses)."""
        return self.get_limit()

    @limit.setter
    def limit(self, limit: int | None = None) -> None:
        self.set_limit(limit)

    def get_limit(
            self,
            default: int | None = None
    ) -> int | None:
        """Gets the limit of store.

        If the limit is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_limit`.

        Parameters:
           default: Default limit.

        Returns:
           Limit or ``None``.
        """
        if self._limit is not None:
            limit: int | None = self._limit
        elif default is not None:
            limit = default
        else:
            limit = self.default_limit
        if limit is None:
            return limit
        else:
            return min(limit, self.max_limit)

    def set_limit(
            self,
            limit: int | None = None
    ) -> None:
        """Sets the limit of store.

        If `limit` is negative, assumes zero.

        If `limit` is ``None``, assumes :attr:`Store.default_limit`.

        Parameters:
           limit: Limit.
        """
        limit = self._check_optional_limit(
            limit, None, self.set_limit, 'limit', 1)
        if (limit != self._limit and self._set_limit(self._limit, limit)):
            self._limit = limit

    def _set_limit(self, old: int | None, new: int | None) -> bool:
        return True

# -- Page size -------------------------------------------------------------

    @classmethod
    def _check_page_size(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        return max(int(Quantity.check(
            arg, function, name, position).amount), 0)

    @classmethod
    def _check_optional_page_size(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        return cls._do_check_optional(
            cls._check_page_size, arg, default, function, name, position)

    @at_property
    def max_page_size(self) -> int:
        """The maximum value for :attr:`Store.page_size`."""
        return self.get_max_page_size()

    def get_max_page_size(self) -> int:
        """Gets the maximum value for :attr:`Store.page_size`.

        Returns:
           Maximum page size.
        """
        return self.context.options.store.max_page_size

    @at_property
    def default_page_size(self) -> int:
        """The default value for :attr:`Store.page_size`."""
        return self.get_default_page_size()

    def get_default_page_size(self) -> int:
        """Gets the default value for :attr:`Store.page_size`.

        Returns:
           Default page size.
        """
        return self.context.options.store.page_size

    #: Page size.
    _page_size: int | None

    @at_property
    def page_size(self) -> int:
        """The page size of store (size of response pages)."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: int | None = None) -> None:
        self.set_page_size(page_size)

    def get_page_size(
            self,
            default: int | None = None
    ) -> int:
        """Gets the page size of store.

        If the page size is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_page_size`.

        Parameters:
           default: Default page size.

        Returns:
           Page size.
        """
        if self._page_size is not None:
            page_size: int = self._page_size
        elif default is not None:
            page_size = default
        else:
            page_size = self.default_page_size
        return min(page_size, self.max_page_size)

    def set_page_size(
            self,
            page_size: int | None = None
    ) -> None:
        """Sets page size of store.

        If `page_size` is negative, assumes zero.

        If `page_size` is ``None``, assumes :attr:`Store.default_page_size`.

        Parameters:
           page_size: Page size.
        """
        page_size = self._check_optional_page_size(
            page_size, None, self.set_page_size, 'page_size', 1)
        if (page_size != self._page_size and self._set_page_size(
                self._page_size, page_size)):
            self._page_size = page_size

    def _set_page_size(self, old: int | None, new: int | None) -> bool:
        return True

# -- Timeout ---------------------------------------------------------------

    @classmethod
    def _check_timeout(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> float:
        return max(float(Quantity.check(
            arg, function, name, position).amount), 0.)

    @classmethod
    def _check_optional_timeout(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> float | None:
        return cls._do_check_optional(
            cls._check_timeout,
            arg, default, function, name, position)

    @at_property
    def max_timeout(self) -> float:
        """The maximum value for :attr:`Store.timeout`."""
        return self.get_max_timeout()

    def get_max_timeout(self) -> float:
        """Gets the maximum value for :attr:`Store.timeout`.

        Returns:
           Maximum timeout (in seconds).
        """
        return self.context.options.store.max_timeout

    @at_property
    def default_timeout(self) -> float | None:
        """The default value for :attr:`Store.timeout`."""
        return self.get_default_timeout()

    def get_default_timeout(self) -> float | None:
        """Gets the default value for :attr:`Store.timeout`.

        Returns:
           Timeout or ``None``.
        """
        return self.context.options.store.timeout

    #: Timeout (in seconds).
    _timeout: float | None

    @at_property
    def timeout(self) -> float | None:
        """The timeout of store (in seconds)."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: float | None = None) -> None:
        self.set_timeout(timeout)

    def get_timeout(
            self,
            default: float | None = None
    ) -> float | None:
        """Gets the timeout of store.

        If the timeout is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_timeout`.

        Parameters:
           default: Default timeout.

        Returns:
           Timeout or ``None``.
        """
        if self._timeout is not None:
            timeout: float | None = self._timeout
        elif default is not None:
            timeout = default
        else:
            timeout = self.default_timeout
        if timeout is None:
            return timeout
        else:
            return min(timeout, self.max_timeout)

    def set_timeout(
            self,
            timeout: float | None = None
    ) -> None:
        """Sets the timeout of store.

        If `timeout` is negative, assumes zero.

        If `timeout` is ``None``, assumes :attr:`Store.default_timeout`.

        Parameters:
           timeout: Timeout.
        """
        timeout = self._check_optional_timeout(
            timeout, None, self.set_timeout, 'timeout', 1)
        if (timeout != self._timeout and self._set_timeout(
                self._timeout, timeout)):
            self._timeout = timeout

    def _set_timeout(self, old: float | None, new: float | None) -> bool:
        return True

# -- Set interface ---------------------------------------------------------

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Store):
            ###
            # Prevent __eq__ from triggering content equality.
            ###
            return id(self) == id(other)
        else:
            return NotImplemented

    def __contains__(self, v: Any) -> bool:
        return self._contains(v) if isinstance(v, Statement) else False

    def __iter__(self) -> Iterator[Statement]:
        return self.filter()

    def __len__(self) -> int:
        return self.count()

# -- Statements ------------------------------------------------------------

    def ask(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None
    ) -> bool:
        """Tests whether some statement matches filter.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           subject_mask: Datatype mask.
           property_mask: Datatype mask.
           value_mask: Datatype mask.
           rank_mask: Rank mask.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._ask_tail(
            self._check_filter(
                subject=subject,
                property=property,
                value=value,
                snak_mask=snak_mask,
                subject_mask=subject_mask,
                property_mask=property_mask,
                value_mask=value_mask,
                rank_mask=rank_mask,
                language=language,
                annotated=annotated,
                snak=snak,
                filter=filter,
                function=self.ask))

    def _ask_tail(self, filter: Filter) -> bool:
        if filter.is_nonempty():
            return self._ask(filter)
        else:
            return False

    def _ask(self, filter: Filter) -> bool:
        return bool(next(self._filter(filter, 1, False), False))

    def contains(self, stmt: Statement) -> bool:
        """Tests whether statement occurs in store.

        Parameters:
           stmt: Statement.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        Statement.check(stmt, self.contains, 'stmt', 1)
        return self._contains(stmt)

    def _contains(self, stmt: Statement) -> bool:
        filter = self._normalize_filter(Filter.from_statement(stmt))
        if filter.is_nonempty():
            annotated = isinstance(stmt, AnnotatedStatement)
            return stmt in self.filter(filter=filter, annotated=annotated)
        else:
            return False

    def count(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None
    ) -> int:
        """Counts statements matching filter.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           subject_mask: Datatype mask.
           property_mask: Datatype mask.
           value_mask: Datatype mask.
           rank_mask: Rank mask.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter.

        Returns:
           The number of statements matching filter.
        """
        return self._count_tail(
            self._check_filter(
                subject=subject,
                property=property,
                value=value,
                snak_mask=snak_mask,
                subject_mask=subject_mask,
                property_mask=property_mask,
                value_mask=value_mask,
                rank_mask=rank_mask,
                language=language,
                annotated=annotated,
                snak=snak,
                filter=filter,
                function=self.count))

    def _count_tail(self, filter: Filter) -> int:
        if filter.is_nonempty():
            return self._count(filter)
        else:
            return 0

    def _count(self, filter: Filter) -> int:
        return sum(1 for _ in self._filter(filter, self.max_limit, True))

    def filter(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            limit: int | None = None,
            distinct: bool | None = None
    ) -> Iterator[Statement]:
        """Searches for statements matching filter.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           subject_mask: Datatype mask.
           property_mask: Datatype mask.
           value_mask: Datatype mask.
           rank_mask: Rank mask.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter filter.
           limit: Limit (maximum number) of statements to return.
           distinct: Whether to skip duplicated matches.

        Returns:
           An iterator of statements matching filter.
        """
        limit = self._check_optional_limit(
            limit, self.limit, self.filter, 'limit', 13)
        if limit is None:
            limit = self.default_limit
        if limit is None:
            limit = self.max_limit
        assert limit is not None
        ###
        # FIXME: Move this to an option.
        ###
        distinct = distinct if distinct is not None else True
        assert distinct is not None
        return self._filter_tail(
            self._check_filter(
                subject=subject,
                property=property,
                value=value,
                snak_mask=snak_mask,
                subject_mask=subject_mask,
                property_mask=property_mask,
                value_mask=value_mask,
                rank_mask=rank_mask,
                language=language,
                annotated=annotated,
                snak=snak,
                filter=filter,
                function=self.filter),
            limit, distinct)

    def _filter_tail(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        if limit > 0 and filter.is_nonempty():
            stmts = self._filter(filter, limit, distinct)
            if filter.annotated and self.extra_references:
                return map(lambda s: s.annotate(
                    references=self.extra_references), stmts)
            else:
                return stmts
        else:
            return iter(())

    def _filter(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        return iter(())

    def filter_annotated(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            limit: int | None = None,
            distinct: bool | None = None
    ) -> Iterator[AnnotatedStatement]:
        """:meth:`Store.filter` with annotations.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           subject_mask: Datatype mask.
           property_mask: Datatype mask.
           value_mask: Datatype mask.
           rank_mask: Rank mask.
           language: Language.
           annotated: Annotated flag (ignored).
           snak: Snak.
           filter: Filter.
           limit: Limit (maximum number) of statements to return.
           distinct: Whether to skip duplicated matches.

        Returns:
           An iterator of annotated statements matching filter.
        """
        return cast(Iterator[AnnotatedStatement], self.filter(
            subject=subject,
            property=property,
            value=value,
            snak_mask=snak_mask,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_mask=value_mask,
            rank_mask=rank_mask,
            language=language,
            annotated=True,     # force
            snak=snak,
            filter=filter,
            limit=limit,
            distinct=distinct))

    def _check_filter(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            function: Location | None = None
    ) -> Filter:
        subject = Fingerprint.check_optional(
            subject, None, function, 'subject', 1)
        property = Fingerprint.check_optional(
            property, None, function, 'property', 2)
        value = Fingerprint.check_optional(
            value, None, function, 'value', 3)
        snak_mask = Filter.SnakMask.check_optional(
            snak_mask, Filter.SnakMask.ALL, function, 'snak_mask', 4)
        subject_mask = Filter.DatatypeMask.check_optional(
            subject_mask, Filter.ENTITY, function, 'subject_mask', 5)
        property_mask = Filter.DatatypeMask.check_optional(
            property_mask, Filter.PROPERTY, function, 'property_mask', 6)
        value_mask = Filter.DatatypeMask.check_optional(
            value_mask, Filter.VALUE, function, 'value_mask', 7)
        rank_mask = Filter.RankMask.check_optional(
            rank_mask, Filter.RankMask.ALL, function, 'rank_mask', 8)
        language = String.check(
            language, function, 'language', 9).content\
            if language is not None else None
        annotated = bool(annotated)
        if filter is None:
            filter = Filter(
                subject=subject,
                property=property,
                value=value,
                snak_mask=snak_mask,
                subject_mask=subject_mask,
                property_mask=property_mask,
                value_mask=value_mask,
                rank_mask=rank_mask,
                language=language,
                annotated=annotated)
        else:
            filter = Filter.check(filter, function, 'filter', 12)
            filter = filter.combine(Filter(
                subject=subject,
                property=property,
                value=value,
                snak_mask=snak_mask,
                subject_mask=subject_mask,
                property_mask=property_mask,
                value_mask=value_mask,
                rank_mask=rank_mask,
                language=language)).replace(
                    annotated=filter.annotated or annotated)
        if snak is not None:
            filter = filter.combine(Filter.from_snak(None, Snak.check(
                snak, function, 'snak', 11))).replace(
                    annotated=filter.annotated or annotated)
        return self._normalize_filter(filter)

    def _normalize_filter(
            self,
            filter: Filter
    ) -> Filter:
        store_snak_mask = Filter.SnakMask(0)
        if self.has_flags(self.VALUE_SNAK):
            store_snak_mask |= Filter.VALUE_SNAK
        if self.has_flags(self.SOME_VALUE_SNAK):
            store_snak_mask |= Filter.SOME_VALUE_SNAK
        if self.has_flags(self.NO_VALUE_SNAK):
            store_snak_mask |= Filter.NO_VALUE_SNAK
        return filter.normalize().replace(
            filter.KEEP, filter.KEEP, filter.KEEP,
            filter.snak_mask & store_snak_mask)
