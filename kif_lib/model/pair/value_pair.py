# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import ClassVar, override, Sequence, TypeAlias, TypeVar, Union
from ..term import Variable
from ..value import Value
from .closed_term_pair import ClosedTermPair

TValuePair: TypeAlias = Union['ValuePair', Sequence[Value]]
VValuePair: TypeAlias = Union['ValuePairVariable', 'ValuePair']
VTValuePair: TypeAlias = Union[Variable, VValuePair, TValuePair]

TL = TypeVar('TL', bound=Value)
TR = TypeVar('TR', bound=Value)


class ValuePairVariable(Variable):
    """Snak set variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ValuePair]]  # pyright: ignore


class ValuePair(
        ClosedTermPair[TL, TR],
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
    def __init__(self, left: TL, right: TR) -> None:
        super().__init__(left, right)
