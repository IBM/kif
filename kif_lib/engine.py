# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import contextlib
import dataclasses
import functools
import sys

from . import error
from .context import Context, Section
from .model import KIF_Object, TQuantity
from .typing import (
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
    Self,
    TypeVar,
)

at_property = property
T = TypeVar('T')
S = TypeVar('S')


@dataclasses.dataclass
class EngineOptions(Section):
    """Base class for engine options."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

    def __init__(self, **kwargs: Any) -> None:
        self._init_parent_callback(kwargs)
        self._init_debug(kwargs)
        self._init_max_limit(kwargs)
        self._init_limit(kwargs)

    def _init_parent_callback(self, kwargs) -> None:
        self._parent_callback = kwargs.get(
            '_parent_callback', self._get_parent_callback)

    @abc.abstractmethod
    def _get_parent_callback(self) -> EngineOptions:
        raise NotImplementedError

    @at_property
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

    # -- debug --

    #: The default value for the debug option.
    DEFAULT_DEBUG: ClassVar[bool] = False

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_ENGINE_DEBUG',), DEFAULT_DEBUG)

    _debug: bool | None

    def _init_debug(self, kwargs: dict[str, Any]) -> None:
        self.debug = cast(bool, kwargs.get(
            '_debug', self.getenv_optional_bool(*self._v_debug)))

    @at_property
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


# == Engine ================================================================

TOptions = TypeVar('TOptions', bound=EngineOptions)


class Engine(Generic[TOptions]):
    """Abstract base class for model-object producing engines."""

    #: The engine plugin registry.
    registry: ClassVar[Mapping[str, type[Engine]]]

    #: Plugin name.
    plugin_name: ClassVar[str]

    #: Plugin description.
    plugin_description: ClassVar[str]

    @classmethod
    def _register_plugin(
            cls,
            engine: type[Engine],
            name: str,
            description: str
    ) -> None:
        engine.plugin_name = name
        engine.plugin_description = description
        cls.registry[engine.plugin_name] = engine  # type: ignore

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

    @classmethod
    def _should_not_get_here(
            cls,
            details: str | None = None
    ) -> error.ShouldNotGetHere:
        """Makes a "should not get here" error.

        Parameters:
           details: Details.

        Returns:
           :class:`ShouldNotGetHere`.
        """
        return KIF_Object._should_not_get_here(details)

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
        self._update_options(debug=debug, **kwargs)

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

    @at_property
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

    @at_property
    def default_debug(self) -> bool:
        """The default value for :attr:`Engine.debug`."""
        return self.get_default_debug()

    def get_default_debug(self) -> bool:
        """Gets the default value for :attr:`Engine.debug`.

        Returns:
           Default debug flag.
        """
        return self.get_default_options().debug

    @at_property
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
            functools.partial(  # pyright: ignore
                self.options.set_debug,
                function=self.set_debug,
                name='debug',
                position=1),
            self._set_debug)

    def _set_debug(self, debug: bool) -> bool:
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
        return self.get_default_options().limit

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
