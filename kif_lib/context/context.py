# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing import TYPE_CHECKING

from ..typing import ClassVar, Optional, TracebackType

if TYPE_CHECKING:  # pragma: no cover
    from .options import Options


class Context:
    """KIF context."""

    _stack: ClassVar[list['Context']] = []

    @classmethod
    def top(cls, context: Optional['Context'] = None) -> 'Context':
        """Gets the top-level context.

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
    )

    #: Context options.
    _options: Optional['Options']

    def __init__(self):
        self._options = None

    def __enter__(self) -> 'Context':
        self._stack.append(self)
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._stack.pop()

    @property
    def options(self) -> 'Options':
        """The options of context."""
        return self.get_options()

    def get_options(self) -> 'Options':
        """Gets the options of context.

        Returns:
           Options.
        """
        if self._options is None:
            from .options import Options
            self._options = Options()
        return self._options
