# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import ClassVar, Iterable, override, Union
from .kif_object_set import KIF_ObjectSet
from .reference_record import ReferenceRecord, TReferenceRecord

TReferenceRecordSet = Union['ReferenceRecordSet', Iterable[ReferenceRecord]]


class ReferenceRecordSet(KIF_ObjectSet, children_class=ReferenceRecord):
    """Set of reference records.

    Parameters:
       refs: Reference records.
    """

    children_class: ClassVar[type[ReferenceRecord]]  # pyright: ignore

    @override
    def __init__(self, *objects: TReferenceRecord):
        super().__init__(*objects)  # type: ignore
