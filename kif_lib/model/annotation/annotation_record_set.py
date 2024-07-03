# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import ClassVar, Iterable, override, TypeAlias, Union
from ..set import KIF_ObjectSet
from .annotation_record import AnnotationRecord

TAnnotationRecordSet: TypeAlias =\
    Union['AnnotationRecordSet', Iterable['AnnotationRecord']]


class AnnotationRecordSet(
        KIF_ObjectSet[AnnotationRecord],
        children_class=AnnotationRecord
):
    """Set of annotation records.

    Parameters:
       annotation_records: Annotation records.
    """

    children_class: ClassVar[type[AnnotationRecord]]  # pyright: ignore

    @override
    def __init__(self, *annotation_records: AnnotationRecord):
        super().__init__(*annotation_records)
