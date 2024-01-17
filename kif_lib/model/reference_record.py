# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable
from typing import cast, NoReturn, Optional, Union

from .kif_object import KIF_Object, TCallable
from .snak import Snak
from .snak_set import SnakSet

TReferenceRecord = Union['ReferenceRecord', SnakSet, Iterable[Snak]]


class ReferenceRecord(SnakSet):
    """Set of snaks representing provenance information.

    Parameters:
       args: Snaks.
    """

    @classmethod
    def _check_arg_reference_record(
            cls,
            arg: TReferenceRecord,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['ReferenceRecord', NoReturn]:
        if (not ReferenceRecord.test(arg)
            and (SnakSet.test(arg)
                 or (not KIF_Object.test(arg)
                     and isinstance(arg, Iterable)))):
            refs = ReferenceRecord(*arg)
        else:
            refs = cast(ReferenceRecord, arg)
        return cls._check_arg_isinstance(
            refs, ReferenceRecord, function, name, position)

    def __init__(self, *args: Snak):
        super().__init__(*args)
