# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import ast
import copy
import dataclasses
import logging
import os
import pathlib
from typing import TYPE_CHECKING

from ..typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Location,
    Self,
    TypeVar,
)

T = TypeVar('T')

_logger: Final[logging.Logger] = logging.getLogger(__name__)

if TYPE_CHECKING:  # pragma: no cover
    from ..model import IRI, Quantity, String
    from .context import Context


@dataclasses.dataclass
class Section:
    """Section in KIF options."""

    #: The name of this section.
    name: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        cls.name = kwargs.get('name', cls.__qualname__)

    @classmethod
    def get_context(cls, context: Context | None = None) -> Context:
        from .context import Context
        return Context.top(context)

    @classmethod
    def _check_float(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> float:
        return float(cls._check_quantity(arg, function, name, position).amount)

    @classmethod
    def _check_optional_float(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> float | None:
        return cls._do_check_optional(
            cls._check_float, arg, default, function, name, position)

    @classmethod
    def _check_int(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        return int(cls._check_quantity(arg, function, name, position).amount)

    @classmethod
    def _check_optional_int(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        return cls._do_check_optional(
            cls._check_int, arg, default, function, name, position)

    @classmethod
    def _check_iri(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> IRI:
        from ..model import IRI
        return IRI.check(arg, function, name, position)

    @classmethod
    def _check_optional_iri(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> IRI | None:
        return cls._do_check_optional(
            cls._check_iri, arg, default, function, name, position)

    @classmethod
    def _check_path(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> pathlib.Path:
        if isinstance(arg, pathlib.PurePath):
            return pathlib.Path(arg)
        else:
            return pathlib.Path(cls._check_str(arg, function, name, position))

    @classmethod
    def _check_optional_path(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> pathlib.Path | None:
        return cls._do_check_optional(
            cls._check_path, arg, default, function, name, position)

    @classmethod
    def _check_quantity(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Quantity:
        from ..model import Quantity
        return Quantity.check(arg, function, name, position)

    @classmethod
    def _check_optional_quantity(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Quantity | None:
        return cls._do_check_optional(
            cls._check_quantity, arg, default, function, name, position)

    @classmethod
    def _check_str(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> str:
        return cls._check_string(arg, function, name, position).content

    @classmethod
    def _check_optional_str(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> str | None:
        return cls._do_check_optional(
            cls._check_str, arg, default, function, name, position)

    @classmethod
    def _check_string(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> String:
        from ..model import String
        return String.check(arg, function, name, position)

    @classmethod
    def _check_optional_string(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> String | None:
        return cls._do_check_optional(
            cls._check_string, arg, default, function, name, position)

    @classmethod
    def _do_check_optional(
            cls,
            check: Callable[
                [Any, Location | None, str | None, int | None], T],
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> T | None:
        if arg is None:
            arg = default
        if arg is None:
            return default
        else:
            return check(arg, function, name, position)

    @classmethod
    def getenv(
            cls,
            vars: str | Iterable[str],
            default: T,
            parse: Callable[[str], T] | None = None,
            _empty_returns_none: bool = False
    ) -> T:
        """Gets the value of the environment variable.

        If `vars` is an iterable, gets the value of the first non-empty
        environment variable in `vars`.

        If variable is not set, returns `default`.

        Parameters:
           vars: Variable or variables.
           default: Default value.
           parse: Value parsing function.

        Returns:
           Value or `default`.
        """
        if isinstance(vars, str):
            vars = (vars,)
        for var in vars:
            value = os.getenv(var)
            if value is None:
                continue
            if not value:
                if _empty_returns_none:
                    return None  # type: ignore
                continue
            try:
                if parse is not None:
                    return parse(value)
                else:
                    return cast(T, value)
            except BaseException:
                _logger.warning(
                    'bad value (%s) for environment variable %s',
                    value, var)
        return default

    @classmethod
    def getenv_optional(
            cls,
            vars: str | Iterable[str],
            default: T | None = None,
            parse: Callable[[str], T] | None = None
    ) -> T | None:
        """Gets the value of environment variable.

        If `vars` is an iterable, gets the value of the first non-empty
        environment variable in `vars`.

        If variable is empty or not set, returns `default`.

        Parameters:
           vars: Variable or variables.
           default: Default value.
           parse: Value parsing function.

        Returns:
           Value or `default`.
        """
        return cls.getenv(vars, default, parse, True)  # type: ignore

    @classmethod
    def getenv_bool(
            cls,
            vars: str | Iterable[str],
            default: bool
    ) -> bool:
        """:meth:`Section.getenv` for boolean variables."""
        return cls.getenv(vars, default, cls._getenv_bool_parse)

    @classmethod
    def getenv_optional_bool(
            cls,
            vars: str | Iterable[str],
            default: bool | None = None
    ) -> bool | None:
        """:meth:`Section.getenv_optional` for boolean variables."""
        return cls.getenv_optional(vars, default, cls._getenv_bool_parse)

    @classmethod
    def _getenv_bool_parse(cls, v: str) -> bool:
        return bool(ast.literal_eval(v))

    @classmethod
    def getenv_float(
            cls,
            vars: str | Iterable[str],
            default: float
    ) -> float:
        """:meth:`Section.getenv` for float variables."""
        return cls.getenv(vars, default, cls._getenv_float_parse)

    @classmethod
    def getenv_optional_float(
            cls,
            vars: str | Iterable[str],
            default: float | None
    ) -> float | None:
        """:meth:`Section.getenv_optional` for float variables."""
        return cls.getenv_optional(vars, default, cls._getenv_float_parse)

    @classmethod
    def _getenv_float_parse(cls, v: str) -> float:
        return float(ast.literal_eval(v))

    @classmethod
    def getenv_int(
            cls,
            vars: str | Iterable[str],
            default: int
    ) -> int:
        """:meth:`Section.getenv` for int variables."""
        return cls.getenv(vars, default, cls._getenv_int_parse)

    @classmethod
    def getenv_optional_int(
            cls,
            vars: str | Iterable[str],
            default: int | None
    ) -> int | None:
        """:meth:`Section.getenv_optional` for int variables."""
        return cls.getenv_optional(vars, default, cls._getenv_int_parse)

    @classmethod
    def _getenv_int_parse(cls, v: str) -> int:
        return int(ast.literal_eval(v))

    @classmethod
    def getenv_str(
            cls,
            vars: str | Iterable[str],
            default: str
    ) -> str:
        """:meth:`Section.getenv` for string variables."""
        return cls.getenv(vars, default)

    @classmethod
    def getenv_optional_str(
            cls,
            vars: str | Iterable[str],
            default: str | None = None
    ) -> str | None:
        """:meth:`Section.getenv_optional` for string variables."""
        return cls.getenv_optional(vars, default)

    @classmethod
    def getenv_path(
            cls,
            vars: str | Iterable[str],
            default: pathlib.Path
    ) -> pathlib.Path:
        """:meth:`Section.getenv` for path variables."""
        return cls.getenv(vars, default, cls._getenv_path_parse)

    @classmethod
    def getenv_optional_path(
            cls,
            vars: str | Iterable[str],
            default: pathlib.Path | None = None
    ) -> pathlib.Path | None:
        """:meth:`Section.getenv_optional` for path variables."""
        return cls.getenv_optional(vars, default, cls._getenv_path_parse)

    @classmethod
    def _getenv_path_parse(cls, v: str) -> pathlib.Path:
        return pathlib.Path(v)

    @classmethod
    def from_ast(cls, ast: dict[str, Any]) -> Self:
        """Converts abstract syntax tree to section.

        Parameters:
           ast: Abstract syntax tree.

        Returns:
           Section.
        """
        def it() -> Iterator[tuple[str, Any]]:
            for field in dataclasses.fields(cls):
                if field.name not in ast:
                    continue
                if (isinstance(field.default_factory, type)
                        and issubclass(field.default_factory, Section)):
                    yield (field.name,
                           field.default_factory.from_ast(ast[field.name]))
                else:
                    yield (field.name, ast[field.name])
        return cls(**dict(it()))

    def to_ast(self) -> dict[str, Any]:
        """Converts section to abstract syntax tree.

        Returns:
           Dictionary.
        """
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return self.to_str()

    def to_str(self) -> str:
        """Converts section to string.

        Returns:
           String.
        """
        return '\n'.join(self._to_str(self.name))

    def _to_str(self, prefix: str) -> Iterator[str]:
        for field in sorted(dataclasses.fields(self), key=lambda f: f.name):
            name = prefix + '.' + field.name
            value = getattr(self, field.name)
            if isinstance(value, Section):
                yield from value._to_str(name)
            else:
                if isinstance(field.type, type):
                    type_name = field.type.__qualname__
                else:
                    type_name = str(field.type)
                yield f'{name}: {type_name} = {value}'

    def describe(self, name: str | None = None) -> str | None:
        """Describes section or name within section.

        If `name` is given, returns the doc-string of the attribute with
        `name` in section.  Otherwise, returns the doc-string of section.

        Parameters:
           name: Attribute name.
        """
        if name is None:
            return type(self).__doc__
        else:
            try:
                return getattr(type(self), name).__doc__
            except AttributeError:
                return getattr(self, name).__doc__

    def copy(self) -> Self:
        """Shallow-copies section.

        Returns:
           A shallow copy of section.
        """
        return copy.copy(self)

    def replace(self, *args: Any, **kwargs: Any) -> Self:
        """Shallow-copies section replacing its arguments.

        Parameters:
           args: Arguments.
           kwargs: Keyword arguments.

        Returns:
           A shallow copy of section.
        """
        return dataclasses.replace(self, *args, **kwargs)
