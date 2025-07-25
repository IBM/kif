# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import functools
import sys

from .. import itertools
from ..context import Context
from ..engine import _EngineOptions, Engine, EngineOptions
from ..model import (
    AnnotatedStatement,
    Entity,
    Filter,
    Fingerprint,
    KIF_Object,
    Property,
    ReferenceRecordSet,
    Snak,
    Statement,
    String,
    TFingerprint,
    TQuantity,
    TReferenceRecordSet,
    TTextLanguage,
    Value,
    ValuePair,
    ValueSnak,
)
from ..typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    cast,
    ClassVar,
    Iterable,
    Iterator,
    Location,
    Mapping,
    override,
    TypeVar,
)

at_property = property
T = TypeVar('T')


@dataclasses.dataclass
class _StoreOptions(EngineOptions):
    """Base class for store options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_STORE_DEBUG',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_MAX_LIMIT',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_STORE_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_STORE_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._init_base_filter(kwargs)
        self._init_distinct(kwargs)
        self._init_distinct_window_size(kwargs)
        self._init_max_distinct_window_size(kwargs)
        self._init_extra_references(kwargs)
        self._init_omega(kwargs)

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.store

    # -- base_filter --

    #: The default value for the base filter option.
    DEFAULT_BASE_FILTER: ClassVar[Filter] = Filter()

    _base_filter: Filter | None

    def _init_base_filter(self, kwargs: dict[str, Any]) -> None:
        self.base_filter = kwargs.get(
            '_base_filter', self.DEFAULT_BASE_FILTER)

    @property
    def base_filter(self) -> Filter:
        """The base filter option."""
        return self.get_base_filter()

    @base_filter.setter
    def base_filter(self, base_filter: Filter) -> None:
        self.set_base_filter(base_filter)

    def get_base_filter(self) -> Filter:
        """Gets the base filter option.

        Returns:
           Filter.
        """
        assert self._base_filter is not None
        return self._base_filter

    def set_base_filter(
            self,
            base_filter: Filter,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the base filter option.

        Parameters:
           base_filter: Filter.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._base_filter = Filter.check(
            base_filter, function, name, position)

    # -- distinct --

    #: The default value for the distinct option.
    DEFAULT_DISTINCT: ClassVar[bool] = True

    _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_STORE_DISTINCT',), DEFAULT_DISTINCT)

    _distinct: bool | None

    def _init_distinct(self, kwargs: dict[str, Any]) -> None:
        self.distinct = cast(bool, kwargs.get(
            '_distinct', self.getenv_optional_bool(*self._v_distinct)))

    @property
    def distinct(self) -> bool:
        """Whether to suppress duplicate results."""
        return self.get_distinct()

    @distinct.setter
    def distinct(self, distinct: bool) -> None:
        self.set_distinct(distinct)

    def get_distinct(self) -> bool:
        """Gets the distinct flag.

        Returns:
           Distinct flag.
        """
        assert self._distinct is not None
        return self._distinct

    def set_distinct(
            self,
            distinct: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the distinct flag.

        Parameters:
           distinct: Distinct flag.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._distinct = bool(distinct)

    # -- max_distinct_window_size -- #

    #: The default value for the max. distinct window-size option.
    DEFAULT_MAX_DISTINCT_WINDOW_SIZE: ClassVar[int] = sys.maxsize

    _v_max_distinct_window_size: ClassVar[
        tuple[Iterable[str], int | None]] = (
            ('KIF_STORE_MAX_DISTINCT_WINDOW_SIZE',),
            DEFAULT_MAX_DISTINCT_WINDOW_SIZE)

    _max_distinct_window_size: int | None

    def _init_max_distinct_window_size(
            self,
            kwargs: dict[str, Any]
    ) -> None:
        self.max_distinct_window_size = cast(int, kwargs.get(
            '_max_distinct_window_size', self.getenv_optional_int(
                *self._v_max_distinct_window_size)))

    @property
    def max_distinct_window_size(self) -> int:
        """The maximum distinct window-size option."""
        return self.get_max_distinct_window_size()

    @max_distinct_window_size.setter
    def max_distinct_window_size(
            self, max_distinct_window_size: TQuantity
    ) -> None:
        self.set_max_distinct_window_size(max_distinct_window_size)

    def get_max_distinct_window_size(self) -> int:
        """Gets the maximum distinct window-size option.

        Returns:
           Distinct window-size.
        """
        assert self._max_distinct_window_size is not None
        return self._max_distinct_window_size

    def set_max_distinct_window_size(
            self,
            max_distinct_window_size: TQuantity,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the maximum distinct window-size option.

        If `max_distinct_window_size` is negative or zero, assumes 1.

        Parameters:
           max_distinct_window_size: Max. distinct window-size.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._max_distinct_window_size =\
            self._check_distinct_window_size(
                max_distinct_window_size, function, name, position)

    # -- distinct_window_size --

    @classmethod
    def _check_distinct_window_size(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        return max(cls._check_int(arg, function, name, position), 1)

    @classmethod
    def _check_optional_distinct_window_size(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        return cls._do_check_optional(
            cls._check_distinct_window_size,
            arg, default, function, name, position)

    #: The default value for the distinct window-size option.
    DEFAULT_DISTINCT_WINDOW_SIZE: ClassVar[int] = 10000

    _v_distinct_window_size: ClassVar[
        tuple[Iterable[str], int | None]] = (
            ('KIF_STORE_DISTINCT_WINDOW_SIZE',),
            DEFAULT_DISTINCT_WINDOW_SIZE)

    _distinct_window_size: int | None

    def _init_distinct_window_size(self, kwargs: dict[str, Any]) -> None:
        self.distinct_window_size = cast(int, kwargs.get(
            '_distinct_window_size', self.getenv_optional_int(
                *self._v_distinct_window_size)))

    @property
    def distinct_window_size(self) -> int:
        """The distinct window-size option."""
        return self.get_distinct_window_size()

    @distinct_window_size.setter
    def distinct_window_size(
            self,
            distinct_window_size: TQuantity
    ) -> None:
        self.set_distinct_window_size(distinct_window_size)

    def get_distinct_window_size(self) -> int:
        """Gets the distinct window-size option.

        Returns:
           Distinct window-size.
        """
        assert self._distinct_window_size is not None
        return self._distinct_window_size

    def set_distinct_window_size(
            self,
            distinct_window_size: TQuantity,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the distinct window-size option.

        If `distinct_window_size` is negative, assumes zero.

        Parameters:
           distinct_window_size: Distinct window-size.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._distinct_window_size = self._check_distinct_window_size(
            distinct_window_size, function, name, position)

    # -- extra_references --

    #: The default value for the extra references option
    DEFAULT_EXTRA_REFERENCES: ClassVar[ReferenceRecordSet] =\
        ReferenceRecordSet()

    _extra_references: ReferenceRecordSet | None

    def _init_extra_references(self, kwargs: dict[str, Any]) -> None:
        self.extra_references = cast(ReferenceRecordSet, kwargs.get(
            '_extra_references', self.DEFAULT_EXTRA_REFERENCES))

    @property
    def extra_references(self) -> ReferenceRecordSet:
        """The extra-references option."""
        return self.get_extra_references()

    @extra_references.setter
    def extra_references(
            self,
            extra_references: TReferenceRecordSet
    ) -> None:
        self.set_extra_references(extra_references)

    def get_extra_references(self) -> ReferenceRecordSet:
        """Gets the extra-references option.

        Returns:
           Reference record set.
        """
        assert self._extra_references is not None
        return self._extra_references

    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the extra-references option.

        Parameters:
           extra_references: Reference record set.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._extra_references = ReferenceRecordSet.check(
            extra_references, function, name, position)

    # -- omega --

    @classmethod
    def _check_omega(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        return max(cls._check_int(arg, function, name, position), 1)

    @classmethod
    def _check_optional_omega(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        return cls._do_check_optional(
            cls._check_omega, arg, default, function, name, position)

    #: The default value for the omega option.
    DEFAULT_OMEGA: ClassVar[int] = 2

    _v_omega: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_OMEGA',), DEFAULT_OMEGA)

    _omega: int | None

    def _init_omega(self, kwargs: dict[str, Any]) -> None:
        self.omega = cast(int, kwargs.get(
            '_omega', self.getenv_optional_int(*self._v_omega)))

    @property
    def omega(self) -> int:
        """The omega option."""
        return self.get_omega()

    @omega.setter
    def omega(self, omega: TQuantity) -> None:
        self.set_omega(omega)

    def get_omega(self) -> int:
        """Gets the omega option.

        Returns:
           Omega.
        """
        assert self._omega is not None
        return self._omega

    def set_omega(
            self,
            omega: TQuantity,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the omega option.

        If `omega` is zero or negative, assumes 1.

        Parameters:
           omega: Omega.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._omega = self._check_omega(
            omega, function, name, position)


@dataclasses.dataclass
class StoreOptions(_StoreOptions):
    """Base class for store options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @override
    def _init_base_filter(self, kwargs: dict[str, Any]) -> None:
        self.set_base_filter(kwargs.get('_base_filter'))

    @override
    def get_base_filter(self) -> Filter:
        return self._do_get('_base_filter', super().get_base_filter)

    @override
    def set_base_filter(
            self,
            base_filter: Filter | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(base_filter, '_base_filter', functools.partial(
            super().set_base_filter,
            function=function, name=name, position=position))

    @override
    def get_distinct(self) -> bool:
        return self._do_get('_distinct', super().get_distinct)

    @override
    def set_distinct(
            self,
            distinct: bool | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(distinct, '_distinct', functools.partial(
            super().set_distinct,
            function=function, name=name, position=position))

    @override
    def get_max_distinct_window_size(self) -> int:
        return self._do_get(
            '_max_distinct_window_size',
            super().get_max_distinct_window_size)

    @override
    def set_max_distinct_window_size(
            self,
            max_distinct_window_size: TQuantity | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(
            max_distinct_window_size,
            '_max_distinct_window_size', functools.partial(
                super().set_max_distinct_window_size,
                function=function, name=name, position=position))

    @override
    def get_distinct_window_size(self) -> int:
        return self._do_get(
            '_distinct_window_size', super().get_distinct_window_size)

    @override
    def set_distinct_window_size(
            self,
            distinct_window_size: TQuantity | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(
            distinct_window_size,
            '_distinct_window_size', functools.partial(
                super().set_distinct_window_size,
                function=function, name=name, position=position))

    @override
    def _init_extra_references(self, kwargs: dict[str, Any]) -> None:
        self.set_extra_references(kwargs.get('_extra_references'))

    @override
    def get_extra_references(self) -> ReferenceRecordSet:
        return self._do_get(
            '_extra_references', super().get_extra_references)

    @override
    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(
            extra_references, '_extra_references', functools.partial(
                super().set_extra_references,
                function=function, name=name, position=position))

    @override
    def get_omega(self) -> int:
        return self._do_get('_omega', super().get_omega)

    @override
    def set_omega(
            self,
            omega: TQuantity | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(omega, '_omega', functools.partial(
            super().set_omega,
            function=function, name=name, position=position))


# == Store =================================================================

TOptions = TypeVar('TOptions', bound=StoreOptions, default=StoreOptions)


class Store(Engine[TOptions]):
    """Abstract base class for store engines."""

    #: The store plugin registry.
    registry: ClassVar[Mapping[str, type[Store]]] = {}  # pyright: ignore

    #: The name of this store plugin.
    store_name: ClassVar[str]

    #: The description of this store plugin.
    store_description: ClassVar[str]

    @classmethod
    def __init_subclass__(
            cls,
            store_name: str,
            store_description: str
    ) -> None:
        Store._register_plugin(cls, store_name, store_description)
        cls.store_name = cls.plugin_name
        cls.store_description = cls.plugin_description

    def __new__(cls, store_name: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            store_name, store_name in cls.registry,
            f"no such store plugin '{store_name}'",
            Store, 'store_name', 1, ValueError)
        return super().__new__(cls.registry[store_name])  # pyright: ignore

    class Error(Engine.Error):
        """Base class for store errors."""

    @override
    @classmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        return cast(TOptions, cls.get_context(context).options.store.empty)

# -- Initialization --------------------------------------------------------

    #: Store options.
    _options: TOptions

    def __init__(
            self,
            *args: Any,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            context: Context | None = None,
            **kwargs: Any
    ) -> None:
        """
        Initializes :class:`Store`.

        Parameters:
           store_name: Name of the store plugin to instantiate.
           args: Arguments.
           base_filter: Base filter.
           debug: Whether to enable debugging mode.
           distinct: Whether to suppress duplicates.
           distinct_window_size: Size of distinct look-back window.
           extra_references: Extra references to attach to statements.
           limit: Limit (maximum number) of responses.
           lookahead: Number of pages to lookahead asynchronously.
           omega: Maximum number of disjoint subqueries.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           context: Context.
           kwargs: Other keyword arguments.
        """
        super().__init__(
            *args,
            base_filter=base_filter,
            debug=debug,
            distinct=distinct,
            distinct_window_size=distinct_window_size,
            extra_references=extra_references,
            limit=limit,
            lookahead=lookahead,
            omega=omega,
            page_size=page_size,
            timeout=timeout,
            context=context,
            **kwargs)

    @override
    def _update_options(self, **kwargs: Any) -> None:
        super()._update_options(**kwargs)
        if 'base_filter' in kwargs:
            self.set_base_filter(kwargs['base_filter'])
        if 'distinct' in kwargs:
            self.set_distinct(kwargs['distinct'])
        if 'distinct_window_size' in kwargs:
            self.set_distinct_window_size(kwargs['distinct_window_size'])
        if 'extra_references' in kwargs:
            self.set_extra_references(kwargs['extra_references'])
        if 'omega' in kwargs:
            self.set_omega(kwargs['omega'])

# -- Base filter -----------------------------------------------------------

    @at_property
    def default_base_filter(self) -> Filter:
        """The default value for :attr:`Store.base_filter`."""
        return self.get_default_base_filter()

    def get_default_base_filter(self) -> Filter:
        """Gets the default value for :attr:`Store.base_filter`.

        Returns:
           Default filter.
        """
        return self.get_default_options().base_filter

    @at_property
    def base_filter(self) -> Filter:
        """The base filter of store."""
        return self.get_base_filter()

    @base_filter.setter
    def base_filter(self, base_filter: Filter | None = None) -> None:
        self.set_base_filter(base_filter)

    def get_base_filter(self) -> Filter:
        """Gets the base filter of store.

        Returns:
           Filter.
        """
        return self.options.base_filter

    def set_base_filter(self, base_filter: Filter | None = None) -> None:
        """Sets the base filter of store.

        If `filter` is ``None``, resets it to the default.

        Parameters:
           base_filter: Filter.
        """
        self._set_option_with_hooks(
            base_filter,
            self.options.get_base_filter,
            functools.partial(
                self.options.set_base_filter,
                function=self.set_base_filter,
                name='base_filter',
                position=1),
            self._set_base_filter)

    def _set_base_filter(self, base_filter: Filter) -> bool:
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
    def property_mask(self) -> Filter.PropertyMask:
        """The property mask of the base filter of store."""
        return self.get_property_mask()

    @property_mask.setter
    def property_mask(self, property_mask: Filter.PropertyMask) -> None:
        self.set_property_mask(property_mask)

    def get_property_mask(self) -> Filter.PropertyMask:
        """Gets the property mask of the base filter of store.

        Returns:
           Datatype mask.
        """
        return self.base_filter.property_mask

    def set_property_mask(self, property_mask: Filter.TPropertyMask) -> None:
        """Sets the property mask of the base filter of store.

        Parameters:
           property_mask: Property mask.
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
    def best_ranked(self) -> bool:
        """The best-ranked flag of the base filter of store."""
        return self.get_best_ranked()

    @best_ranked.setter
    def best_ranked(self, best_ranked: bool) -> None:
        self.set_best_ranked(best_ranked)

    def get_best_ranked(self) -> bool:
        """Gets the best-ranked flag of the base filter of store.

        Returns:
           Best-ranked flag.
        """
        return self.base_filter.best_ranked

    def set_best_ranked(self, best_ranked: bool) -> None:
        """Sets the best-ranked flag of the base filter of store.

        Parameters:
           best_ranked: Best-ranked flag.
        """
        self.base_filter = self.base_filter.replace(best_ranked=best_ranked)

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

# -- Distinct --------------------------------------------------------------

    @at_property
    def default_distinct(self) -> bool:
        """The default value for :attr:`Store.distinct`."""
        return self.get_default_distinct()

    def get_default_distinct(self) -> bool:
        """Gets the default value for :attr:`Store.distinct`.

        Returns:
           Default distinct flag.
        """
        return self.get_default_options().distinct

    @at_property
    def distinct(self) -> bool:
        """The distinct flag of store (whether to suppress duplicates)."""
        return self.get_distinct()

    @distinct.setter
    def distinct(self, distinct: bool | None = None) -> None:
        self.set_distinct(distinct)

    def get_distinct(self) -> bool:
        """Gets the distinct flag of store.

        Returns:
           Distinct flag.
        """
        return self.options.distinct

    def set_distinct(self, distinct: bool | None = None) -> None:
        """Sets the distinct flag of store.

        If `distinct` is ``None``, resets it to the default.

        Parameters:
           distinct: Distinct flag.
        """
        self._set_option_with_hooks(
            distinct,
            self.options.get_distinct,
            functools.partial(
                self.options.set_distinct,
                function=self.set_distinct,
                name='distinct',
                position=1),
            self._set_distinct)

    def _set_distinct(self, distinct: bool) -> bool:
        return True

# -- Distinct window-size --------------------------------------------------

    @at_property
    def max_distinct_window_size(self) -> int:
        """The maximum value for :attr:`Store.distinct_window_size`."""
        return self.get_max_distinct_window_size()

    def get_max_distinct_window_size(self) -> int:
        """Gets the maximum value for :attr:`Store.distinct_window_size`.

        Returns:
           Maximum distinct window-size.
        """
        return self.get_default_options().max_distinct_window_size

    @at_property
    def default_distinct_window_size(self) -> int:
        """The default value for :attr:`Store.distinct_window_size`."""
        return self.get_default_distinct_window_size()

    def get_default_distinct_window_size(self) -> int:
        """Gets the default value for :attr:`Store.distinct_window_size`.

        Returns:
           Default distinct window-size.
        """
        return self.get_default_options().distinct_window_size

    @at_property
    def distinct_window_size(self) -> int:
        """The distinct window-size of store."""
        return self.get_distinct_window_size()

    @distinct_window_size.setter
    def distinct_window_size(
            self,
            distinct_window_size: int | None = None
    ) -> None:
        self.set_distinct_window_size(distinct_window_size)

    def get_distinct_window_size(self) -> int:
        """Gets the distinct window-size of store.

        Returns:
           Page size.
        """
        return min(
            self.options.distinct_window_size,
            self.max_distinct_window_size)

    def set_distinct_window_size(
            self,
            distinct_window_size: int | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the page size of store.

        If `distinct_window_size` is negative or zero, assumes 1.

        If `distinct_window_size` is ``None``, resets it to the default.

        Parameters:
           distinct_window_size: Page size.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._set_option_with_hooks(
            distinct_window_size,
            self.options.get_distinct_window_size,
            functools.partial(
                self.options.set_distinct_window_size,
                function=self.set_distinct_window_size,
                name='distinct_window_size',
                position=1),
            self._set_distinct_window_size)

    def _set_distinct_window_size(self, distinct_window_size: int) -> bool:
        return True

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
        return self.get_default_options().extra_references

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

    def get_extra_references(self) -> ReferenceRecordSet:
        """Gets the extra references of store.

        Returns:
           Reference record set.
        """
        return self.options.extra_references

    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet | None = None
    ) -> None:
        """Sets the extra references of store.

        If `extra_references` is ``None``, resets it to the default.

        Parameters:
           references: Reference record set.
        """
        self._set_option_with_hooks(
            extra_references,
            self.options.get_extra_references,
            functools.partial(
                self.options.set_extra_references,
                function=self.set_extra_references,
                name='extra_references',
                position=1),
            self._set_extra_references)

    def _set_extra_references(
            self,
            extra_references: ReferenceRecordSet
    ) -> bool:
        return True

# -- Omega -----------------------------------------------------------------

    @at_property
    def default_omega(self) -> int:
        """The default value for :attr:`Store.omega`."""
        return self.get_default_omega()

    def get_default_omega(self) -> int:
        """Gets the default value for :attr:`Store.omega`.

        Returns:
           Default omega value.
        """
        return self.get_default_options().omega

    @at_property
    def omega(self) -> int:
        """The omega of store."""
        return self.get_omega()

    @omega.setter
    def omega(self, omega: int | None = None) -> None:
        self.set_omega(omega)

    def get_omega(self) -> int:
        """Gets the omega of store.

        Returns:
           Omega.
        """
        return self.options.omega

    def set_omega(self, omega: int | None = None) -> None:
        """Sets the omega of store.

        If `omega` is negative, assumes one.

        If `omega` is ``None``, resets it to the default.

        Parameters:
           omega: Omega.
        """
        self._set_option_with_hooks(
            omega,
            self.options.get_omega,
            functools.partial(
                self.options.set_omega,
                function=self.set_omega,
                name='omega',
                position=1),
            self._set_omega)

    def _set_omega(self, omega: int) -> bool:
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
        return self._contains_tail(v) if isinstance(v, Statement) else False

    def __iter__(self) -> Iterator[Statement]:
        return self.filter()

    def __len__(self) -> int:
        return self.count()

# -- Ask -------------------------------------------------------------------

    def ask(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
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
           best_ranked: Best-ranked flag.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter.
           base_filter: Base filter.
           debug: Whether to enable debugging mode.
           distinct: Whether to suppress duplicates.
           distinct_window_size: Size of distinct look-back window.
           extra_references: Extra references to attach to statements.
           limit: Limit (maximum number) of responses.
           lookahead: Number of pages to lookahead asynchronously.
           omega: Maximum number of disjoint subqueries.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           kwargs: Other keyword arguments.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._check_filter_with_options_and_run(
            self._ask_tail,
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.ask)

    def _ask_tail(self, filter: Filter, options: TOptions) -> bool:
        if filter.is_nonempty():
            return self._ask(filter, options)
        else:
            return False

    def _ask(self, filter: Filter, options: TOptions) -> bool:
        options.distinct = False
        options.limit = 1
        return bool(next(self._filter(filter, options), False))

    async def aask(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> bool:
        """Async version of :meth:`Store.ask`."""
        return await self._check_filter_with_options_and_run(
            self._aask_tail,
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.aask)

    async def _aask_tail(self, filter: Filter, options: TOptions) -> bool:
        if filter.is_nonempty():
            return await self._aask(filter, options)
        else:
            return False

    async def _aask(self, filter: Filter, options: TOptions) -> bool:
        options.distinct = False
        options.limit = 1
        async for _ in self._afilter(filter, options):
            return True
        return False

# -- Contains --------------------------------------------------------------

    def contains(self, stmt: Statement) -> bool:
        """Tests whether statement occurs in store.

        Parameters:
           stmt: Statement.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        Statement.check(stmt, self.contains, 'stmt', 1)
        return self._contains_tail(stmt)

    def _contains_tail(self, stmt: Statement) -> bool:
        filter = self._xcontains_filter_from_statement(stmt)
        if filter.is_nonempty():
            return self._contains(stmt, filter)
        else:
            return False

    def _xcontains_filter_from_statement(self, stmt: Statement) -> Filter:
        filter = self._normalize_filter(Filter.from_statement(stmt))
        if isinstance(stmt, AnnotatedStatement):
            return filter.replace(annotated=True)
        else:
            return filter

    def _contains(self, stmt: Statement, filter: Filter) -> bool:
        with self(distinct=True, limit=self.max_limit) as options:
            return stmt in self._filter(filter, options)

    async def acontains(self, stmt: Statement) -> bool:
        """Async version of :meth:`Store.contains`."""
        Statement.check(stmt, self.acontains, 'stmt', 1)
        return await self._acontains_tail(stmt)

    async def _acontains_tail(self, stmt: Statement) -> bool:
        filter = self._xcontains_filter_from_statement(stmt)
        if filter.is_nonempty():
            return await self._acontains(stmt, filter)
        else:
            return False

    async def _acontains(self, stmt: Statement, filter: Filter) -> bool:
        with self(distinct=True, limit=self.max_limit) as options:
            async for other in self._afilter(filter, options):
                if stmt == other:
                    return True
            return False

# -- Count -----------------------------------------------------------------

    def count(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
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
           best_ranked: Best-ranked flag.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter.
           base_filter: Base filter.
           debug: Whether to enable debugging mode.
           distinct: Whether to suppress duplicates.
           distinct_window_size: Size of distinct look-back window.
           extra_references: Extra references to attach to statements.
           limit: Limit (maximum number) of responses.
           lookahead: Number of pages to lookahead asynchronously.
           omega: Maximum number of disjoint subqueries.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           kwargs: Other keyword arguments.

        Returns:
           The number of statements matching filter.
        """
        return self._check_filter_with_options_and_run(
            functools.partial(self._count_x_tail, self._count),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.count)

    def _count_x_tail(
            self,
            count_x_fn: Callable[[Filter, TOptions], int],
            filter: Filter,
            options: TOptions
    ) -> int:
        if (filter.is_empty()
            or ((not filter.snak_mask & Filter.VALUE_SNAK) and (
                (count_x_fn in (
                    self._count_v, self._count_sv, self._count_pv))))):
            return 0            # nothing to do
        else:
            return count_x_fn(filter.replace(annotated=False), options)

    def _count(self, filter: Filter, options: TOptions) -> int:
        return self._count_x_fallback_overriding_distinct_and_limit(
            self._filter, filter, options)

    def count_s(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.count` with projection on subject."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._count_x_tail, self._count_s),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.count_s)

    def _count_s(self, filter: Filter, options: TOptions) -> int:
        return self._count_x_fallback_overriding_distinct_and_limit(
            self._filter_s, filter, options)

    def _count_x_fallback_overriding_distinct_and_limit(
            self,
            filter_x_fn: Callable[[Filter, TOptions], Iterator[Any]],
            filter: Filter,
            options: TOptions
    ) -> int:
        options.distinct = True
        options.limit = options.max_limit
        return sum(1 for _ in self._filter_x_tail(
            filter_x_fn, filter.replace(annotated=False), options))

    def count_p(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.count` with projection on property."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._count_x_tail, self._count_p),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.count_p)

    def _count_p(self, filter: Filter, options: TOptions) -> int:
        return self._count_x_fallback_overriding_distinct_and_limit(
            self._filter_p, filter, options)

    def count_v(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.count` with projection on value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._count_x_tail, self._count_v),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.count_v)

    def _count_v(self, filter: Filter, options: TOptions) -> int:
        return self._count_x_fallback_overriding_distinct_and_limit(
            self._filter_v, filter, options)

    def count_sp(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.count` with projection on subject and property."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._count_x_tail, self._count_sp),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.count_sp)

    def _count_sp(self, filter: Filter, options: TOptions) -> int:
        return self._count_x_fallback_overriding_distinct_and_limit(
            self._filter_sp, filter, options)

    def count_sv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.count` with projection on subject and value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._count_x_tail, self._count_sv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.count_sv)

    def _count_sv(self, filter: Filter, options: TOptions) -> int:
        return self._count_x_fallback_overriding_distinct_and_limit(
            self._filter_sv, filter, options)

    def count_pv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.count` with projection on subject and value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._count_x_tail, self._count_pv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.count_pv)

    def _count_pv(self, filter: Filter, options: TOptions) -> int:
        return self._count_x_fallback_overriding_distinct_and_limit(
            self._filter_pv, filter, options)

    async def acount(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """Async version of :meth:`Store.count`."""
        return await self._check_filter_with_options_and_run(
            functools.partial(self._acount_x_tail, self._acount),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.acount)

    async def _acount_x_tail(
            self,
            acount_x_fn: Callable[[Filter, TOptions], Awaitable[int]],
            filter: Filter,
            options: TOptions
    ) -> int:
        if (filter.is_empty()
           or ((not filter.snak_mask & Filter.VALUE_SNAK) and (
               (acount_x_fn in (
                   self._acount_v, self._acount_sv, self._acount_pv))))):
            return 0            # nothing to do
        else:
            return await acount_x_fn(
                filter.replace(annotated=False), options)

    async def _acount(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_x_fallback_overriding_distinct_and_limit(
            self._afilter, filter, options)

    async def acount_s(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.acount` with projection on subject."""
        return await self._check_filter_with_options_and_run(
            functools.partial(self._acount_x_tail, self._acount_s),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.acount_s)

    async def _acount_s(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_x_fallback_overriding_distinct_and_limit(
            self._afilter_s, filter, options)

    async def _acount_x_fallback_overriding_distinct_and_limit(
            self,
            filter_x_fn: Callable[[Filter, TOptions], AsyncIterator[Any]],
            filter: Filter,
            options: TOptions
    ) -> int:
        options.distinct = True
        options.limit = options.max_limit
        n = 0
        async for _ in self._afilter_x_tail(
                filter_x_fn, filter.replace(annotated=False), options):
            n += 1
        return n

    async def acount_p(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.acount` with projection on property."""
        return await self._check_filter_with_options_and_run(
            functools.partial(self._acount_x_tail, self._acount_p),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.acount_p)

    async def _acount_p(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_x_fallback_overriding_distinct_and_limit(
            self._afilter_p, filter, options)

    async def acount_v(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.acount` with projection on value."""
        return await self._check_filter_with_options_and_run(
            functools.partial(self._acount_x_tail, self._acount_v),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.acount_v)

    async def _acount_v(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_x_fallback_overriding_distinct_and_limit(
            self._afilter_v, filter, options)

    async def acount_sp(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.acount` with projection on subject and property."""
        return await self._check_filter_with_options_and_run(
            functools.partial(self._acount_x_tail, self._acount_sp),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.acount_sp)

    async def _acount_sp(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_x_fallback_overriding_distinct_and_limit(
            self._afilter_sp, filter, options)

    async def acount_sv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.acount` with projection on subject and value."""
        return await self._check_filter_with_options_and_run(
            functools.partial(self._acount_x_tail, self._acount_sv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.acount_sv)

    async def _acount_sv(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_x_fallback_overriding_distinct_and_limit(
            self._afilter_sv, filter, options)

    async def acount_pv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> int:
        """:meth:`Store.acount` with projection on property and value."""
        return await self._check_filter_with_options_and_run(
            functools.partial(self._acount_x_tail, self._acount_pv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.acount_pv)

    async def _acount_pv(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_x_fallback_overriding_distinct_and_limit(
            self._afilter_pv, filter, options)

# -- Filter ----------------------------------------------------------------

    def filter(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
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
           best_ranked: Best-ranked flag.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter.
           base_filter: Base filter.
           debug: Whether to enable debugging mode.
           distinct: Whether to suppress duplicates.
           distinct_window_size: Size of distinct look-back window.
           extra_references: Extra references to attach to statements.
           limit: Limit (maximum number) of responses.
           lookahead: Number of pages to lookahead asynchronously.
           omega: Maximum number of disjoint subqueries.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           kwargs: Other keyword arguments.

        Returns:
           An iterator of statements matching filter.
        """
        return self._check_filter_with_options_and_run(
            functools.partial(self._filter_x_tail, self._filter),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.filter)

    def _filter_x_tail(
            self,
            filter_x_fn: Callable[[Filter, TOptions], Iterator[T]],
            filter: Filter,
            options: TOptions
    ) -> Iterator[T]:
        if ((options.limit is not None and options.limit <= 0)
            or filter.is_empty()
            or ((not filter.snak_mask & Filter.VALUE_SNAK) and (
                (filter_x_fn in (
                    self._filter_v, self._filter_sv, self._filter_pv))))):
            return iter(())  # nothing to do
        else:
            mix = functools.partial(
                itertools.mix,
                distinct=options.distinct,
                distinct_window_size=options.distinct_window_size,
                limit=options.limit)
            if filter_x_fn == self._filter:
                return cast(
                    Iterator[T], mix(self._filter_with_extra_references(
                        filter, options)))
            else:
                return mix(filter_x_fn(
                    filter.replace(annotated=False), options))

    def _filter_with_extra_references(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Statement]:
        it = self._filter(filter, options)
        if filter.annotated and options.extra_references:
            return map(lambda s: s.annotate(
                references=options.extra_references), it)
        else:
            return it

    def _filter(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Statement]:
        return iter(())

    def filter_s(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> Iterator[Entity]:
        """:meth:`Store.filter` with projection on subject."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._filter_x_tail, self._filter_s),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.filter_s)

    def _filter_s(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Entity]:
        return self._filter_x_fallback_overriding_limit(
            self._filter_s_fallback, filter, options)

    def _filter_x_fallback_overriding_limit(
            self,
            filter_x_fn: Callable[[Filter, TOptions], Iterator[T]],
            filter: Filter,
            options: TOptions
    ) -> Iterator[T]:
        saved_limit = options.limit
        options.limit = options.max_limit
        return itertools.mix(
            filter_x_fn(filter, options),
            distinct=options.distinct, limit=saved_limit)

    def _filter_s_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Entity]:
        return map(lambda s: s.subject, self._filter(filter, options))

    def filter_p(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> Iterator[Property]:
        """:meth:`Store.filter` with projection on property."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._filter_x_tail, self._filter_p),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.filter_p)

    def _filter_p(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Property]:
        return self._filter_x_fallback_overriding_limit(
            self._filter_p_fallback, filter, options)

    def _filter_p_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Property]:
        return map(lambda s: s.snak.property, self._filter(filter, options))

    def filter_v(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> Iterator[Value]:
        """:meth:`Store.filter` with projection on value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._filter_x_tail, self._filter_v),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.filter_v)

    def _filter_v(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Value]:
        return self._filter_x_fallback_overriding_limit(
            self._filter_v_fallback, filter, options)

    def _filter_v_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Value]:
        return map(
            lambda s: cast(ValueSnak, s.snak).value,
            itertools.filter(
                lambda s: isinstance(s.snak, ValueSnak),
                self._filter(filter, options)))

    def filter_sp(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> Iterator[ValuePair[Entity, Property]]:
        """:meth:`Store.filter` with projection on subject and property."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._filter_x_tail, self._filter_sp),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.filter_sp)

    def _filter_sp(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValuePair[Entity, Property]]:
        return self._filter_x_fallback_overriding_limit(
            self._filter_sp_fallback, filter, options)

    def _filter_sp_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValuePair[Entity, Property]]:
        return map(
            lambda s: ValuePair(s.subject, s.snak.property),
            self._filter(filter, options))

    def filter_sv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> Iterator[ValuePair[Entity, Value]]:
        """:meth:`Store.filter` with projection on subject and value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._filter_x_tail, self._filter_sv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.filter_sv)

    def _filter_sv(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValuePair[Entity, Value]]:
        return self._filter_x_fallback_overriding_limit(
            self._filter_sv_fallback, filter, options)

    def _filter_sv_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValuePair[Entity, Value]]:
        return map(
            lambda s: ValuePair(s.subject, cast(ValueSnak, s.snak).value),
            itertools.filter(
                lambda s: isinstance(s.snak, ValueSnak),
                self._filter(filter, options)))

    def filter_pv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> Iterator[ValueSnak]:
        """:meth:`Store.filter` with projection on property and value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._filter_x_tail, self._filter_pv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.filter_pv)

    def _filter_pv(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValueSnak]:
        return self._filter_x_fallback_overriding_limit(
            self._filter_pv_fallback, filter, options)

    def _filter_pv_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValueSnak]:
        return map(
            lambda s: cast(ValueSnak, s.snak),
            itertools.filter(
                lambda s: isinstance(s.snak, ValueSnak),
                self._filter(filter, options)))

    def afilter(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[Statement]:
        """Async version of :meth:`Store.filter`."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._afilter_x_tail, self._afilter),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.afilter)

    def _afilter_x_tail(
            self,
            afilter_x_fn: Callable[[Filter, TOptions], AsyncIterator[T]],
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[T]:
        if ((options.limit is not None and options.limit <= 0)
            or filter.is_empty()
            or ((not filter.snak_mask & Filter.VALUE_SNAK) and (
                (afilter_x_fn in (
                    self._afilter_v, self._afilter_sv, self._afilter_pv))))):
            return self._afilter_empty_iterator()  # nothing to do
        else:
            amix = functools.partial(
                itertools.amix,
                distinct=options.distinct,
                distinct_window_size=options.distinct_window_size,
                limit=options.limit)
            if afilter_x_fn == self._afilter:
                return cast(
                    AsyncIterator[T], amix(self._afilter_with_extra_references(
                        filter, options)))
            else:
                return amix(afilter_x_fn(
                    filter.replace(annotated=False), options))

    def _afilter_with_extra_references(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Statement]:
        it = self._afilter(filter, options)
        if filter.annotated and options.extra_references:
            return itertools.amap(lambda s: s.annotate(
                references=options.extra_references), it)
        else:
            return it

    def _afilter(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Statement]:
        return self._afilter_empty_iterator()

    async def _afilter_empty_iterator(self) -> AsyncIterator[Any]:
        return
        yield

    def afilter_s(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[Entity]:
        """:meth:`Store.afilter` with projection on subject."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._afilter_x_tail, self._afilter_s),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.afilter_s)

    def _afilter_s(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Entity]:
        return self._afilter_x_fallback_overriding_limit(
            self._afilter_s_fallback, filter, options)

    def _afilter_x_fallback_overriding_limit(
            self,
            afilter_x_fn: Callable[[Filter, TOptions], AsyncIterator[T]],
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[T]:
        saved_limit = options.limit
        options.limit = options.max_limit
        return itertools.amix(
            afilter_x_fn(filter, options),
            distinct=options.distinct, limit=saved_limit)

    def _afilter_s_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Entity]:
        return itertools.amap(
            lambda s: s.subject, self._afilter(filter, options))

    def afilter_p(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[Property]:
        """:meth:`Store.afilter` with projection on property."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._afilter_x_tail, self._afilter_p),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.afilter_p)

    def _afilter_p(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Property]:
        return self._afilter_x_fallback_overriding_limit(
            self._afilter_p_fallback, filter, options)

    def _afilter_p_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Property]:
        return itertools.amap(
            lambda s: s.snak.property, self._afilter(filter, options))

    def afilter_v(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[Value]:
        """:meth:`Store.afilter` with projection on value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._afilter_x_tail, self._afilter_v),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.afilter_v)

    def _afilter_v(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Value]:
        return self._afilter_x_fallback_overriding_limit(
            self._afilter_v_fallback, filter, options)

    def _afilter_v_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Value]:
        return itertools.amap(
            lambda s: cast(ValueSnak, s.snak).value,
            itertools.afilter(
                lambda s: isinstance(s.snak, ValueSnak),
                self._afilter(filter, options)))

    def afilter_sp(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[ValuePair[Entity, Property]]:
        """:meth:`Store.afilter` with projection on subject and property."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._afilter_x_tail, self._afilter_sp),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.afilter_sp)

    def _afilter_sp(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValuePair[Entity, Property]]:
        return self._afilter_x_fallback_overriding_limit(
            self._afilter_sp_fallback, filter, options)

    def _afilter_sp_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValuePair[Entity, Property]]:
        return itertools.amap(
            lambda s: ValuePair(s.subject, s.snak.property),
            self._afilter(filter, options))

    def afilter_sv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[ValuePair[Entity, Value]]:
        """:meth:`Store.afilter` with projection on subject and value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._afilter_x_tail, self._afilter_sv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.afilter_sv)

    def _afilter_sv(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValuePair[Entity, Value]]:
        return self._afilter_x_fallback_overriding_limit(
            self._afilter_sv_fallback, filter, options)

    def _afilter_sv_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValuePair[Entity, Value]]:
        return itertools.amap(
            lambda s: ValuePair(s.subject, cast(ValueSnak, s.snak).value),
            itertools.afilter(
                lambda s: isinstance(s.snak, ValueSnak),
                self._afilter(filter, options)))

    def afilter_pv(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[ValueSnak]:
        """:meth:`Store.afilter` with projection on property and value."""
        return self._check_filter_with_options_and_run(
            functools.partial(self._afilter_x_tail, self._afilter_pv),
            # filter
            subject, property, value,
            snak_mask, subject_mask, property_mask, value_mask,
            rank_mask, best_ranked, language, annotated, snak, filter,
            # options
            base_filter, debug, distinct, distinct_window_size,
            extra_references, limit, lookahead, omega, page_size, timeout,
            # function
            self.afilter_pv)

    def _afilter_pv(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValueSnak]:
        return self._afilter_x_fallback_overriding_limit(
            self._afilter_pv_fallback, filter, options)

    def _afilter_pv_fallback(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValueSnak]:
        return itertools.amap(
            lambda s: cast(ValueSnak, s.snak),
            itertools.afilter(
                lambda s: isinstance(s.snak, ValueSnak),
                self._afilter(filter, options)))

    def filter_annotated(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            _annotate: Callable[[Statement], AnnotatedStatement] = (
                lambda stmt: stmt.annotate()),
            **kwargs: Any
    ) -> Iterator[AnnotatedStatement]:
        """:meth:`Store.filter` with annotations."""
        return map(
            _annotate,
            self.filter(
                subject, property, value,
                snak_mask, subject_mask, property_mask, value_mask,
                rank_mask, best_ranked, language, True, snak, filter,
                base_filter, debug, distinct, distinct_window_size,
                extra_references, limit, lookahead, omega, page_size, timeout,
                **kwargs))

    def afilter_annotated(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            _annotate: Callable[[Statement], AnnotatedStatement] = (
                lambda stmt: stmt.annotate()),
            **kwargs: Any
    ) -> AsyncIterator[AnnotatedStatement]:
        """:meth:`Store.afilter` with annotations."""
        return itertools.amap(
            _annotate,
            self.filter(
                subject, property, value,
                snak_mask, subject_mask, property_mask, value_mask,
                rank_mask, best_ranked, language, True, snak, filter,
                base_filter, debug, distinct, distinct_window_size,
                extra_references, limit, lookahead, omega, page_size, timeout,
                **kwargs))

    def _check_filter_with_options_and_run(
            self,
            callback: Callable[[Filter, TOptions], T],
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            function: Location | None = None,
            **kwargs: Any
    ) -> T:
        with self(
                base_filter=base_filter,
                debug=debug,
                distinct=distinct,
                distinct_window_size=distinct_window_size,
                extra_references=extra_references,
                limit=limit,
                lookahead=lookahead,
                omega=omega,
                page_size=page_size,
                timeout=timeout,
                **kwargs
        ) as options:
            return callback(
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
                    function=function), options)

    def _check_filter(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TPropertyMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            best_ranked: bool | None = None,
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
        property_mask = Filter.PropertyMask.check_optional(
            property_mask, Filter.PropertyMask.ALL,
            function, 'property_mask', 6)
        value_mask = Filter.DatatypeMask.check_optional(
            value_mask, Filter.VALUE, function, 'value_mask', 7)
        rank_mask = Filter.RankMask.check_optional(
            rank_mask, Filter.RankMask.ALL, function, 'rank_mask', 8)
        if best_ranked is None:
            best_ranked = self.base_filter.best_ranked
        else:
            best_ranked = bool(best_ranked)
        language = String.check(
            language, function, 'language', 9).content\
            if language is not None else None
        if annotated is None:
            annotated = self.base_filter.annotated
        else:
            annotated = bool(annotated)
        if filter is None:
            filter = self.base_filter.combine(Filter(
                subject=subject,
                property=property,
                value=value,
                snak_mask=snak_mask,
                subject_mask=subject_mask,
                property_mask=property_mask,
                value_mask=value_mask,
                rank_mask=rank_mask,
                language=language)).replace(
                    best_ranked=best_ranked,
                    annotated=annotated)
        else:
            filter = Filter.check(filter, function, 'filter', 12)
            filter = self.base_filter.combine(
                filter,
                Filter(
                    subject=subject,
                    property=property,
                    value=value,
                    snak_mask=snak_mask,
                    subject_mask=subject_mask,
                    property_mask=property_mask,
                    value_mask=value_mask,
                    rank_mask=rank_mask,
                    language=language)).replace(
                        best_ranked=filter.best_ranked and best_ranked,
                        annotated=filter.annotated or annotated)
        if snak is not None:
            filter = filter.combine(Filter.from_snak(None, Snak.check(
                snak, function, 'snak', 11))).replace(
                    best_ranked=filter.best_ranked and best_ranked,
                    annotated=filter.annotated or annotated)
        return self._normalize_filter(filter)

    def _normalize_filter(
            self,
            filter: Filter
    ) -> Filter:
        store_snak_mask = Filter.SnakMask(0)
        if self.snak_mask & Filter.VALUE_SNAK:
            store_snak_mask |= Filter.VALUE_SNAK
        if self.snak_mask & Filter.SOME_VALUE_SNAK:
            store_snak_mask |= Filter.SOME_VALUE_SNAK
        if self.snak_mask & Filter.NO_VALUE_SNAK:
            store_snak_mask |= Filter.NO_VALUE_SNAK
        return filter.normalize().replace(
            snak_mask=filter.snak_mask & store_snak_mask)

# -- Mix -------------------------------------------------------------------

    def mix(
            self,
            *sources: Filter | Iterable[Statement],
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> Iterator[Statement]:
        """Mixes sources of statement.

        If source is a :class:`Filter`, evaluates it over store it to obtain
        a statement iterator.

        Parameters:
           sources: Sources to mix.
           base_filter: Base filter.
           debug: Whether to enable debugging mode.
           distinct: Whether to suppress duplicates.
           distinct_window_size: Size of distinct look-back window.
           extra_references: Extra references to attach to statements.
           limit: Limit (maximum number) of responses.
           lookahead: Number of pages to lookahead asynchronously.
           omega: Maximum number of disjoint subqueries.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           kwargs: Other keyword arguments.

        Returns:
           An iterator of statements.
        """
        with self(
                base_filter=base_filter,
                debug=debug,
                distinct=distinct,
                distinct_window_size=distinct_window_size,
                extra_references=extra_references,
                limit=limit,
                lookahead=lookahead,
                omega=omega,
                page_size=page_size,
                timeout=timeout,
                **kwargs
        ) as options:
            filter_fn = functools.partial(self._filter, options=options)
            passthrough_fn = functools.partial(
                Statement.check, function=self.mix, name='sources')
            return itertools.mix(
                *map(lambda src: filter_fn(filter=src)
                     if isinstance(src, Filter)
                     else map(passthrough_fn, src), sources),
                distinct=options.distinct,
                distinct_window_size=options.distinct_window_size,
                limit=options.limit)

    async def amix(
            self,
            *sources: Filter | Iterable | AsyncIterable[Statement],
            base_filter: Filter | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            distinct_window_size: int | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            omega: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            **kwargs: Any
    ) -> AsyncIterator[Statement]:
        """Async version of :meth:`Store.mix`."""
        with self(
                base_filter=base_filter,
                debug=debug,
                distinct=distinct,
                distinct_window_size=distinct_window_size,
                extra_references=extra_references,
                limit=limit,
                lookahead=lookahead,
                omega=omega,
                page_size=page_size,
                timeout=timeout,
                **kwargs
        ) as options:
            afilter_fn = functools.partial(
                self._afilter, options=self.options)
            passthrough_fn = functools.partial(
                Statement.check, function=self.amix, name='sources')
            its = map(lambda src: afilter_fn(filter=src)
                      if isinstance(src, Filter)
                      else itertools.amap(passthrough_fn, src), sources)
            async for stmt in itertools.amix(
                    *its,
                    distinct=options.distinct,
                    distinct_window_size=options.distinct_window_size,
                    limit=options.limit):
                yield stmt
