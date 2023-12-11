# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable
from typing import cast, NoReturn, Optional, Union

from .kif_object import TCallable
from .kif_object_set import KIF_ObjectSet
from .reference_record import ReferenceRecord

TReferenceRecordSet = Union['ReferenceRecordSet', Iterable[ReferenceRecord]]


class ReferenceRecordSet(KIF_ObjectSet):
    """Set of reference records.

    Parameters:
       args: Reference records.
    """

    @classmethod
    def _check_arg_reference_record_set(
            cls,
            arg: TReferenceRecordSet,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['ReferenceRecordSet', NoReturn]:
        return cast(ReferenceRecordSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    def __init__(self, *args: ReferenceRecord):
        super().__init__(*args)

    def _preprocess_arg(self, arg, i):
        return self._preprocess_arg_reference_record(arg, i)

    @property
    def args_set(self) -> frozenset[ReferenceRecord]:
        """Set arguments as frozen set."""
        return self.get_args_set()

    def get_args_set(self) -> frozenset[ReferenceRecord]:
        """Gets set arguments as frozen set.

        Returns:
           Set arguments as set.
        """
        return cast(frozenset[ReferenceRecord], self._get_args_set())

    def union(self, *others: 'ReferenceRecordSet') -> 'ReferenceRecordSet':
        """Computes the union of set and `others`.

        Parameters:
           others: Reference record sets.

        Returns:
           The resulting reference record set.
        """
        return cast(ReferenceRecordSet, self._union(others))
