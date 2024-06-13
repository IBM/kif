# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import Any, cast, Iterable, Optional, override, Union
from .annotation_record import AnnotationRecord
from .kif_object import TLocation
from .kif_object_set import KIF_ObjectSet

TAnnotationRecordSet = Union['AnnotationRecordSet', Iterable[AnnotationRecord]]
TFrozenset = frozenset


class AnnotationRecordSet(KIF_ObjectSet):
    """Set of annotation records.

    Parameters:
       annots: Annotation records.
    """

    @classmethod
    def _check_arg_annotation_record_set(
            cls,
            arg: TAnnotationRecordSet,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'AnnotationRecordSet':
        return cast(AnnotationRecordSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._preprocess_arg_annotation_record(arg, i)

    @property
    @override
    def frozenset(self) -> TFrozenset[AnnotationRecord]:
        """The set of annotation records as a frozen set."""
        return self.get_frozenset()

    @override
    def get_frozenset(self) -> TFrozenset[AnnotationRecord]:
        """Gets the set of annotation records as a frozen set.

        Returns:
           Frozen set.
        """
        return cast(frozenset[AnnotationRecord], self._get_frozenset())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'AnnotationRecordSet':
        """Computes the union of set and `others`.

        Parameters:
           others: Annotation record sets.

        Returns:
           The resulting annotation record set.
        """
        return cast(AnnotationRecordSet, self._union(others))
