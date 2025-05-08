# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import functools
import sys

from ..context import Section
from ..model import Filter, ReferenceRecordSet, TQuantity, TReferenceRecordSet
from ..typing import (
    Any,
    Callable,
    ClassVar,
    Iterable,
    Location,
    Optional,
    override,
    Self,
    TypeVar,
)

T = TypeVar('T')


@dataclasses.dataclass
class _StoreOptions(Section):
    """Store options."""

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

# -- Base filter -----------------------------------------------------------

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
        self._base_filter = Filter.check(base_filter, function, name, position)

# -- Best ranked -----------------------------------------------------------

    #: The default value for the best ranked option.
    DEFAULT_BEST_RANKED: ClassVar[bool] = True

    _v_best_ranked: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_STORE_BEST_RANKED',), DEFAULT_BEST_RANKED)

    _best_ranked: bool | None

    def _init_best_ranked(self, kwargs: dict[str, Any]) -> None:
        self.best_ranked = kwargs.get(
            '_best_ranked', self.getenv_optional_bool(*self._v_best_ranked))

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

# -- Debug -----------------------------------------------------------------

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

# -- Distinct --------------------------------------------------------------

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

# -- Extra references ------------------------------------------------------

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
    def extra_references(self, extra_references: TReferenceRecordSet) -> None:
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

# -- Max. limit ------------------------------------------------------------

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

# -- Limit -----------------------------------------------------------------

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

# -- Lookahead -------------------------------------------------------------

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

# -- Max. page size --------------------------------------------------------

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

# -- Page size -------------------------------------------------------------

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

# -- Max. timeout ----------------------------------------------------------

    #: The default value for the max. timeout option.
    DEFAULT_MAX_TIMEOUT: ClassVar[float] = float(sys.maxsize)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_STORE_MAX_TIMEOUT',), DEFAULT_MAX_TIMEOUT)

    _max_timeout: float | None

    def _init_max_timeout(self, kwargs: dict[str, Any]) -> None:
        self.max_timeout = kwargs.get(
            '_max_timeout', self.getenv_optional_float(*self._v_max_timeout))

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

# -- Timeout ---------------------------------------------------------------

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


# == Store options =========================================================

class StoreOptions(_StoreOptions):
    """Store options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_parent_callback(kwargs)
        super().__init__(**kwargs)

    def _init_parent_callback(self, kwargs) -> None:
        self._parent_callback = kwargs.get(
            '_parent_callback', self._get_parent_callback)

    def _get_parent_callback(self) -> _StoreOptions:
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
        return self._do_get('_extra_references', super().get_extra_references)

    @override
    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._do_set(extra_references, '_extra_references', functools.partial(
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
