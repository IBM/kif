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
    TypeAlias,
    TypeVar,
    Union,
)
from ..snak import Snak, TSnak
from ..term import Variable
from .closed_term_set import ClosedTermSet

TSnakSet: TypeAlias = Union['SnakSet', Iterable[TSnak]]
VSnakSet: TypeAlias = Union['SnakSetVariable', 'SnakSet']
VTSnakSet: TypeAlias = Union[Variable, VSnakSet, TSnakSet]

TQualifierRecord: TypeAlias = Union['QualifierRecord', TSnakSet]
VQualifierRecord: TypeAlias =\
    Union['QualifierRecordVariable', 'QualifierRecord']
VTQualifierRecord: TypeAlias =\
    Union[Variable, VQualifierRecord, TQualifierRecord]


class SnakSetVariable(Variable):
    """Snak set variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[SnakSet]]  # pyright: ignore


T = TypeVar('T', bound=Snak, default=Snak)


class SnakSet(
        ClosedTermSet[T],
        children_class=Snak,
        variable_class=SnakSetVariable
):
    """Set of snaks.

    Parameters:
       snaks: Snaks.
    """

    children_class: ClassVar[type[Snak]]            # pyright: ignore
    variable_class: ClassVar[type[SnakSetVariable]]  # pyright: ignore

    @override
    def __init__(self, *snaks: Snak) -> None:
        super().__init__(*snaks)


class QualifierRecordVariable(SnakSetVariable):
    """Qualifier record variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[QualifierRecord]]  # pyright: ignore


class QualifierRecord(
        SnakSet,
        children_class=Snak,
        variable_class=QualifierRecordVariable
):
    """Qualifier record (set of snaks).

    Parameters:
       snaks: Snaks.
    """

    variable_class: ClassVar[type[QualifierRecordVariable]]  # pyright: ignore

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
        elif isinstance(arg, SnakSet):
            return cls(*arg)
        else:
            return super().check(arg, function, name, position)
