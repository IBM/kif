# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import ClassVar, Iterable, override, Union
from .annotation_record import AnnotationRecord
from .kif_object_set import KIF_ObjectSet

TAnnotationRecordSet = Union['AnnotationRecordSet', Iterable[AnnotationRecord]]
TFrozenset = frozenset


class AnnotationRecordSet(KIF_ObjectSet, children_class=AnnotationRecord):
    """Set of annotation records.

    Parameters:
       annots: Annotation records.
    """

    children_class: ClassVar[type[AnnotationRecord]]  # pyright: ignore

    @override
    def __init__(self, *objects: AnnotationRecord):
        super().__init__(*objects)  # type: ignore
