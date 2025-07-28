# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import (
    Any,
    ClassVar,
    Iterable,
    Location,
    override,
    Self,
    Sequence,
    TypeVar,
    TypeVarTuple,
    Unpack,
)
from ..term import ClosedTerm

T = TypeVar('T', bound=ClosedTerm, default=ClosedTerm)
Ts = TypeVarTuple('Ts')


class ClosedTermSet(ClosedTerm, Sequence[T]):
    """Set of closed terms.

    Parameters:
       children: Closed term.
    """

    children_class: ClassVar[type[ClosedTerm]]

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        if 'children_class' in kwargs:
            cls.children_class = kwargs['children_class']
            assert issubclass(cls.children_class, ClosedTerm)
        super().__init_subclass__(**kwargs)

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
        elif not isinstance(arg, ClosedTerm) and isinstance(arg, Iterable):
            return cls(*map(
                lambda x: cls.children_class.check(
                    x, function or cls.check, name, position), arg))
        else:
            raise cls._check_error(arg, function, name, position)

    __slots__ = (
        '_frozenset',
    )

    _frozenset: frozenset[T]

    @override
    def _set_args(self, args: tuple[Unpack[Ts]]) -> None:
        self._frozenset = frozenset(args)  # type: ignore
        self._args = tuple(sorted(self._frozenset))

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self.children_class.check(arg, type(self), None, i)

    def __contains__(self, v: Any) -> bool:
        if isinstance(v, self.children_class):
            return v in self._frozenset
        else:
            return False

    def issubset(self, other: Self) -> bool:
        """Tests whether self is a subset of `other`.

        Parameters:
           other: Closed-term set.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._frozenset.issubset(other._frozenset)

    def issuperset(self, other: Self) -> bool:
        """Tests whether self is a superset of `other`.

        Parameters:
           other: Closed-term set.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._frozenset.issuperset(other._frozenset)

    def intersection(self, *others: Self) -> Self:
        """Computes the intersection of self and `others`.

        Parameters:
           others: Closed-term sets.

        Returns:
           Closed-term set.
        """
        return type(self)(*self._frozenset.intersection(*map(
            lambda x: x._frozenset, others)))

    def union(self, *others: Self) -> Self:
        """Computes the union of self and `others`.

        Parameters:
           others: Closed-term sets.

        Returns:
           Closed-term set.
        """
        return type(self)(*self._frozenset.union(*map(
            lambda x: x._frozenset, others)))
