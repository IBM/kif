# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc

from ..model import Pattern
from ..model.kif_object import Error as KIF_ObjectError
from ..model.kif_object import (
    KIF_Object,
    MustBeImplementedInSubclass,
    TCallable,
)
from ..typing import Any, Callable, Final, NoReturn, Optional, Union


class Compiler(abc.ABC):
    """Abstract base class for compilers."""

    class Error(KIF_ObjectError):
        """Base class for compiler errors."""

    class Results(abc.ABC):
        """Abstract base class for compiler results."""

    registry: Final[dict[str, type['Compiler']]] = dict()
    default: Final[str] = 'sparql'

    format: str
    description: str

    @classmethod
    def __init_subclass__(
            cls,
            format: str,
            description: str):
        Compiler._register(cls, format, description)

    @classmethod
    def _register(
            cls,
            compiler: type['Compiler'],
            format: str,
            description: str):
        compiler.format = format
        compiler.description = description
        cls.registry[format] = compiler

    @classmethod
    def from_format(
            cls,
            format: Optional[str] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            details: Optional[Callable[[Any], str]] = None
    ) -> Union[type['Compiler'], NoReturn]:
        fmt: str = format or cls.default
        KIF_Object._check_arg(
            fmt, fmt in cls.registry, details, function, name, position)
        assert fmt is not None
        return cls.registry[fmt]

    _pattern: Pattern

    __slots__ = (
        '_pattern',
    )

    def __init__(self, pattern: Pattern, **kwargs: Any):
        self._pattern = pattern

    @property
    def pattern(self):
        return self._pattern

    def compile(self) -> Union['Compiler.Results', NoReturn]:
        """Compiles pattern.

        Parameter:
           pat: Pattern.

        Returns:
           The compiled results.

        Raises:
           `CompilerError`: Compiler error.
        """
        raise MustBeImplementedInSubclass
