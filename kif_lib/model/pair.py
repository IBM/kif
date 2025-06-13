# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import (
    Any,
    ClassVar,
    Generic,
    Location,
    override,
    Self,
    Sequence,
    TypeAlias,
    TypeVar,
    Union,
)
from .term import ClosedTerm, Variable
from .value import Value

TValuePair: TypeAlias = Union['ValuePair', Sequence[Value]]
VValuePair: TypeAlias = Union['ValuePairVariable', 'ValuePair']
VTValuePair: TypeAlias = Union[Variable, VValuePair, TValuePair]

_TClosedTermLeft = TypeVar('_TClosedTermLeft', bound=ClosedTerm)
_TClosedTermRight = TypeVar('_TClosedTermRight', bound=ClosedTerm)

_TValueLeft = TypeVar('_TValueLeft', bound=Value)
_TValueRight = TypeVar('_TValueRight', bound=Value)


class ClosedTermPair(
        ClosedTerm,
        Generic[_TClosedTermLeft, _TClosedTermRight]
):
    """Pair of closed terms.

    Parameters:
       left: Closed term.
       right: Closed term.
    """

    left_class: ClassVar[type[ClosedTerm]]
    right_class: ClassVar[type[ClosedTerm]]

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        if 'left_class' in kwargs:
            cls.left_class = kwargs['left_class']
            assert issubclass(cls.left_class, ClosedTerm)
        if 'right_class' in kwargs:
            cls.right_class = kwargs['right_class']
            assert issubclass(cls.right_class, ClosedTerm)
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
        elif (not isinstance(arg, ClosedTerm)
              and isinstance(arg, Sequence) and len(arg) == 2):
            return cls(
                cls.left_class.check(
                    arg[0], function or cls.check, name, position),
                cls.right_class.check(
                    arg[1], function or cls.check, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # left
            return self.left_class.check(arg, type(self), None, i)
        elif i == 2:            # right
            return self.right_class.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def left(self) -> _TClosedTermLeft:
        """The left component of the pair."""
        return self[0]

    def get_left(self) -> _TClosedTermLeft:
        """Gets the left component of the pair.

        Returns:
           Closed term.
        """
        return self[0]

    @property
    def right(self) -> _TClosedTermRight:
        """The right component of the pair."""
        return self.get_right()

    def get_right(self) -> _TClosedTermRight:
        """Gets the right component of the pair.

        Returns:
           Closed term.
        """
        return self[1]


class ValuePairVariable(Variable):
    """Snak set variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ValuePair]]  # pyright: ignore


class ValuePair(
        ClosedTermPair[_TValueLeft, _TValueRight],
        left_class=Value,
        right_class=Value,
        variable_class=ValuePairVariable
):
    """Value pair.

    Parameters:
       left: Value.
       right: Value.
    """

    left_class: ClassVar[type[Value]]                 # pyright: ignore
    right_class: ClassVar[type[Value]]                # pyright: ignore
    variable_class: ClassVar[type[ValuePairVariable]]  # pyright: ignore

    @override
    def __init__(self, left: _TValueLeft, right: _TValueRight) -> None:
        super().__init__(left, right)
