# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import cast, Iterable, NoReturn, Optional, override, Union
from .annotation_record import AnnotationRecord
from .kif_object import TCallable
from .kif_object_set import KIF_ObjectSet

TAnnotationRecordSet = Union['AnnotationRecordSet', Iterable[AnnotationRecord]]


class AnnotationRecordSet(KIF_ObjectSet):
    """Set of annotation records.

    Parameters:
       annots: annotation records.
    """

    @classmethod
    def _check_arg_annotation_record_set(
            cls,
            arg: TAnnotationRecordSet,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['AnnotationRecordSet', NoReturn]:
        return cast(AnnotationRecordSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    def __init__(self, *annots: AnnotationRecord):
        super().__init__(*annots)

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_annotation_record(arg, i)

    @property
    def args_set(self) -> frozenset[AnnotationRecord]:
        """The set of set arguments as a frozen set."""
        return self.get_args_set()

    @override
    def get_args_set(self) -> frozenset[AnnotationRecord]:
        """Gets the set of arguments as a frozen set.

        Returns:
           Frozen set.
        """
        return cast(frozenset[AnnotationRecord], self._get_args_set())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'AnnotationRecordSet':
        """Computes the union of set and `others`.

        Parameters:
           others: annotation record sets.

        Returns:
           The resulting annotation record set.
        """
        return cast(AnnotationRecordSet, self._union(others))
