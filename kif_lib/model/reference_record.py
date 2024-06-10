# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import cast, Iterable, Optional, TypeAlias, Union
from .kif_object import KIF_Object, TLocation
from .snak import Snak
from .snak_set import SnakSet

TReferenceRecord: TypeAlias = Union['ReferenceRecord', SnakSet, Iterable[Snak]]


class ReferenceRecord(SnakSet):
    """Reference record (set of snaks).

    Parameters:
       snaks: Snaks.
    """

    @classmethod
    def _check_arg_reference_record(
            cls,
            arg: TReferenceRecord,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'ReferenceRecord':
        if (not ReferenceRecord.test(arg)
            and (SnakSet.test(arg)
                 or (not KIF_Object.test(arg)
                     and isinstance(arg, Iterable)))):
            refs = ReferenceRecord(*arg)
        else:
            refs = cast(ReferenceRecord, arg)
        return cls._check_arg_isinstance(
            refs, ReferenceRecord, function, name, position)

    def __init__(self, *snaks: Snak):
        super().__init__(*snaks)
