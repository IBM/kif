# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from ..typing import ClassVar, TracebackType

if TYPE_CHECKING:  # pragma: no cover
    from .options import Options
    from .registry import Registry


class Context:
    """KIF context."""

    _stack: ClassVar[list[Context]] = []

    @classmethod
    def top(cls, context: Context | None = None) -> Context:
        """Gets the current context.

        If `context` is not ``None``, returns `context`.

        Returns:
           Context.
        """
        if context is not None:
            return context
        if not cls._stack:
            cls._stack.append(cls())
        assert cls._stack
        return cls._stack[-1]

    __slots__ = (
        '_options',
        '_registry',
    )

    #: Context options.
    _options: Options | None

    #: Context registry.
    _registry: Registry | None

    def __init__(self) -> None:
        self._options = None
        self._registry = None

    def __enter__(self) -> Context:
        self._stack.append(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._stack.pop()

    @property
    def options(self) -> Options:
        """The options of context."""
        return self.get_options()

    def get_options(self) -> Options:
        """Gets the options of context.

        Returns:
           Options.
        """
        if self._options is None:
            from .options import Options
            self._options = Options()
        return self._options

    @property
    def registry(self) -> Registry:
        """The registry of context."""
        return self.get_registry()

    def get_registry(self) -> Registry:
        """Gets the registry of context.

        Returns:
           Registry.
        """
        if self._registry is None:
            from ..namespace import PREFIXES
            from .registry import Registry
            self._registry = Registry(self, PREFIXES)
        return self._registry
