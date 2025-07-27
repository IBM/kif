# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import (
    Any,
    cast,
    ClassVar,
    Location,
    override,
    Self,
    Sequence,
    TypeVar,
)
from ..term import ClosedTerm

TL = TypeVar('TL', bound=ClosedTerm)
TR = TypeVar('TR', bound=ClosedTerm)


class ClosedTermPair(ClosedTerm[TL, TR]):
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
                cast(TL, cls.left_class.check(
                    arg[0], function or cls.check, name, position)),
                cast(TR, cls.right_class.check(
                    arg[1], function or cls.check, name, position)))
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
    def left(self) -> TL:
        """The left component of the pair."""
        return self[0]

    def get_left(self) -> TL:
        """Gets the left component of the pair.

        Returns:
           Closed term.
        """
        return self[0]

    @property
    def right(self) -> TR:
        """The right component of the pair."""
        return self.get_right()

    def get_right(self) -> TR:
        """Gets the right component of the pair.

        Returns:
           Closed term.
        """
        return self[1]
