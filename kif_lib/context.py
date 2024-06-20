# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses
import os

from .typing import ClassVar, Optional, TracebackType


@dataclasses.dataclass
class Options:
    """KIF options."""
    model: 'ModelOptions'


@dataclasses.dataclass
class ModelOptions:
    """KIF/Model options."""
    text: 'TextOptions'


@dataclasses.dataclass
class TextOptions:
    """KIF/Model/Text options."""
    default_language: str = os.getenv('KIF_MODEL_TEXT_DEFAULT_LANGUAGE', 'en')


#: Default values for all options.
_DEFAULT_OPTIONS: Options = Options(
    model=ModelOptions(
        text=TextOptions(),
    ),
)


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
        from copy import deepcopy
        self._options = deepcopy(_DEFAULT_OPTIONS)

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
