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
    Union,
)
from ..snak import Snak
from ..term import Variable
from .closed_term_set import ClosedTermSet
from .snak_set import SnakSet, SnakSetVariable, TSnakSet

TReferenceRecord: TypeAlias = Union['ReferenceRecord', TSnakSet]
VReferenceRecord: TypeAlias =\
    Union['ReferenceRecordVariable', 'ReferenceRecord']
VTReferenceRecord: TypeAlias =\
    Union[Variable, VReferenceRecord, TReferenceRecord]

TReferenceRecordSet: TypeAlias =\
    Union['ReferenceRecordSet', Iterable[TReferenceRecord]]
VReferenceRecordSet: TypeAlias =\
    Union['ReferenceRecordSetVariable', 'ReferenceRecordSet']
VTReferenceRecordSet: TypeAlias =\
    Union[Variable, VReferenceRecordSet, TReferenceRecordSet]


class ReferenceRecordVariable(SnakSetVariable):
    """Reference record variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ReferenceRecord]]  # pyright: ignore


class ReferenceRecord(
        SnakSet,
        children_class=Snak,
        variable_class=ReferenceRecordVariable
):
    """Reference record (set of snaks).

    Parameters:
       snaks: Snaks.
    """

    variable_class: ClassVar[type[ReferenceRecordVariable]]  # pyright: ignore

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


class ReferenceRecordSetVariable(Variable):
    """Reference record set variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ReferenceRecordSet]]  # pyright: ignore


class ReferenceRecordSet(
        ClosedTermSet[ReferenceRecord],
        children_class=ReferenceRecord,
        variable_class=ReferenceRecordSetVariable
):
    """Set of reference records.

    Parameters:
       reference_records: Reference records.
    """

    children_class: ClassVar[type[ReferenceRecord]]  # pyright: ignore
    variable_class: ClassVar[type[                   # pyright: ignore
        ReferenceRecordSetVariable]]

    @override
    def __init__(self, *reference_records: TReferenceRecord) -> None:
        super().__init__(*reference_records)
