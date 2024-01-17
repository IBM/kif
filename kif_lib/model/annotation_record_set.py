# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable
from typing import cast, NoReturn, Optional, Union

from .annotation_record import AnnotationRecord
from .kif_object import TCallable
from .kif_object_set import KIF_ObjectSet

TAnnotationRecordSet = Union['AnnotationRecordSet', Iterable[AnnotationRecord]]


class AnnotationRecordSet(KIF_ObjectSet):
    """Set of annotation records.

    Parameters:
       args: annotation records.
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

    def __init__(self, *args: AnnotationRecord):
        super().__init__(*args)

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_annotation_record(arg, i)

    @property
    def args_set(self) -> frozenset[AnnotationRecord]:
        """Set arguments as frozen set."""
        return self.get_args_set()

    def get_args_set(self) -> frozenset[AnnotationRecord]:
        """Gets set arguments as frozen set.

        Returns:
           Set arguments as set.
        """
        return cast(frozenset[AnnotationRecord], self._get_args_set())

    def union(
            self,
            *others: 'AnnotationRecordSet'
    ) -> 'AnnotationRecordSet':
        """Computes the union of set and `others`.

        Parameters:
           others: annotation record sets.

        Returns:
           The resulting annotation record set.
        """
        return cast(AnnotationRecordSet, self._union(others))
