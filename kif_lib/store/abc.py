# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import contextlib
import dataclasses
import functools
import sys

from .. import itertools
from ..context import Context, Section
from ..error import Error as KIF_Error
from ..error import ShouldNotGetHere
from ..model import (
    AnnotatedStatement,
    Filter,
    Fingerprint,
    KIF_Object,
    ReferenceRecordSet,
    Snak,
    Statement,
    String,
    TFingerprint,
    TQuantity,
    TReferenceRecordSet,
    TTextLanguage,
)
from ..typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Callable,
    cast,
    ClassVar,
    Final,
    Generator,
    Iterable,
    Iterator,
    Location,
    Optional,
    override,
    Self,
    Set,
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

# -- Error -----------------------------------------------------------------

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

# -- Options ---------------------------------------------------------------

    @dataclasses.dataclass
    class _Options(Section):
        """Base class for store options."""

        def __init__(self, **kwargs: Any) -> None:
            self._init_base_filter(kwargs)
            self._init_best_ranked(kwargs)
            self._init_debug(kwargs)
            self._init_distinct(kwargs)
            self._init_extra_references(kwargs)
            self._init_max_limit(kwargs)
            self._init_limit(kwargs)
            self._init_lookahead(kwargs)
            self._init_max_page_size(kwargs)
            self._init_page_size(kwargs)
            self._init_max_timeout(kwargs)
            self._init_timeout(kwargs)

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

        # -- best_ranked --

        #: The default value for the best ranked option.
        DEFAULT_BEST_RANKED: ClassVar[bool] = True

        _v_best_ranked: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_STORE_BEST_RANKED',), DEFAULT_BEST_RANKED)

        _best_ranked: bool | None

        def _init_best_ranked(self, kwargs: dict[str, Any]) -> None:
            self.best_ranked = kwargs.get(
                '_best_ranked',
                self.getenv_optional_bool(*self._v_best_ranked))

        @property
        def best_ranked(self) -> bool:
            """The best-ranked flag."""
            return self.get_best_ranked()

        @best_ranked.setter
        def best_ranked(self, best_ranked: bool) -> None:
            self.set_best_ranked(best_ranked)

        def get_best_ranked(self) -> bool:
            """Gets the best-ranked flag.

            Returns:
               Best-ranked flag.
            """
            assert self._best_ranked is not None
            return self._best_ranked

        def set_best_ranked(
                self,
                best_ranked: bool,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the best-ranked flag.

            Parameters:
               best_ranked: Best-ranked flag.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._best_ranked = bool(best_ranked)

        # -- debug --

        #: The default value for the debug option.
        DEFAULT_DEBUG: ClassVar[bool] = False

        _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_STORE_DEBUG',), DEFAULT_DEBUG)

        _debug: bool | None

        def _init_debug(self, kwargs: dict[str, Any]) -> None:
            self.debug = kwargs.get(
                '_debug', self.getenv_optional_bool(*self._v_debug))

        @property
        def debug(self) -> bool:
            """The debug flag."""
            return self.get_debug()

        @debug.setter
        def debug(self, debug: bool) -> None:
            self.set_debug(debug)

        def get_debug(self) -> bool:
            """Gets the debug flag.

            Returns:
               Debug flag.
            """
            assert self._debug is not None
            return self._debug

        def set_debug(
                self,
                debug: bool,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the debug flag.

            Parameters:
               debug: Debug flag.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._debug = bool(debug)

        # -- distinct --

        #: The default value for the distinct option.
        DEFAULT_DISTINCT: ClassVar[bool] = True

        _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_STORE_DISTINCT',), DEFAULT_DISTINCT)

        _distinct: bool | None

        def _init_distinct(self, kwargs: dict[str, Any]) -> None:
            self.distinct = kwargs.get(
                '_distinct', self.getenv_optional_bool(*self._v_distinct))

        @property
        def distinct(self) -> bool:
            """The distinct flag."""
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

        # -- extra_references --

        #: The default value for the extra references option
        DEFAULT_EXTRA_REFERENCES: ClassVar[ReferenceRecordSet] =\
            ReferenceRecordSet()

        _extra_references: ReferenceRecordSet | None

        def _init_extra_references(self, kwargs: dict[str, Any]) -> None:
            self.extra_references = kwargs.get(
                '_extra_references', self.DEFAULT_EXTRA_REFERENCES)

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

        # -- max_limit --

        #: The default value for the max. limit option.
        DEFAULT_MAX_LIMIT: ClassVar[int] = sys.maxsize

        _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_STORE_MAX_LIMIT',), DEFAULT_MAX_LIMIT)

        _max_limit: int | None

        def _init_max_limit(self, kwargs: dict[str, Any]) -> None:
            self.max_limit = kwargs.get(
                '_max_limit', self.getenv_optional_int(*self._v_max_limit))

        @property
        def max_limit(self) -> int:
            """The maximum limit option."""
            return self.get_max_limit()

        @max_limit.setter
        def max_limit(self, max_limit: TQuantity) -> None:
            self.set_max_limit(max_limit)

        def get_max_limit(self) -> int:
            """Gets the maximum limit option.

            Returns:
               Limit.
            """
            assert self._max_limit is not None
            return self._max_limit

        def set_max_limit(
                self,
                max_limit: TQuantity,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the maximum limit option.

            If `max_limit` is negative, assumes zero.

            Parameters:
               max_limit: Max. limit.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._max_limit = self._check_limit(
                max_limit, function, name, position)

        # -- limit --

        @classmethod
        def _check_limit(
                cls,
                arg: Any,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> int:
            return max(cls._check_int(arg, function, name, position), 0)

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

        #: The default value for the limit option.
        DEFAULT_LIMIT: ClassVar[Optional[int]] = None

        _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_STORE_LIMIT',), DEFAULT_LIMIT)

        _limit: int | None

        def _init_limit(self, kwargs: dict[str, Any]) -> None:
            self.limit = kwargs.get(
                '_limit', self.getenv_optional_int(*self._v_limit))

        @property
        def limit(self) -> int | None:
            """The limit option."""
            return self.get_limit()

        @limit.setter
        def limit(self, limit: TQuantity | None) -> None:
            self.set_limit(limit)

        def get_limit(self) -> int | None:
            """Gets the limit option.

            Returns:
               Limit or ``None``.
            """
            return self._limit

        def set_limit(
                self,
                limit: TQuantity | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the limit option.

            If `limit` is negative, assumes zero.

            If `limit` is ``None``, assumes no limit.

            Parameters:
               limit: Limit.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._limit = self._check_optional_limit(
                limit, None, function, name, position)

        # -- lookahead --

        @classmethod
        def _check_lookahead(
                cls,
                arg: Any,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> int:
            return max(cls._check_int(arg, function, name, position), 1)

        @classmethod
        def _check_optional_lookahead(
                cls,
                arg: Any | None,
                default: Any | None = None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> int | None:
            return cls._do_check_optional(
                cls._check_lookahead, arg, default, function, name, position)

        #: The default value for the lookahead option.
        DEFAULT_LOOKAHEAD: ClassVar[int] = 2

        _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_STORE_LOOKAHEAD',), DEFAULT_LOOKAHEAD)

        _lookahead: int | None

        def _init_lookahead(self, kwargs: dict[str, Any]) -> None:
            self.lookahead = kwargs.get(
                '_lookahead', self.getenv_optional_int(*self._v_lookahead))

        @property
        def lookahead(self) -> int:
            """The lookahead option."""
            return self.get_lookahead()

        @lookahead.setter
        def lookahead(self, lookahead: TQuantity) -> None:
            self.set_lookahead(lookahead)

        def get_lookahead(self) -> int:
            """Gets the lookahead option.

            Returns:
               Lookahead.
            """
            assert self._lookahead is not None
            return self._lookahead

        def set_lookahead(
                self,
                lookahead: TQuantity,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the lookahead option.

            If `lookahead` is zero or negative, assumes 1.

            Parameters:
               lookahead: Lookahead.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._lookahead = self._check_lookahead(
                lookahead, function, name, position)

        # -- max_page_size --

        #: The default value for the max. page size option.
        DEFAULT_MAX_PAGE_SIZE: ClassVar[int] = sys.maxsize

        _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_STORE_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

        _max_page_size: int | None

        def _init_max_page_size(self, kwargs: dict[str, Any]) -> None:
            self.max_page_size = kwargs.get(
                '_max_page_size', self.getenv_optional_int(
                    *self._v_max_page_size))

        @property
        def max_page_size(self) -> int:
            """The maximum page size option."""
            return self.get_max_page_size()

        @max_page_size.setter
        def max_page_size(self, max_page_size: TQuantity) -> None:
            self.set_max_page_size(max_page_size)

        def get_max_page_size(self) -> int:
            """Gets the maximum page size option.

            Returns:
               Page size.
            """
            assert self._max_page_size is not None
            return self._max_page_size

        def set_max_page_size(
                self,
                max_page_size: TQuantity,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the maximum page size option.

            If `max_page_size` is negative, assumes zero.

            Parameters:
               max_page_size: Max. page size.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._max_page_size = self._check_page_size(
                max_page_size, function, name, position)

        # -- page_size --

        @classmethod
        def _check_page_size(
                cls,
                arg: Any,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> int:
            return max(cls._check_int(arg, function, name, position), 0)

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

        #: The default value for the page size option.
        DEFAULT_PAGE_SIZE: ClassVar[int] = 100

        _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_STORE_PAGE_SIZE',), DEFAULT_PAGE_SIZE)

        _page_size: int | None

        def _init_page_size(self, kwargs: dict[str, Any]) -> None:
            self.page_size = kwargs.get(
                '_page_size', self.getenv_optional_int(*self._v_page_size))

        @property
        def page_size(self) -> int:
            """The page size option."""
            return self.get_page_size()

        @page_size.setter
        def page_size(self, page_size: TQuantity) -> None:
            self.set_page_size(page_size)

        def get_page_size(self) -> int:
            """Gets the page size option.

            Returns:
               Page size.
            """
            assert self._page_size is not None
            return self._page_size

        def set_page_size(
                self,
                page_size: TQuantity,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the page size option.

            If `page_size` is negative, assumes zero.

            Parameters:
               page_size: Page size.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._page_size = self._check_page_size(
                page_size, function, name, position)

        # -- max_timeout --

        #: The default value for the max. timeout option.
        DEFAULT_MAX_TIMEOUT: ClassVar[float] = float(sys.maxsize)

        _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
            (('KIF_STORE_MAX_TIMEOUT',), DEFAULT_MAX_TIMEOUT)

        _max_timeout: float | None

        def _init_max_timeout(self, kwargs: dict[str, Any]) -> None:
            self.max_timeout = kwargs.get(
                '_max_timeout', self.getenv_optional_float(
                    *self._v_max_timeout))

        @property
        def max_timeout(self) -> float:
            """The maximum timeout option (in seconds)."""
            return self.get_max_timeout()

        @max_timeout.setter
        def max_timeout(self, max_timeout: TQuantity) -> None:
            self.set_max_timeout(max_timeout)

        def get_max_timeout(self) -> float:
            """Gets the maximum timeout option (in seconds).

            Returns:
               Timeout.
            """
            assert self._max_timeout is not None
            return self._max_timeout

        def set_max_timeout(
                self,
                max_timeout: TQuantity,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the maximum timeout option (in seconds).

            If `max_timeout` is negative, assumes zero.

            Parameters:
               max_timeout: Max. timeout.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._max_timeout = self._check_timeout(
                max_timeout, function, name, position)

        # -- timeout --

        @classmethod
        def _check_timeout(
                cls,
                arg: Any,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> float:
            return max(cls._check_float(arg, function, name, position), 0.)

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
                cls._check_timeout, arg, default, function, name, position)

        #: The default value for the timeout option
        DEFAULT_TIMEOUT: ClassVar[Optional[int]] = None

        _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
            (('KIF_STORE_TIMEOUT',), None)

        _timeout: float | None

        def _init_timeout(self, kwargs: dict[str, Any]) -> None:
            self.timeout = kwargs.get(
                '_timeout', self.getenv_optional_float(*self._v_timeout))

        @property
        def timeout(self) -> float | None:
            """The timeout option (in seconds)."""
            return self.get_timeout()

        @timeout.setter
        def timeout(self, timeout: TQuantity | None) -> None:
            self.set_timeout(timeout)

        def get_timeout(self) -> float | None:
            """Gets the timeout option (in seconds).

            Returns:
               Timeout (in seconds) or ``None`` (no timeout).
            """
            return self._timeout

        def set_timeout(
                self,
                timeout: TQuantity | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the timeout option.

            If `timeout` is negative, assumes zero.

            Parameters:
               timeout: Timeout (in seconds) or ``None`` (no timeout).
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._timeout = self._check_optional_timeout(
                timeout, None, function, name, position)

    @dataclasses.dataclass
    class Options(_Options):
        """Base class for store options (overriden)."""

        def __init_subclass__(cls, **kwargs: Any) -> None:
            super().__init_subclass__(**kwargs)

        def __init__(self, **kwargs: Any) -> None:
            self._init_parent_callback(kwargs)
            super().__init__(**kwargs)

        def _init_parent_callback(self, kwargs) -> None:
            self._parent_callback = kwargs.get(
                '_parent_callback', self._get_parent_callback)

        def _get_parent_callback(self) -> Store._Options:
            return self.get_context().options.store

        @property
        def parent(self) -> Self:
            """The parent options."""
            return self._parent_callback()

        def _do_get(self, field: str, super_get_fn: Callable[[], T]) -> T:
            if getattr(self, field) is None:
                return getattr(self.parent, 'get' + field)()
            else:
                return super_get_fn()

        def _do_set(
                self,
                value: T | None,
                field: str,
                super_set_fn: Callable[[T], None],
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            if value is None:
                setattr(self, field, None)
            else:
                super_set_fn(value)

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
        def get_best_ranked(self) -> bool:
            return self._do_get('_best_ranked', super().get_best_ranked)

        @override
        def set_best_ranked(
                self,
                best_ranked: bool | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(best_ranked, '_best_ranked', functools.partial(
                super().set_best_ranked,
                function=function, name=name, position=position))

        @override
        def get_debug(self) -> bool:
            return self._do_get('_debug', super().get_debug)

        @override
        def set_debug(
                self,
                debug: bool | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(debug, '_debug', functools.partial(
                super().set_debug,
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
        def get_max_limit(self) -> int:
            return self._do_get('_max_limit', super().get_max_limit)

        @override
        def set_max_limit(
                self,
                max_limit: TQuantity | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            return self._do_set(max_limit, '_max_limit', functools.partial(
                super().set_max_limit,
                function=function, name=name, position=position))

        @override
        def get_limit(self) -> int | None:
            return self._do_get('_limit', super().get_limit)

        @override
        def get_lookahead(self) -> int:
            return self._do_get('_lookahead', super().get_lookahead)

        @override
        def set_lookahead(
                self,
                lookahead: TQuantity | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(lookahead, '_lookahead', functools.partial(
                super().set_lookahead,
                function=function, name=name, position=position))

        @override
        def get_max_page_size(self) -> int:
            return self._do_get('_max_page_size', super().get_max_page_size)

        @override
        def set_max_page_size(
                self,
                max_page_size: TQuantity | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(max_page_size, '_max_page_size', functools.partial(
                super().set_max_page_size,
                function=function, name=name, position=position))

        @override
        def get_page_size(self) -> int:
            return self._do_get('_page_size', super().get_page_size)

        @override
        def set_page_size(
                self,
                page_size: TQuantity | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(page_size, '_page_size', functools.partial(
                super().set_page_size,
                function=function, name=name, position=position))

        @override
        def get_max_timeout(self) -> float:
            return self._do_get('_max_timeout', super().get_max_timeout)

        @override
        def set_max_timeout(
                self,
                max_timeout: TQuantity | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(max_timeout, '_max_timeout', functools.partial(
                super().set_max_timeout,
                function=function, name=name, position=position))

        @override
        def get_timeout(self) -> float | None:
            return self._do_get('_timeout', super().get_timeout)

# -- Initialization --------------------------------------------------------

    __slots__ = (
        '_options',
    )

    def __init__(
            self,
            *args: Any,
            base_filter: Filter | None = None,
            best_ranked: bool | None = None,
            debug: bool | None = None,
            distinct: bool | None = None,
            extra_references: TReferenceRecordSet | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
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
           best_ranked: Whether to consider only best-ranked statements.
           debug: Whether to enable debugging mode.
           distinct: Whether to suppress duplicates.
           extra_references: Extra references to attach to statements.
           limit: Limit (maximum number) of responses.
           lookahead: Number of pages to lookahead asynchronously.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           kwargs: Other keyword arguments.
        """
        self._options = self.default_options
        self._push_options()
        self._update_options(
            base_filter=base_filter,
            best_ranked=best_ranked,
            debug=debug,
            distinct=distinct,
            extra_references=extra_references,
            limit=limit,
            lookahead=lookahead,
            page_size=page_size,
            timeout=timeout)

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        """Closes store."""
        self._close()

    def _close(self) -> None:
        pass

    async def aclose(self) -> None:
        """Async version of :meth:`Store.close`."""
        await self._aclose()

    async def _aclose(self) -> None:
        pass

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

    #: Store options.
    _options: Options

    @at_property
    def default_options(self) -> Options:
        """The default options of store."""
        return self.get_default_options()

    def get_default_options(self) -> Options:
        """Gets the default options of store.

        Returns:
           Store options.
        """
        return self.context.options.store.empty

    @at_property
    def options(self) -> Options:
        """The options of store."""
        return self.get_options()

    def get_options(self) -> Options:
        """Gets the options of store.

        Returns:
           Store options.
        """
        return self._options

    def _update_options(self, **kwargs: Any) -> None:
        if 'base_filter' in kwargs:
            self.set_base_filter(kwargs['base_filter'])
        if 'best_ranked' in kwargs:
            self.set_best_ranked(kwargs['best_ranked'])
        if 'debug' in kwargs:
            self.set_debug(kwargs['debug'])
        if 'distinct' in kwargs:
            self.set_distinct(kwargs['distinct'])
        if 'extra_references' in kwargs:
            self.set_extra_references(kwargs['extra_references'])
        if 'limit' in kwargs:
            self.set_limit(kwargs['limit'])
        if 'lookahead' in kwargs:
            self.set_lookahead(kwargs['lookahead'])
        if 'page_size' in kwargs:
            self.set_page_size(kwargs['page_size'])
        if 'timeout' in kwargs:
            self.set_timeout(kwargs['timeout'])

    def _set_option_with_hooks(
            self,
            value: T | None,
            get_fn: Callable[[], S],
            set_fn: Callable[[S | T | None], None],
            hook_fn: Callable[[S], bool]
    ) -> None:
        old = get_fn()
        set_fn(value)
        new = get_fn()
        if not hook_fn(new):
            set_fn(old)         # revert

    @contextlib.contextmanager
    def __call__(self, **kwargs: Any) -> Generator[Options, None, None]:
        self._push_options()
        self._update_options(**kwargs)
        yield self._options
        self._pop_options()
        self._update_options(**{k: getattr(self._options, k) for k in kwargs})

    def _push_options(self) -> Options:
        parent = self._options
        self._options = parent.replace(_parent_callback=lambda: parent)
        return self._options

    def _pop_options(self) -> Options:
        self._options = self._options.parent
        return self._options.parent

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
        return self.default_options.base_filter

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

# -- Best-ranked -----------------------------------------------------------

    @at_property
    def default_best_ranked(self) -> bool:
        """The default value for :attr:`Store.best_ranked`."""
        return self.get_default_best_ranked()

    def get_default_best_ranked(self) -> bool:
        """Gets the default value for :attr:`Store.best_ranked`.

        Returns:
           Default best_ranked flag.
        """
        return self.default_options.best_ranked

    @at_property
    def best_ranked(self) -> bool:
        """The best-ranked flag of store."""
        return self.get_best_ranked()

    @best_ranked.setter
    def best_ranked(self, best_ranked: bool | None = None) -> None:
        self.set_best_ranked(best_ranked)

    def get_best_ranked(self) -> bool:
        """Gets the best-ranked flag of store.

        Returns:
           Best-ranked flag.
        """
        return self.options.best_ranked

    def set_best_ranked(self, best_ranked: bool | None = None) -> None:
        """Sets the best-ranked flag of store.

        If `best_ranked` is ``None``, resets it to the default.

        Parameters:
           best_ranked: Best-ranked flag.
        """
        self._set_option_with_hooks(
            best_ranked,
            self.options.get_best_ranked,
            functools.partial(
                self.options.set_best_ranked,
                function=self.set_best_ranked,
                name='best_ranked',
                position=1),
            self._set_best_ranked)

    def _set_best_ranked(self, best_ranked: bool) -> bool:
        return True

# -- Debug -----------------------------------------------------------------

    @at_property
    def default_debug(self) -> bool:
        """The default value for :attr:`Store.debug`."""
        return self.get_default_debug()

    def get_default_debug(self) -> bool:
        """Gets the default value for :attr:`Store.debug`.

        Returns:
           Default debug flag.
        """
        return self.default_options.debug

    @at_property
    def debug(self) -> bool:
        """The debug flag of store (whether to enable debugging mode)."""
        return self.get_debug()

    @debug.setter
    def debug(self, debug: bool | None = None) -> None:
        self.set_debug(debug)

    def get_debug(self) -> bool:
        """Gets the debug flag of store.

        Returns:
           Debug flag.
        """
        return self.options.debug

    def set_debug(self, debug: bool | None = None) -> None:
        """Sets the debug flag of store.

        If `debug` is ``None``, resets it to the default.

        Parameters:
           debug: Debug flag.
        """
        self._set_option_with_hooks(
            debug,
            self.options.get_debug,
            functools.partial(
                self.options.set_debug,
                function=self.set_debug,
                name='debug',
                position=1),
            self._set_debug)

    def _set_debug(self, debug: bool) -> bool:
        return True

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
        return self.default_options.distinct

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
        return self.default_options.extra_references

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

# -- Limit -----------------------------------------------------------------

    @at_property
    def max_limit(self) -> int:
        """The maximum value for :attr:`Store.limit`."""
        return self.get_max_limit()

    def get_max_limit(self) -> int:
        """Gets the maximum value for :attr:`Store.limit`.

        Returns:
           Maximum limit.
        """
        return self.options.max_limit

    @at_property
    def default_limit(self) -> int | None:
        """The default value for :attr:`Store.limit`."""
        return self.get_default_limit()

    def get_default_limit(self) -> int | None:
        """Gets the default value for :attr:`Store.limit`.

        Returns:
           Default limit or ``None``.
        """
        return self.default_options.limit

    @at_property
    def limit(self) -> int | None:
        """The limit of store (maximum number of responses)."""
        return self.get_limit()

    @limit.setter
    def limit(self, limit: int | None = None) -> None:
        self.set_limit(limit)

    def get_limit(self, default: int | None = None) -> int | None:
        """Gets the limit of store.

        If the limit is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_limit`.

        Parameters:
           default: Default limit.

        Returns:
           Limit or ``None``.
        """
        limit = self.options.limit
        if limit is None:
            limit = default
        if limit is None:
            return None
        else:
            return min(limit, self.max_limit)

    def set_limit(
            self,
            limit: int | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the limit of store.

        If `limit` is negative, assumes zero.

        If `limit` is ``None``, resets it to the default.

        Parameters:
           limit: Limit.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._set_option_with_hooks(
            limit,
            self.options.get_limit,
            functools.partial(
                self.options.set_limit,
                function=self.set_limit,
                name='limit',
                position=1),
            self._set_limit)

    def _set_limit(self, limit: int | None) -> bool:
        return True

# -- Lookahead -------------------------------------------------------------

    @at_property
    def default_lookahead(self) -> int:
        """The default value for :attr:`Store.lookahead`."""
        return self.get_default_lookahead()

    def get_default_lookahead(self) -> int:
        """Gets the default value for :attr:`Store.lookahead`.

        Returns:
           Default lookahead value.
        """
        return self.default_options.lookahead

    @at_property
    def lookahead(self) -> int:
        """The lookahead of store."""
        return self.get_lookahead()

    @lookahead.setter
    def lookahead(self, lookahead: int | None = None) -> None:
        self.set_lookahead(lookahead)

    def get_lookahead(self) -> int:
        """Gets the lookahead of store.

        Returns:
           Lookahead.
        """
        return self.options.lookahead

    def set_lookahead(self, lookahead: int | None = None) -> None:
        """Sets the lookhead of store.

        If `lookahead` is negative, assumes one.

        If `lookahead` is ``None``, resets it to the default.

        Parameters:
           lookahead: Lookahead.
        """
        self._set_option_with_hooks(
            lookahead,
            self.options.get_lookahead,
            functools.partial(
                self.options.set_lookahead,
                function=self.set_lookahead,
                name='lookahead',
                position=1),
            self._set_lookahead)

    def _set_lookahead(self, lookahead: int) -> bool:
        return True

# -- Page size -------------------------------------------------------------

    @at_property
    def max_page_size(self) -> int:
        """The maximum value for :attr:`Store.page_size`."""
        return self.get_max_page_size()

    def get_max_page_size(self) -> int:
        """Gets the maximum value for :attr:`Store.page_size`.

        Returns:
           Maximum page size.
        """
        return self.default_options.max_page_size

    @at_property
    def default_page_size(self) -> int:
        """The default value for :attr:`Store.page_size`."""
        return self.get_default_page_size()

    def get_default_page_size(self) -> int:
        """Gets the default value for :attr:`Store.page_size`.

        Returns:
           Default page size.
        """
        return self.default_options.page_size

    @at_property
    def page_size(self) -> int:
        """The page size of store (size of response pages)."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: int | None = None) -> None:
        self.set_page_size(page_size)

    def get_page_size(self) -> int:
        """Gets the page size of store.

        Returns:
           Page size.
        """
        return min(self.options.page_size, self.max_page_size)

    def set_page_size(
            self,
            page_size: int | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the page size of store.

        If `page_size` is negative, assumes zero.

        If `page_size` is ``None``, resets it to the default.

        Parameters:
           page_size: Page size.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._set_option_with_hooks(
            page_size,
            self.options.get_page_size,
            functools.partial(
                self.options.set_page_size,
                function=self.set_page_size,
                name='page_size',
                position=1),
            self._set_page_size)

    def _set_page_size(self, page_size: int) -> bool:
        return True

# -- Timeout ---------------------------------------------------------------

    @at_property
    def max_timeout(self) -> float:
        """The maximum value for :attr:`Store.timeout`."""
        return self.get_max_timeout()

    def get_max_timeout(self) -> float:
        """Gets the maximum value for :attr:`Store.timeout`.

        Returns:
           Maximum timeout (in seconds).
        """
        return self.default_options.max_timeout

    @at_property
    def default_timeout(self) -> float | None:
        """The default value for :attr:`Store.timeout`."""
        return self.get_default_timeout()

    def get_default_timeout(self) -> float | None:
        """Gets the default value for :attr:`Store.timeout`.

        Returns:
           Timeout or ``None``.
        """
        return self.default_options.timeout

    @at_property
    def timeout(self) -> float | None:
        """The timeout of store (in seconds)."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: float | None = None) -> None:
        self.set_timeout(timeout)

    def get_timeout(self, default: float | None = None) -> float | None:
        """Gets the timeout of store.

        If the timeout is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_timeout`.

        Parameters:
           default: Default timeout.

        Returns:
           Timeout or ``None``.
        """
        timeout = self.options.timeout
        if timeout is None:
            timeout = default
        if timeout is None:
            return None
        else:
            return min(timeout, self.max_timeout)

    def set_timeout(
            self,
            timeout: float | None = None
    ) -> None:
        """Sets the timeout of store.

        If `timeout` is negative, assumes zero.

        If `timeout` is ``None``, resets it to the default.

        Parameters:
           timeout: Timeout.
        """
        self._set_option_with_hooks(
            timeout,
            self.options.get_timeout,
            functools.partial(
                self.options.set_timeout,
                function=self.set_timeout,
                name='timeout',
                position=1),
            self._set_timeout)

    def _set_timeout(self, timeout: float | None) -> bool:
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
        with self(distinct=False, limit=1):
            return bool(next(self._filter(filter, self.options), False))

    async def aask(
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
        """Async version of :meth:`Store.ask`.

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
           ``True`` if successful; ``False`` otherwise."""
        return await self._aask_tail(
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
                function=self.aask))

    async def _aask_tail(self, filter: Filter) -> bool:
        if filter.is_nonempty():
            return await self._aask(filter)
        else:
            return False

    async def _aask(self, filter: Filter) -> bool:
        with self(distinct=True, limit=self.max_limit):
            async for _ in self._afilter(filter, self.options):
                return True
            return False

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
        with self(distinct=True, limit=self.max_limit):
            return stmt in self._filter(filter, self.options)

    async def acontains(self, stmt: Statement) -> bool:
        """Async version of :meth:`Store.contains`.

        Parameters:
           stmt: Statement.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        Statement.check(stmt, self.acontains, 'stmt', 1)
        return await self._acontains_tail(stmt)

    async def _acontains_tail(self, stmt: Statement) -> bool:
        filter = self._xcontains_filter_from_statement(stmt)
        if filter.is_nonempty():
            return await self._acontains(stmt, filter)
        else:
            return False

    async def _acontains(self, stmt: Statement, filter: Filter) -> bool:
        with self(distinct=True, limit=self.max_limit):
            async for other in self._afilter(filter, self.options):
                if stmt == other:
                    return True
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
        with self(distinct=True, limit=self.max_limit):
            return sum(1 for _ in self._filter(filter, self.options))

    async def acount(
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
        """Async version of :meth:`Store.count`.

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
        return await self._acount_tail(
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
                function=self.acount))

    async def _acount_tail(self, filter: Filter) -> int:
        if filter.is_nonempty():
            return await self._acount(filter)
        else:
            return 0

    async def _acount(self, filter: Filter) -> int:
        with self(distinct=True, limit=self.max_limit):
            n = 0
            async for _ in self._afilter(filter, self.options):
                n += 1
            return n

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
            distinct: bool | None = None,
            limit: int | None = None
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
           distinct: Whether to skip duplicated matches.
           limit: Limit (maximum number) of statements to return.

        Returns:
           An iterator of statements matching filter.
        """
        with self(distinct=distinct, limit=limit):
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
                    function=self.filter), self.options)

    def _filter_tail(
            self,
            filter: Filter,
            options: Options
    ) -> Iterator[Statement]:
        if ((options.limit is None or options.limit > 0)
                and filter.is_nonempty()):
            stmts = self._filter(filter, options)
            if filter.annotated and options.extra_references:
                return map(lambda s: s.annotate(
                    references=options.extra_references), stmts)
            else:
                return stmts
        else:
            return iter(())

    def _filter(
            self,
            filter: Filter,
            options: Options
    ) -> Iterator[Statement]:
        return iter(())

    def afilter(
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
            distinct: bool | None = None,
            limit: int | None = None
    ) -> AsyncIterator[Statement]:
        """Async version of :meth:`Store.filter`.

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
           distinct: Whether to skip duplicated matches.
           limit: Limit (maximum number) of statements to return.

        Returns:
           An async iterator of statements matching filter.
        """
        with self(distinct=distinct, limit=limit):
            return self._afilter_tail(
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
                    function=self.afilter), self.options)

    async def _afilter_tail(
            self,
            filter: Filter,
            options: Options
    ) -> AsyncIterator[Statement]:
        if ((options.limit is None or options.limit > 0)
                and filter.is_nonempty()):
            async for stmt in self._afilter(filter, options):
                if filter.annotated and options.extra_references:
                    yield stmt.annotate(references=options.extra_references)
                else:
                    yield stmt
        else:
            return              # empty async iterator
            yield

    async def _afilter(
            self,
            filter: Filter,
            options: Options
    ) -> AsyncIterator[Statement]:
        return                  # empty async iterator
        yield

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

    def afilter_annotated(
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
    ) -> AsyncIterator[AnnotatedStatement]:
        """:meth:`Store.afilter` with annotations.

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
           An async iterator of annotated statements matching filter.
        """
        return cast(AsyncIterator[AnnotatedStatement], self.afilter(
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
                language=language)).replace(annotated=annotated)
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
        if self.snak_mask & Filter.VALUE_SNAK:
            store_snak_mask |= Filter.VALUE_SNAK
        if self.snak_mask & Filter.SOME_VALUE_SNAK:
            store_snak_mask |= Filter.SOME_VALUE_SNAK
        if self.snak_mask & Filter.NO_VALUE_SNAK:
            store_snak_mask |= Filter.NO_VALUE_SNAK
        return filter.normalize().replace(
            snak_mask=filter.snak_mask & store_snak_mask)

    def mix(
            self,
            *sources: Filter | Iterable[Statement],
            distinct: bool | None = None,
            limit: int | None = None
    ) -> Iterator[Statement]:
        """Mixes sources of statement.

        If source is a :class:`Filter`, evaluates it over store it to obtain
        a statement iterator.

        Parameters:
           sources: Sources to mix.
           distinct: Whether to skip duplicates.
           limit: Limit (maximum number) of statements to yield.

        Returns:
           An iterator of statements.
        """
        with self(distinct=distinct, limit=limit):
            filter_fn = functools.partial(self._filter, options=self.options)
            passthrough_fn = functools.partial(
                Statement.check, function=self.mix, name='sources')
            return itertools.mix(
                *map(lambda src: filter_fn(filter=src)
                     if isinstance(src, Filter)
                     else map(passthrough_fn, src), sources),
                distinct=self.distinct, limit=self.limit)

    async def amix(
            self,
            *sources: Filter | Iterable | AsyncIterable[Statement],
            distinct: bool | None = None,
            limit: int | None = None
    ) -> AsyncIterator[Statement]:
        """Async version of :meth:`Store.mix`.

        If source is a :class:`Filter`, evaluates it over store it to obtain
        a statement iterator.

        Parameters:
           sources: Sources to mix.
           distinct: Whether to skip duplicates.
           limit: Limit (maximum number) of statements to yield.

        Returns:
           An async iterator of statements.
        """
        with self(distinct=distinct, limit=limit):
            afilter_fn = functools.partial(
                self._afilter, options=self.options)
            passthrough_fn = functools.partial(
                Statement.check, function=self.amix, name='sources')
            its = map(lambda src: afilter_fn(filter=src)
                      if isinstance(src, Filter)
                      else itertools.amap(passthrough_fn, src), sources)
            async for stmt in itertools.amix(
                    *its, distinct=self.distinct, limit=self.limit):
                yield stmt
