# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .options import Options
from .typing import ClassVar, Optional, TracebackType


class Context:
    """KIF context.

    Stores the global options of the KIF library.
    """

    _stack: ClassVar[list['Context']] = []

    @classmethod
    def top(cls) -> 'Context':
        """Gets the current top-level context.

        Returns:
           Context.
        """
        if not cls._stack:
            cls._stack.append(cls())
        assert cls._stack
        return cls._stack[-1]

    def __init__(self):
        self._options = Options()

    @property
    def options(self):
        """The options of context."""
        return self.get_options()

    def get_options(self) -> Options:
        """Gets the options of context.

        Returns:
           Options.
        """
        return self._options

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
