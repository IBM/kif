# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc

from ..model.kif_object import Error as KIF_ObjectError
from ..model.kif_object import KIF_Object
from ..typing import Any, Callable, ClassVar, Final, Optional, TypeAlias, Union

TCompilerPattern: TypeAlias = KIF_Object


class Compiler(abc.ABC):
    """Abstract base class for compilers."""

    class Error(KIF_ObjectError):
        """Base class for compiler errors."""

    class Results(abc.ABC):
        """Abstract base class for compiler results."""

    registry: Final[dict[str, type['Compiler']]] = {}
    default: Final[str] = 'sparql'

    format: ClassVar[str]
    description: ClassVar[str]

    @classmethod
    def __init_subclass__(
            cls,
            format: str,
            description: str
    ):
        Compiler._register(cls, format, description)

    @classmethod
    def _register(
            cls,
            compiler: type['Compiler'],
            format: str,
            description: str
    ):
        compiler.format = format
        compiler.description = description
        cls.registry[format] = compiler

    @classmethod
    def from_format(
            cls,
            format: Optional[str] = None,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            details: Optional[Union[Callable[[Any], str], str]] = None
    ) -> type['Compiler']:
        fmt: str = format or cls.default
        KIF_Object._check_arg(
            fmt, fmt in cls.registry, details, function, name, position)
        assert fmt is not None
        return cls.registry[fmt]

    _pattern: TCompilerPattern

    __slots__ = (
        '_pattern',
    )

    def __init__(self, pattern: TCompilerPattern, **kwargs: Any):
        self._pattern = pattern

    @property
    def pattern(self):
        return self._pattern

    def compile(self) -> 'Compiler.Results':
        """Compiles pattern.

        Parameter:
           pat: Pattern.

        Returns:
           The compiled results.

        Raises:
           `CompilerError`: Compiler error.
        """
        raise NotImplementedError
