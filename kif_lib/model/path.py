# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from ..typing import (
    Any,
    cast,
    Iterable,
    Iterator,
    Literal,
    Location,
    override,
    Self,
    TypeAlias,
    TypeVarTuple,
    Union,
    Unpack,
)
from .kif_object import KIF_Object
from .value import Property, TProperty, TValue

if TYPE_CHECKING:  # pragma: no cover
    from .filter import Filter
    from .fingerprint import PathFingerprint

TPath: TypeAlias = Union['Path', 'TSequencePath', 'TEdgePath']
TSequencePath: TypeAlias = Union['SequencePath', Iterable[TPath]]
TEdgePath: TypeAlias = Union['EdgePath', TProperty]

Ts = TypeVarTuple('Ts')
at_property = property


class Path(KIF_Object[Unpack[Ts]]):
    """Abstract base class for property path expressions."""

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, (list, tuple)):
            return cast(Self, SequencePath.check(
                arg, function or cls.check, name, position))
        else:
            return cast(Self, EdgePath.check(
                arg, function or cls.check, name, position))

    def __call__(self, value: TValue) -> PathFingerprint:
        """Constructs a path fingerprint from value.

        Parameters:
           value: Value.

        Returns:
           Path fingerprint.
        """
        from .fingerprint import PathFingerprint
        return PathFingerprint(self, value)

    def __truediv__(self, path: TPath | Literal[1]) -> Path:
        """Constructs a sequence path from path.

        Parameters:
           path: Path.

        Returns:
           Sequence path.
        """
        if path == 1:
            return self
        else:
            return SequencePath(self, cast(TPath, path))

    def __rtruediv__(self, path: TPath) -> Path:
        """Constructs a sequence path from path.

        Parameters:
           path: Path.

        Returns:
           Sequence path.
        """
        return SequencePath(path, self)

    @property
    def range_datatype_mask(self) -> Filter.DatatypeMask:
        """The datatypes shallow-matched by the range of fingerprint."""
        return self.get_range_datatype_mask()

    def get_range_datatype_mask(self) -> Filter.DatatypeMask:
        """Gets the datatypes shallow-matched by the range of fingerprint.

        Returns:
           Datatype mask.
        """
        return self._get_range_datatype_mask()

    @abc.abstractmethod
    def _get_range_datatype_mask(self) -> Filter.DatatypeMask:
        raise NotImplementedError

    def normalize(self) -> Self:
        """Reduces property path to a normal form.

        Returns:
           Normal path.
        """
        return self._normalize()

    @abc.abstractmethod
    def _normalize(self) -> Self:
        raise NotImplementedError


class SequencePath(Path):
    """Sequence path expression."""

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        else:
            if isinstance(arg, Iterable):
                return cls(*arg)
            else:
                raise cls._check_error(arg, function, name, position)

    def __init__(self, path: TPath, *paths: TPath) -> None:
        super().__init__(path, *paths)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return Path.check(arg, type(self), None, i)

    def _get_range_datatype_mask(self) -> Filter.DatatypeMask:
        from .filter import Filter
        if all(map(Filter.ENTITY.__and__,
                   map(Path.get_range_datatype_mask, self.args[:-1]))):
            return self.args[-1]._get_range_datatype_mask()
        else:
            return Filter.DatatypeMask(0)

    def _normalize(self) -> Self:
        return type(self)(*self._normalize_tail())

    def _normalize_tail(self) -> Iterator[Path]:
        for arg in map(Path.normalize, self.args):
            if isinstance(arg, SequencePath):
                yield from arg  # unpack
            else:
                yield arg


class EdgePath(Path[Property]):
    """Edge (atomic) path expression."""

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        else:
            return cls(Property.check(arg, function, name, position))

    def __init__(self, property: TProperty) -> None:
        super().__init__(property)  # type: ignore

    @at_property
    def property(self) -> Property:
        """The property of edge path."""
        return self.get_property()

    def get_property(self) -> Property:
        """Gets the property of edge path.

        Returns:
           Property.
        """
        return self.args[0]

    def _get_range_datatype_mask(self) -> Filter.DatatypeMask:
        from .filter import Filter
        return cast(Filter.DatatypeMask, Filter.DatatypeMask.check_optional(
            self.property.range, Filter.DatatypeMask.ALL))

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return Property.check(arg, type(self), None, i)

    def _normalize(self) -> Self:
        return self
