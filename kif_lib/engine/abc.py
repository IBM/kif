# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import contextlib
import dataclasses
import sys

from .. import error, functools, itertools
from ..context import Context, Section
from ..model import TQuantity
from ..typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Generator,
    Generic,
    Iterable,
    Location,
    Mapping,
    Optional,
    override,
    Self,
    Set,
    TypeVar,
)

S = TypeVar('S')
T = TypeVar('T')


@dataclasses.dataclass
class _EngineOptions(Section):
    """Base class for engine options."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

    def __init__(self, **kwargs: Any) -> None:
        self._init_parent_callback(kwargs)
        self._init_debug(kwargs)
        self._init_max_limit(kwargs)
        self._init_limit(kwargs)
        self._init_lookahead(kwargs)
        self._init_max_page_size(kwargs)
        self._init_page_size(kwargs)
        self._init_max_timeout(kwargs)
        self._init_timeout(kwargs)

    def _init_parent_callback(self, kwargs) -> None:
        self._parent_callback = kwargs.get(
            '_parent_callback', self._get_parent_callback)

    @abc.abstractmethod
    def _get_parent_callback(self) -> _EngineOptions:
        raise NotImplementedError

    @property
    def parent(self) -> Self:
        """The parent options."""
        return self._parent_callback()

    def _do_get(self, field: str, super_get_fn: Callable[[], T]) -> T:
        if getattr(self, field) is None:
            try:
                return getattr(self.parent, 'get' + field)()
            except AttributeError:
                pass
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

    # -- debug --

    #: The default value for the debug option.
    DEFAULT_DEBUG: ClassVar[bool] = False

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_ENGINE_DEBUG',), DEFAULT_DEBUG)

    _debug: bool | None

    def _init_debug(self, kwargs: dict[str, Any]) -> None:
        self.debug = cast(bool, kwargs.get(
            '_debug', self.getenv_optional_bool(*self._v_debug)))

    @property
    def debug(self) -> bool:
        """Whether debugging is enabled."""
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

    # -- max_limit --

    #: The default value for the max. limit option.
    DEFAULT_MAX_LIMIT: ClassVar[int] = sys.maxsize

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_ENGINE_MAX_LIMIT',), DEFAULT_MAX_LIMIT)

    _max_limit: int | None

    def _init_max_limit(self, kwargs: dict[str, Any]) -> None:
        self.max_limit = cast(int, kwargs.get(
            '_max_limit', self.getenv_optional_int(*self._v_max_limit)))

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
        (('KIF_ENGINE_LIMIT',), DEFAULT_LIMIT)

    _limit: int | None

    def _init_limit(self, kwargs: dict[str, Any]) -> None:
        self.limit = cast(int, kwargs.get(
            '_limit', self.getenv_optional_int(*self._v_limit)))

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
        (('KIF_ENGINE_LOOKAHEAD',), DEFAULT_LOOKAHEAD)

    _lookahead: int | None

    def _init_lookahead(self, kwargs: dict[str, Any]) -> None:
        self.lookahead = cast(int, kwargs.get(
            '_lookahead', self.getenv_optional_int(*self._v_lookahead)))

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
        (('KIF_ENGINE_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

    _max_page_size: int | None

    def _init_max_page_size(self, kwargs: dict[str, Any]) -> None:
        self.max_page_size = cast(int, kwargs.get(
            '_max_page_size', self.getenv_optional_int(
                *self._v_max_page_size)))

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
        (('KIF_ENGINE_PAGE_SIZE',), DEFAULT_PAGE_SIZE)

    _page_size: int | None

    def _init_page_size(self, kwargs: dict[str, Any]) -> None:
        self.page_size = cast(int, kwargs.get(
            '_page_size', self.getenv_optional_int(*self._v_page_size)))

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
        (('KIF_ENGINE_MAX_TIMEOUT',), DEFAULT_MAX_TIMEOUT)

    _max_timeout: float | None

    def _init_max_timeout(self, kwargs: dict[str, Any]) -> None:
        self.max_timeout = cast(float, kwargs.get(
            '_max_timeout', self.getenv_optional_float(
                *self._v_max_timeout)))

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
        (('KIF_ENGINE_TIMEOUT',), None)

    _timeout: float | None

    def _init_timeout(self, kwargs: dict[str, Any]) -> None:
        self.timeout = cast(float, kwargs.get(
            '_timeout', self.getenv_optional_float(*self._v_timeout)))

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
class EngineOptions(_EngineOptions):
    """Base class for engine options (overriden)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @override
    def _get_parent_callback(self) -> _EngineOptions:
        return self.get_context().options.engine

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


# == Engine ================================================================

TOptions = TypeVar('TOptions', bound=EngineOptions)


class Engine(Generic[TOptions]):
    """Abstract base class for KIF object producing engines."""

    #: The engine plugin registry.
    registry: ClassVar[Mapping[str, type[Engine]]]

    #: Plugin name.
    plugin_name: ClassVar[str]

    #: Plugin aliases.
    plugin_aliases: ClassVar[Set[str]]

    #: Plugin description.
    plugin_description: ClassVar[str]

    @classmethod
    def _register_plugin(
            cls,
            engine: type[Engine],
            name: str,
            aliases: Iterable[str],
            description: str
    ) -> None:
        engine.plugin_name = name
        engine.plugin_aliases = frozenset(aliases)
        engine.plugin_description = description
        for name in itertools.chain(
                (engine.plugin_name,), engine.plugin_aliases):
            cls.registry[name] = engine  # type: ignore

# -- Context ---------------------------------------------------------------

    @classmethod
    def get_context(cls, context: Context | None = None) -> Context:
        """Gets the current KIF context.

        If `context` is not ``None``, returns `context`.

        Parameters:
           context: Context.

        Returns:
           Context.
        """
        return Context.top(context)

# -- Error -----------------------------------------------------------------

    class Error(error.Error):
        """Base class for engine errors."""

    @classmethod
    def _error(cls, details: str) -> Error:
        """Makes an engine error.

        Parameters:
           details: Details.

        Returns:
           :class:`Error`.
        """
        return cls.Error(details)

    #: Alias for :func:`error.missing_dependency`.
    _missing_dependency = error.missing_dependency

    #: Alias for :func:`error.should_not_get_here`.
    _should_not_get_here = error.should_not_get_here

# -- Options ---------------------------------------------------------------

    @classmethod
    @abc.abstractmethod
    def get_default_options(cls, context: Context | None = None) -> TOptions:
        """Gets the default options of engine.

        Parameters:
           context: Context.

        Returns:
           Engine options.
        """
        raise NotImplementedError

# -- Initialization --------------------------------------------------------

    __slots__ = (
        '_options',
    )

    #: Engine options.
    _options: TOptions

    def __init__(
            self,
            *args: Any,
            debug: bool | None = None,
            limit: int | None = None,
            lookahead: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
            context: Context | None = None,
            **kwargs: Any
    ) -> None:
        """
        Initializes :class:`Engine`.

        Parameters:
           plugin_name: Name of the engine plugin to instantiate.
           args: Arguments.
           debug: Whether to enable debugging mode.
           context: Context.
           kwargs: Other keyword arguments.
        """
        self._options = self.get_default_options(context)
        self._push_options()
        self._update_options(
            debug=debug,
            limit=limit,
            lookahead=lookahead,
            page_size=page_size,
            timeout=timeout,
            **kwargs)

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        """Closes engine."""
        self._close()

    def _close(self) -> None:
        pass

    async def aclose(self) -> None:
        """Async version of :meth:`Engine.close`."""
        await self._aclose()

    async def _aclose(self) -> None:
        pass

    @property
    def options(self) -> TOptions:
        """The options of engine."""
        return self.get_options()

    def get_options(self) -> TOptions:
        """Gets the options of engine.

        Returns:
           Engine options.
        """
        return self._options

    def _update_options(self, **kwargs: Any) -> None:
        if 'debug' in kwargs:
            self.set_debug(kwargs['debug'])
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
    def __call__(self, **kwargs: Any) -> Generator[TOptions, None, None]:
        self._push_options()
        self._update_options(**kwargs)
        yield self._options.copy()
        self._pop_options()
        self._update_options(**{k: getattr(self._options, k) for k in kwargs})

    def _push_options(self) -> TOptions:
        parent = self._options
        self._options = parent.replace(_parent_callback=lambda: parent)
        return self._options

    def _pop_options(self) -> TOptions:
        self._options = self._options.parent
        return self._options.parent

# -- Debug -----------------------------------------------------------------

    @property
    def default_debug(self) -> bool:
        """The default value for :attr:`Engine.debug`."""
        return self.get_default_debug()

    def get_default_debug(self) -> bool:
        """Gets the default value for :attr:`Engine.debug`.

        Returns:
           Default debug flag.
        """
        return self.get_default_options().debug

    @property
    def debug(self) -> bool:
        """The debug flag of engine (whether debugging is enabled)."""
        return self.get_debug()

    @debug.setter
    def debug(self, debug: bool | None = None) -> None:
        self.set_debug(debug)

    def get_debug(self) -> bool:
        """Gets the debug flag of engine.

        Returns:
           Debug flag.
        """
        return self.options.debug

    def set_debug(self, debug: bool | None = None) -> None:
        """Sets the debug flag of engine.

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

# -- Limit -----------------------------------------------------------------

    @property
    def max_limit(self) -> int:
        """The maximum value for :attr:`Engine.limit`."""
        return self.get_max_limit()

    def get_max_limit(self) -> int:
        """Gets the maximum value for :attr:`Engine.limit`.

        Returns:
           Maximum limit.
        """
        return self.options.max_limit

    @property
    def default_limit(self) -> int | None:
        """The default value for :attr:`Engine.limit`."""
        return self.get_default_limit()

    def get_default_limit(self) -> int | None:
        """Gets the default value for :attr:`Engine.limit`.

        Returns:
           Default limit or ``None``.
        """
        return self.get_default_options().limit

    @property
    def limit(self) -> int | None:
        """The limit of engine (maximum number of responses)."""
        return self.get_limit()

    @limit.setter
    def limit(self, limit: int | None = None) -> None:
        self.set_limit(limit)

    def get_limit(self, default: int | None = None) -> int | None:
        """Gets the limit of engine.

        If the limit is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Engine.default_limit`.

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

    def set_limit(self, limit: int | None = None) -> None:
        """Sets the limit of engine.

        If `limit` is negative, assumes zero.

        If `limit` is ``None``, resets it to the default.

        Parameters:
           limit: Limit.
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

    @property
    def default_lookahead(self) -> int:
        """The default value for :attr:`Engine.lookahead`."""
        return self.get_default_lookahead()

    def get_default_lookahead(self) -> int:
        """Gets the default value for :attr:`Engine.lookahead`.

        Returns:
           Default lookahead value.
        """
        return self.get_default_options().lookahead

    @property
    def lookahead(self) -> int:
        """The lookahead of engine."""
        return self.get_lookahead()

    @lookahead.setter
    def lookahead(self, lookahead: int | None = None) -> None:
        self.set_lookahead(lookahead)

    def get_lookahead(self) -> int:
        """Gets the lookahead of engine.

        Returns:
           Lookahead.
        """
        return self.options.lookahead

    def set_lookahead(self, lookahead: int | None = None) -> None:
        """Sets the lookhead of engine.

        If `lookahead` is negative, assumes one.

        If `lookahead` is ``None``, resets it to the default.

        Parameters:
           lookahead: Lookahead.
        """
        self._set_option_with_hooks(
            lookahead,
            self.options.get_lookahead,
            functools.partial(  # pyright: ignore
                self.options.set_lookahead,
                function=self.set_lookahead,
                name='lookahead',
                position=1),
            self._set_lookahead)

    def _set_lookahead(self, lookahead: int) -> bool:
        return True

# -- Page size -------------------------------------------------------------

    @property
    def max_page_size(self) -> int:
        """The maximum value for :attr:`Engine.page_size`."""
        return self.get_max_page_size()

    def get_max_page_size(self) -> int:
        """Gets the maximum value for :attr:`Engine.page_size`.

        Returns:
           Maximum page size.
        """
        return self.options.max_page_size

    @property
    def default_page_size(self) -> int:
        """The default value for :attr:`Engine.page_size`."""
        return self.get_default_page_size()

    def get_default_page_size(self) -> int:
        """Gets the default value for :attr:`Engine.page_size`.

        Returns:
           Default page size.
        """
        return self.get_default_options().page_size

    @property
    def page_size(self) -> int:
        """The page size of engine (size of response pages)."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: int | None = None) -> None:
        self.set_page_size(page_size)

    def get_page_size(self) -> int:
        """Gets the page size of engine.

        Returns:
           Page size.
        """
        return min(self.options.page_size, self.max_page_size)

    def set_page_size(self, page_size: int | None = None) -> None:
        """Sets the page size of engine.

        If `page_size` is negative, assumes zero.

        If `page_size` is ``None``, resets it to the default.

        Parameters:
           page_size: Page size.
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

    @property
    def max_timeout(self) -> float:
        """The maximum value for :attr:`Engine.timeout`."""
        return self.get_max_timeout()

    def get_max_timeout(self) -> float:
        """Gets the maximum value for :attr:`Engine.timeout`.

        Returns:
           Maximum timeout (in seconds).
        """
        return self.options.max_timeout

    @property
    def default_timeout(self) -> float | None:
        """The default value for :attr:`Engine.timeout`."""
        return self.get_default_timeout()

    def get_default_timeout(self) -> float | None:
        """Gets the default value for :attr:`Engine.timeout`.

        Returns:
           Timeout or ``None``.
        """
        return self.get_default_options().timeout

    @property
    def timeout(self) -> float | None:
        """The timeout of engine (in seconds)."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: float | None = None) -> None:
        self.set_timeout(timeout)

    def get_timeout(self, default: float | None = None) -> float | None:
        """Gets the timeout of engine.

        If the timeout is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Engine.default_timeout`.

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
        """Sets the timeout of engine.

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
